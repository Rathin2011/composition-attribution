"""Evaluate a fitted J-Lens on one generalized composition task.

Input
-----
The task's merged ``logit_lens_evaluation.jsonl.gz`` file, its
``baseline_summary.json`` candidate catalog, and the fitted Stage 1 OLMo 3
Jacobian lens.  The Logit-Lens input fixes the exact prompt instances,
paper-token eligibility, and final-query token span used by both lenses.

Output
------
One compressed JSONL row per input prompt instance.  Eligible rows receive a
``j_lens`` object containing:

* ``jlens_z`` with shape ``[n_Fx, n_fitted_layers]``;
* ``jlens_rr`` for the true intermediate at every fitted layer; and
* a compositional/ambiguous/shortcut-candidate classification.

At each fitted layer, all candidate logits are taken from the same query
position: the earliest position giving the true Fx its best full-vocabulary
rank.  This matches the generalized Logit-Lens position-selection rule.

This program evaluates an already fitted lens.  It does not fit Jacobians,
generate answers, or modify model activations.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Literal, Mapping, Sequence

import torch

from evaluate_baseline import (
    MODEL_DTYPE,
    MODEL_ID,
    STAGE_ONE_COMMIT,
    STAGE_ONE_REVISION,
    ensure_outputs,
    open_text,
)
from evaluate_logit_lens import (
    COMPOSITION_RR_THRESHOLD,
    SHORTCUT_RR_THRESHOLD,
    classify_rank,
    load_fx_catalog,
    read_correct_slice,
    select_best_position_values,
)
from tasks import TASKS, get_task_spec


EvidenceGroup = Literal["compositional", "ambiguous", "shortcut_candidate"]
GROUPS = ("compositional", "ambiguous", "shortcut_candidate")
EXPECTED_SOURCE_LAYERS = (12, 16, 18, 20, 22, 24)
EXPECTED_HIDDEN_SIZE = 4096
EXPECTED_FIT_PROMPTS = 1000
EXPECTED_LENS_SHA256 = (
    "c7b0d3b0bc2cfda2aec1365e71261bdec3213f12548617ad6f44c3e5f0ba5821"
)
JLENS_COMMIT = "581d398613e5602a5af361e1c34d3a92ea82ba8e"

PROJECT_DIR = Path(__file__).resolve().parent.parent
COMPOSITION_EXPERIMENTS_DIR = PROJECT_DIR.parent.parent
JLENS_DIR = COMPOSITION_EXPERIMENTS_DIR / "JLens"
VENDORED_JLENS = JLENS_DIR / "vendor" / "jacobian-lens"
DEFAULT_LENS = JLENS_DIR / "results" / "fit_1000" / "merged" / "jacobian_lens.pt"


@dataclass
class RunningSummary:
    """Count J-Lens groups, exclusions, and Logit-to-J-Lens transitions."""

    input_records: int = 0
    eligible_records: int = 0
    excluded_records: int = 0
    groups: Counter[str] = field(default_factory=Counter)
    exclusions: Counter[str] = field(default_factory=Counter)
    transitions: Counter[str] = field(default_factory=Counter)

    def add(self, record: Mapping[str, Any]) -> None:
        self.input_records += 1
        measurement = record["j_lens"]
        if measurement["paper_token_eligible"]:
            self.eligible_records += 1
            jlens_group = measurement["classification"]["group"]
            llens_group = record["logit_lens"]["classification"]["group"]
            self.groups[jlens_group] += 1
            self.transitions[f"{llens_group}->{jlens_group}"] += 1
        else:
            self.excluded_records += 1
            self.exclusions[measurement["paper_token_filter_reason"]] += 1

    def as_dict(self) -> dict[str, Any]:
        if self.input_records != self.eligible_records + self.excluded_records:
            raise RuntimeError("eligible and excluded counts do not partition input")
        if sum(self.groups.values()) != self.eligible_records:
            raise RuntimeError("J-Lens groups do not partition eligible input")
        if sum(self.transitions.values()) != self.eligible_records:
            raise RuntimeError("lens transitions do not partition eligible input")
        return {
            "num_input_records": self.input_records,
            "num_paper_token_eligible": self.eligible_records,
            "num_paper_token_excluded": self.excluded_records,
            "paper_token_exclusion_reasons": dict(sorted(self.exclusions.items())),
            "classification_counts": {group: self.groups[group] for group in GROUPS},
            "logit_lens_to_j_lens_transitions": dict(
                sorted(self.transitions.items())
            ),
        }


def parse_args() -> argparse.Namespace:
    """Parse one task-general full, smoke, or array-shard evaluation."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, choices=sorted(TASKS))
    parser.add_argument("--input", type=Path)
    parser.add_argument("--catalog-summary", type=Path)
    parser.add_argument("--lens", type=Path, default=DEFAULT_LENS)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--summary-output", type=Path)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--num-records", type=int)
    parser.add_argument("--max-seq-len", type=int, default=512)
    parser.add_argument("--candidate-chunk-size", type=int, default=16)
    parser.add_argument("--progress-every", type=int, default=10)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument(
        "--allow-download",
        action="store_true",
        help="Allow downloads instead of requiring cached model files.",
    )
    return parser.parse_args()


def file_sha256(path: Path) -> str:
    """Return the hexadecimal SHA-256 digest of one file."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_logit_lens_record(record: Mapping[str, Any]) -> None:
    """Require a merged generalized Logit-Lens row suitable for J-Lens."""

    lens = record.get("logit_lens")
    if not isinstance(lens, Mapping):
        raise ValueError("input record lacks logit_lens")
    eligible = lens.get("paper_token_eligible")
    if not isinstance(eligible, bool):
        raise ValueError("logit_lens eligibility must be boolean")
    if eligible:
        if lens.get("classification", {}).get("group") not in GROUPS:
            raise ValueError("eligible input has invalid Logit-Lens classification")
        query_start = lens.get("query_token_start")
        num_positions = lens.get("num_query_positions")
        if (
            not isinstance(query_start, int)
            or isinstance(query_start, bool)
            or query_start < 0
            or not isinstance(num_positions, int)
            or isinstance(num_positions, bool)
            or num_positions < 1
        ):
            raise ValueError("eligible input has invalid query-token span")
        token_info = lens.get("node_token_info")
        if not isinstance(token_info, Mapping) or set(token_info) != {
            "x",
            "Fx",
            "GFx",
        }:
            raise ValueError("eligible input lacks node_token_info")
    elif lens.get("classification") is not None:
        raise ValueError("paper-filtered input must not be classified")


def candidate_logits_and_ranks(
    logits_by_layer: Mapping[int, torch.Tensor],
    candidate_token_ids: Sequence[int],
    source_layers: Sequence[int],
    *,
    candidate_chunk_size: int,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Select candidate logits and compute full-vocabulary ranks.

    Inputs:
        Official J-Lens logits ``{layer: [P,V]}``, ``K`` candidate token IDs,
        and the fitted layers in their saved order.
    Outputs:
        CPU tensors ``(logits, ranks)`` with shape ``[P,L,K]``.

    Candidate ranks are chunked to keep the temporary ``[P,V,K]`` comparison
    bounded.  Ties receive the shared best rank: ``1 + count(logit > target)``.
    """

    layers = tuple(source_layers)
    if not layers or set(logits_by_layer) != set(layers):
        raise ValueError("J-Lens logits must exactly cover source_layers")
    if not candidate_token_ids:
        raise ValueError("at least one candidate token is required")
    if candidate_chunk_size < 1:
        raise ValueError("candidate_chunk_size must be positive")

    selected_layers = []
    rank_layers = []
    expected_shape: tuple[int, int] | None = None
    ids = [int(token_id) for token_id in candidate_token_ids]
    for layer in layers:
        logits = logits_by_layer[layer]
        if not isinstance(logits, torch.Tensor) or logits.ndim != 2:
            raise ValueError("each J-Lens tensor must have shape [positions,vocab]")
        if expected_shape is None:
            expected_shape = tuple(logits.shape)
        if tuple(logits.shape) != expected_shape:
            raise ValueError("J-Lens layer logits have inconsistent shapes")
        if any(token_id < 0 or token_id >= logits.shape[1] for token_id in ids):
            raise ValueError("candidate token is outside the vocabulary")

        selected = logits[:, ids]
        layer_rank_chunks = []
        for start in range(0, len(ids), candidate_chunk_size):
            targets = selected[:, start : start + candidate_chunk_size]
            ranks = 1 + (logits.unsqueeze(2) > targets.unsqueeze(1)).sum(dim=1)
            layer_rank_chunks.append(ranks.long().cpu())
        selected_layers.append(selected.float().cpu())
        rank_layers.append(torch.cat(layer_rank_chunks, dim=1))

    return (
        torch.stack(selected_layers, dim=1),
        torch.stack(rank_layers, dim=1),
    )


def validate_loaded_lens(lens: Any) -> tuple[int, ...]:
    """Require the verified 1,000-prompt, six-layer Stage 1 lens."""

    layers = tuple(int(layer) for layer in lens.source_layers)
    if layers != EXPECTED_SOURCE_LAYERS:
        raise ValueError(
            f"expected source layers {EXPECTED_SOURCE_LAYERS}, found {layers}"
        )
    if int(lens.n_prompts) != EXPECTED_FIT_PROMPTS:
        raise ValueError(
            f"expected {EXPECTED_FIT_PROMPTS} fitting prompts, found {lens.n_prompts}"
        )
    if int(lens.d_model) != EXPECTED_HIDDEN_SIZE:
        raise ValueError(
            f"expected hidden size {EXPECTED_HIDDEN_SIZE}, found {lens.d_model}"
        )
    if set(lens.jacobians) != set(layers):
        raise ValueError("saved Jacobians do not match source-layer metadata")
    expected_shape = (EXPECTED_HIDDEN_SIZE, EXPECTED_HIDDEN_SIZE)
    if any(tuple(lens.jacobians[layer].shape) != expected_shape for layer in layers):
        raise ValueError("saved Jacobian has an unexpected shape")
    return layers


def excluded_result(record: Mapping[str, Any]) -> dict[str, Any]:
    """Preserve a paper-filtered row without invoking the model or J-Lens."""

    output = dict(record)
    output["j_lens"] = {
        "paper_token_eligible": False,
        "paper_token_filter_reason": record["logit_lens"][
            "paper_token_filter_reason"
        ],
        "source_layers": list(EXPECTED_SOURCE_LAYERS),
        "classification": None,
        "jlens_z": None,
        "jlens_rr": None,
    }
    return output


def analyze_record(
    lens: Any,
    adapter: Any,
    record: Mapping[str, Any],
    fx_catalog: Sequence[Mapping[str, Any]],
    *,
    source_layers: Sequence[int],
    max_seq_len: int,
    candidate_chunk_size: int,
) -> dict[str, Any]:
    """Apply J-Lens and summarize all candidate-Fx logits for one prompt."""

    validate_logit_lens_record(record)
    get_task_spec(record["task"]).validate_prompt(record["prompt"], record["query"]["x"])
    logit_lens = record["logit_lens"]
    query_start = int(logit_lens["query_token_start"])
    num_positions = int(logit_lens["num_query_positions"])
    positions = list(range(query_start, query_start + num_positions))

    logits_by_layer, _, input_ids = lens.apply(
        adapter,
        record["prompt"],
        layers=list(source_layers),
        positions=positions,
        max_seq_len=max_seq_len,
        use_jacobian=True,
    )
    if positions[-1] >= int(input_ids.shape[1]):
        raise ValueError("saved query-token span exceeds the tokenized prompt")

    values = [row["value"] for row in fx_catalog]
    try:
        target_index = values.index(record["query"]["Fx"])
    except ValueError as error:
        raise ValueError("true Fx is absent from the candidate catalog") from error

    candidate_logits, candidate_ranks = candidate_logits_and_ranks(
        logits_by_layer,
        [int(row["token_ids"][0]) for row in fx_catalog],
        source_layers,
        candidate_chunk_size=candidate_chunk_size,
    )
    jlens_z, jlens_rr, selected_positions = select_best_position_values(
        candidate_logits,
        candidate_ranks,
        target_index=target_index,
    )
    best_rank = int(candidate_ranks[:, :, target_index].min().item())
    peak_rr = 1.0 / best_rank
    peak_layers = [
        int(source_layers[index])
        for index, value in enumerate(jlens_rr)
        if value == peak_rr
    ]

    output = dict(record)
    output["j_lens"] = {
        "paper_token_eligible": True,
        "paper_token_filter_reason": None,
        "query_token_start": query_start,
        "num_query_positions": num_positions,
        "source_layers": [int(layer) for layer in source_layers],
        "layer_index_definition": "post_decoder_block_zero_based",
        "rank_scope": "complete_vocabulary",
        "target_definition": get_task_spec(record["task"]).target_definition,
        "position_summary": "earliest_position_with_best_true_Fx_rank_per_layer",
        "selected_query_position_by_layer": selected_positions,
        "selected_prompt_position_by_layer": [
            query_start + position for position in selected_positions
        ],
        "jlens_z": jlens_z,
        "jlens_rr": jlens_rr,
        "classification": {
            "group": classify_rank(best_rank),
            "intermediate_value": record["query"]["Fx"],
            "intermediate_catalog_index": target_index,
            "peak_reciprocal_rank": peak_rr,
            "best_vocabulary_rank": best_rank,
            "peak_layers": peak_layers,
            "first_peak_layer": peak_layers[0],
            "composition_rr_threshold": COMPOSITION_RR_THRESHOLD,
            "shortcut_rr_threshold": SHORTCUT_RR_THRESHOLD,
        },
    }
    return output


def _import_runtime() -> tuple[Any, Any, Any, Any]:
    """Import the official vendored J-Lens and model dependencies lazily."""

    if not (VENDORED_JLENS / "jlens" / "__init__.py").is_file():
        raise FileNotFoundError(f"missing official J-Lens checkout: {VENDORED_JLENS}")
    vendor_path = str(VENDORED_JLENS)
    if vendor_path not in sys.path:
        sys.path.insert(0, vendor_path)
    import jlens
    from transformers import AutoModelForCausalLM, AutoTokenizer

    return jlens, torch, AutoModelForCausalLM, AutoTokenizer


def main() -> None:
    """Load the pinned model and fitted lens, then stream one input slice."""

    args = parse_args()
    if min(args.max_seq_len, args.candidate_chunk_size, args.progress_every) <= 0:
        raise ValueError("sequence length, chunk size, and progress must be positive")

    task = get_task_spec(args.task).dataset_task
    task_directory = PROJECT_DIR / "results" / task
    input_path = args.input or task_directory / "logit_lens_evaluation.jsonl.gz"
    catalog_path = args.catalog_summary or task_directory / "baseline_summary.json"
    output_path = args.output or task_directory / "jlens_evaluation.jsonl.gz"
    summary_path = args.summary_output or task_directory / "jlens_summary.json"
    ensure_outputs((output_path, summary_path), args.overwrite)

    if not args.lens.is_file():
        raise FileNotFoundError(f"missing fitted J-Lens: {args.lens}")
    lens_sha256 = file_sha256(args.lens)
    if lens_sha256 != EXPECTED_LENS_SHA256:
        raise ValueError(f"unexpected fitted J-Lens SHA-256: {lens_sha256}")

    jlens, torch_module, model_class, tokenizer_class = _import_runtime()
    lens = jlens.JacobianLens.load(str(args.lens))
    source_layers = validate_loaded_lens(lens)
    tokenizer = tokenizer_class.from_pretrained(
        MODEL_ID,
        revision=STAGE_ONE_COMMIT,
        local_files_only=not args.allow_download,
    )
    model = model_class.from_pretrained(
        MODEL_ID,
        revision=STAGE_ONE_COMMIT,
        dtype=torch_module.bfloat16,
        device_map="auto",
        local_files_only=not args.allow_download,
    )
    model.eval()
    fx_catalog = load_fx_catalog(catalog_path, task=task, tokenizer=tokenizer)

    # Logit-Lens query positions were tokenized without forcing a fresh BOS.
    # Preserve that convention so both lenses inspect the same activation rows.
    adapter = jlens.from_hf(model, tokenizer, compile=False, force_bos=False)
    lens.jacobians = {
        layer: matrix.to(adapter.input_device)
        for layer, matrix in lens.jacobians.items()
    }

    counters = RunningSummary()
    with open_text(output_path, "wt") as output_handle:
        for record in read_correct_slice(
            input_path,
            task=task,
            start_index=args.start_index,
            num_records=args.num_records,
        ):
            validate_logit_lens_record(record)
            if record["logit_lens"]["paper_token_eligible"]:
                result = analyze_record(
                    lens,
                    adapter,
                    record,
                    fx_catalog,
                    source_layers=source_layers,
                    max_seq_len=args.max_seq_len,
                    candidate_chunk_size=args.candidate_chunk_size,
                )
            else:
                result = excluded_result(record)
            output_handle.write(json.dumps(result, ensure_ascii=False) + "\n")
            output_handle.flush()
            counters.add(result)
            if counters.input_records % args.progress_every == 0:
                print(f"Processed {counters.input_records} records", flush=True)

    summary = {
        "task": task,
        "model": MODEL_ID,
        "stage_one_revision": STAGE_ONE_REVISION,
        "model_commit": STAGE_ONE_COMMIT,
        "dtype": MODEL_DTYPE,
        "jlens_commit": JLENS_COMMIT,
        "lens": str(args.lens),
        "lens_sha256": lens_sha256,
        "lens_fit_prompts": int(lens.n_prompts),
        "input": str(input_path),
        "candidate_catalog_source": str(catalog_path),
        "output": str(output_path),
        "start_index": args.start_index,
        "requested_num_records": args.num_records,
        "max_seq_len": args.max_seq_len,
        "candidate_chunk_size": args.candidate_chunk_size,
        "Fx_catalog": fx_catalog,
        "rank_scope": "complete_vocabulary",
        "target_definition": get_task_spec(task).target_definition,
        "query_positions": "reused_from_generalized_logit_lens",
        "source_layers": list(source_layers),
        "processing_signature": "maximum_true_Fx_RR_over_query_positions_per_layer",
        "position_tie_break": "earliest_query_position",
        "composition_rr_threshold": COMPOSITION_RR_THRESHOLD,
        "shortcut_rr_threshold": SHORTCUT_RR_THRESHOLD,
        **counters.as_dict(),
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {key: value for key, value in summary.items() if key != "Fx_catalog"},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
