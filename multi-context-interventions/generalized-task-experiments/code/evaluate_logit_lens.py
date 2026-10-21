"""Evaluate generalized Khandelwal--Pavlick Logit Lens measurements.

Input
-----
The task's ``correct_instances.jsonl.gz`` and ``baseline_summary.json``.
The latter supplies the complete ordered set of possible intermediate values.

Output
------
One compressed JSONL row per correct query-context instance.  Eligible rows
receive an ``llens_z`` matrix shaped ``[n_Fx, n_layers]`` and ``llens_rr`` for
the true intermediate.  At each layer, all values come from the same query
position: the earliest position with the true Fx's best vocabulary rank.

Rows excluded by the paper's first-token-overlap filter remain in the output
with an explicit reason, making every input row auditable.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Iterator, Literal, Mapping, Sequence

import torch

from evaluate_baseline import (
    MODEL_DTYPE,
    MODEL_ID,
    STAGE_ONE_COMMIT,
    STAGE_ONE_REVISION,
    ensure_outputs,
    open_text,
    read_jsonl,
)
from logit_lens import candidate_logits_and_ranks, capture_residual_stream
from tasks import TASKS, get_task_spec


NODES = ("x", "Fx", "GFx")
COMPOSITION_RR_THRESHOLD = 0.5
SHORTCUT_RR_THRESHOLD = 0.2
EvidenceGroup = Literal["compositional", "ambiguous", "shortcut_candidate"]
PROJECT_DIR = Path(__file__).resolve().parent.parent


@dataclass
class RunningSummary:
    """Count eligible, excluded, and classified output records."""

    input_records: int = 0
    eligible_records: int = 0
    excluded_records: int = 0
    groups: Counter[str] = field(default_factory=Counter)
    exclusions: Counter[str] = field(default_factory=Counter)

    def add(self, lens: Mapping[str, Any]) -> None:
        self.input_records += 1
        if lens["paper_token_eligible"]:
            self.eligible_records += 1
            self.groups[lens["classification"]["group"]] += 1
        else:
            self.excluded_records += 1
            self.exclusions[lens["paper_token_filter_reason"]] += 1

    def as_dict(self) -> dict[str, Any]:
        if self.input_records != self.eligible_records + self.excluded_records:
            raise RuntimeError("eligible and excluded counts do not partition input")
        return {
            "num_input_records": self.input_records,
            "num_paper_token_eligible": self.eligible_records,
            "num_paper_token_excluded": self.excluded_records,
            "paper_token_exclusion_reasons": dict(sorted(self.exclusions.items())),
            "classification_counts": {
                group: self.groups[group]
                for group in ("compositional", "ambiguous", "shortcut_candidate")
            },
        }


def parse_args() -> argparse.Namespace:
    """Parse one task-general full, smoke, or array-shard evaluation."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, choices=sorted(TASKS))
    parser.add_argument("--input", type=Path)
    parser.add_argument("--catalog-summary", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--summary-output", type=Path)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--num-records", type=int)
    parser.add_argument("--activation-chunk-size", type=int, default=32)
    parser.add_argument("--candidate-chunk-size", type=int, default=16)
    parser.add_argument("--progress-every", type=int, default=10)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def read_correct_slice(
    path: Path,
    *,
    task: str,
    start_index: int = 0,
    num_records: int | None = None,
) -> Iterator[dict[str, Any]]:
    """Yield a validated contiguous slice of exact-correct instances."""

    if start_index < 0:
        raise ValueError("start_index must be non-negative")
    if num_records is not None and num_records <= 0:
        raise ValueError("num_records must be positive when supplied")
    selected = 0
    seen: set[str] = set()
    for index, record in enumerate(read_jsonl(path)):
        if index < start_index:
            continue
        if num_records is not None and selected >= num_records:
            break
        if record.get("task") != task:
            raise ValueError(f"row {index + 1} does not belong to task {task!r}")
        prompt_id = record.get("prompt_instance_id")
        if not isinstance(prompt_id, str) or not prompt_id:
            raise ValueError(f"row {index + 1} has invalid prompt_instance_id")
        if prompt_id in seen:
            raise ValueError(f"duplicate prompt_instance_id: {prompt_id!r}")
        seen.add(prompt_id)
        if not isinstance(record.get("prompt"), str):
            raise ValueError(f"row {index + 1} has invalid prompt")
        query = record.get("query")
        if not isinstance(query, Mapping) or any(
            not isinstance(query.get(node), str) for node in NODES
        ):
            raise ValueError(f"row {index + 1} has invalid query")
        evaluation = record.get("evaluation")
        if not isinstance(evaluation, Mapping) or evaluation.get("exact_match") is not True:
            raise ValueError(f"row {index + 1} is not exact-correct")
        selected += 1
        yield record


def leading_space_token_ids(tokenizer: Any, value: str) -> list[int]:
    """Tokenize a task value as a continuation immediately after ``A:``."""

    token_ids = tokenizer.encode(f" {value}", add_special_tokens=False)
    if not token_ids:
        raise ValueError(f"task value has no tokens: {value!r}")
    return [int(token_id) for token_id in token_ids]


def node_token_info(tokenizer: Any, query: Mapping[str, str], *, task: str) -> dict[str, dict]:
    """Record complete and first-token encodings for x, Fx, and GFx."""

    output = {}
    for node in NODES:
        token_ids = get_task_spec(task).token_ids(tokenizer, node, query[node])
        output[node] = {
            "value": query[node],
            "token_ids": token_ids,
            "num_tokens": len(token_ids),
            "first_token_id": token_ids[0],
            "first_token": tokenizer.decode([token_ids[0]]),
        }
    return output


def paper_token_filter_reason(token_info: Mapping[str, Mapping[str, Any]]) -> str | None:
    """Reproduce the paper's first-token identity/containment exclusions."""

    first_ids = [int(token_info[node]["first_token_id"]) for node in NODES]
    if len(first_ids) != len(set(first_ids)):
        return "node_first_tokens_overlap"
    non_x = {int(token_info[node]["first_token_id"]) for node in ("Fx", "GFx")}
    if non_x & set(token_info["x"]["token_ids"]):
        return "target_first_token_occurs_inside_x"
    return None


def first_query_token_index(tokenizer: Any, prompt: str, x: str) -> int:
    """Locate the first token covering the final ``x + newline + A:`` suffix."""

    trailing_space = " " if prompt.endswith("A: ") else ""
    expected = f"Q: {x}\nA:{trailing_space}"
    if not prompt.endswith(expected):
        raise ValueError(f"prompt does not end with {expected!r}")
    characters_remaining = len(f"{x}\nA:{trailing_space}")
    token_ids = tokenizer.encode(prompt, add_special_tokens=False)
    for token_index in range(len(token_ids) - 1, -1, -1):
        characters_remaining -= len(tokenizer.decode(token_ids[token_index]))
        if characters_remaining <= 0:
            return token_index
    raise ValueError("could not locate final query token boundary")


def load_fx_catalog(
    summary_path: Path, *, task: str, tokenizer: Any
) -> list[dict[str, Any]]:
    """Load and verify every possible Fx value in its canonical row order."""

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    if summary.get("task") != task:
        raise ValueError("baseline summary task does not match evaluation task")
    catalog = summary.get("candidate_catalog", {}).get("Fx")
    if not isinstance(catalog, list) or not catalog:
        raise ValueError("baseline summary lacks a nonempty Fx catalog")
    output = []
    values: set[str] = set()
    for row in catalog:
        if not isinstance(row, Mapping):
            raise ValueError("Fx catalog entries must be objects")
        value = row.get("value")
        token_ids = row.get("token_ids")
        if not isinstance(value, str) or value in values:
            raise ValueError("Fx catalog values must be unique strings")
        expected_ids = get_task_spec(task).token_ids(tokenizer, "Fx", value)
        if token_ids != expected_ids:
            raise ValueError(f"saved tokenizer IDs changed for Fx={value!r}")
        values.add(value)
        output.append({"value": value, "token_ids": expected_ids})
    return output


def classify_reciprocal_rank(value: float) -> EvidenceGroup:
    """Map peak true-Fx reciprocal rank to the fixed evidence bands."""

    if not 0.0 <= value <= 1.0:
        raise ValueError("reciprocal rank must be between zero and one")
    if value >= COMPOSITION_RR_THRESHOLD:
        return "compositional"
    if value <= SHORTCUT_RR_THRESHOLD:
        return "shortcut_candidate"
    return "ambiguous"


def classify_rank(rank: int) -> EvidenceGroup:
    """Classify an exact one-based vocabulary rank without float boundaries."""

    if not isinstance(rank, int) or isinstance(rank, bool) or rank < 1:
        raise ValueError("rank must be a positive integer")
    if rank <= 2:  # 1 / rank >= 0.5
        return "compositional"
    if rank >= 5:  # 1 / rank <= 0.2
        return "shortcut_candidate"
    return "ambiguous"


def select_best_position_values(
    candidate_logits: torch.Tensor,
    candidate_ranks: torch.Tensor,
    *,
    target_index: int,
) -> tuple[list[list[float]], list[float], list[int]]:
    """Collapse query positions without mixing positions within a layer.

    For every layer, choose the earliest position with the smallest (best)
    full-vocabulary rank for the true Fx.  Return all candidate logits at those
    same positions as ``[K,L]``, the true Fx RR as ``[L]``, and chosen relative
    positions as ``[L]``.
    """

    if candidate_logits.ndim != 3 or candidate_ranks.shape != candidate_logits.shape:
        raise ValueError("candidate tensors must share shape [P,L,K]")
    if not 0 <= target_index < candidate_logits.shape[2]:
        raise ValueError("target_index is outside the candidate axis")
    target_ranks = candidate_ranks[:, :, target_index]
    best_positions = target_ranks.argmin(dim=0)
    layer_indices = torch.arange(candidate_logits.shape[1])
    selected_logits = candidate_logits[best_positions, layer_indices, :].T.float()
    selected_ranks = target_ranks[best_positions, layer_indices].long()
    return (
        selected_logits.tolist(),
        [1.0 / int(rank) for rank in selected_ranks.tolist()],
        [int(value) for value in best_positions.tolist()],
    )


def analyze_record(
    model: Any,
    tokenizer: Any,
    record: Mapping[str, Any],
    token_info: Mapping[str, Mapping[str, Any]],
    fx_catalog: Sequence[Mapping[str, Any]],
    *,
    activation_chunk_size: int,
    candidate_chunk_size: int,
) -> dict[str, Any]:
    """Run activation capture, projection, position selection, and classification."""

    prompt = record["prompt"]
    query = record["query"]
    get_task_spec(record["task"]).validate_prompt(prompt, query["x"])
    query_start = first_query_token_index(tokenizer, prompt, query["x"])
    model_inputs = tokenizer(
        [prompt], return_tensors="pt", return_token_type_ids=False
    )
    input_device = model.get_input_embeddings().weight.device
    model_inputs = {name: value.to(input_device) for name, value in model_inputs.items()}
    residual = capture_residual_stream(
        model, model_inputs, position_slice=slice(query_start, None)
    )

    candidate_values = [row["value"] for row in fx_catalog]
    try:
        target_index = candidate_values.index(query["Fx"])
    except ValueError as error:
        raise ValueError(f"true Fx is absent from candidate catalog: {query['Fx']!r}") from error
    candidate_logits, candidate_ranks = candidate_logits_and_ranks(
        model,
        residual,
        [int(row["token_ids"][0]) for row in fx_catalog],
        activation_chunk_size=activation_chunk_size,
        candidate_chunk_size=candidate_chunk_size,
    )
    llens_z, llens_rr, selected_positions = select_best_position_values(
        candidate_logits, candidate_ranks, target_index=target_index
    )
    best_vocabulary_rank = int(
        candidate_ranks[:, :, target_index].min().item()
    )
    peak_rr = 1.0 / best_vocabulary_rank
    peak_layers = [index for index, value in enumerate(llens_rr) if value == peak_rr]

    output = dict(record)
    output["logit_lens"] = {
        "paper_token_eligible": True,
        "paper_token_filter_reason": None,
        "query_token_start": query_start,
        "num_query_positions": int(residual.shape[0]),
        "num_layers": int(residual.shape[1]),
        "layer_index_definition": "post_decoder_block_zero_based",
        "rank_scope": "complete_vocabulary",
        "target_definition": get_task_spec(record["task"]).target_definition,
        "position_summary": "earliest_position_with_best_true_Fx_rank_per_layer",
        "selected_query_position_by_layer": selected_positions,
        "selected_prompt_position_by_layer": [
            query_start + position for position in selected_positions
        ],
        "llens_z": llens_z,
        "llens_rr": llens_rr,
        "classification": {
            "group": classify_rank(best_vocabulary_rank),
            "intermediate_value": query["Fx"],
            "intermediate_catalog_index": target_index,
            "peak_reciprocal_rank": peak_rr,
            # Keep the exact integer rank instead of reconstructing it from a
            # floating-point reciprocal rank.
            "best_vocabulary_rank": best_vocabulary_rank,
            "peak_layers": peak_layers,
            "first_peak_layer": peak_layers[0],
            "composition_rr_threshold": COMPOSITION_RR_THRESHOLD,
            "shortcut_rr_threshold": SHORTCUT_RR_THRESHOLD,
        },
        "node_token_info": dict(token_info),
    }
    return output


def excluded_result(
    record: Mapping[str, Any],
    token_info: Mapping[str, Mapping[str, Any]],
    reason: str,
) -> dict[str, Any]:
    """Preserve a paper-filtered row without running a model forward pass."""

    output = dict(record)
    output["logit_lens"] = {
        "paper_token_eligible": False,
        "paper_token_filter_reason": reason,
        "classification": None,
        "node_token_info": dict(token_info),
        "llens_z": None,
        "llens_rr": None,
    }
    return output


def main() -> None:
    """Load pinned OLMo, stream one input slice, and save compressed results."""

    args = parse_args()
    if min(
        args.activation_chunk_size,
        args.candidate_chunk_size,
        args.progress_every,
    ) <= 0:
        raise ValueError("chunk sizes and progress-every must be positive")
    task = get_task_spec(args.task).dataset_task
    task_directory = PROJECT_DIR / "results" / task
    input_path = args.input or task_directory / "correct_instances.jsonl.gz"
    catalog_path = args.catalog_summary or task_directory / "baseline_summary.json"
    output_path = args.output or task_directory / "logit_lens_evaluation.jsonl.gz"
    summary_path = args.summary_output or task_directory / "logit_lens_summary.json"
    ensure_outputs((output_path, summary_path), args.overwrite)

    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=STAGE_ONE_COMMIT)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        revision=STAGE_ONE_COMMIT,
        device_map="auto",
        dtype=torch.bfloat16,
    )
    model.eval()
    fx_catalog = load_fx_catalog(catalog_path, task=task, tokenizer=tokenizer)
    counters = RunningSummary()

    with open_text(output_path, "wt") as output_handle:
        for record in read_correct_slice(
            input_path,
            task=task,
            start_index=args.start_index,
            num_records=args.num_records,
        ):
            get_task_spec(task).validate_prompt(record["prompt"], record["query"]["x"])
            token_info = node_token_info(tokenizer, record["query"], task=task)
            reason = paper_token_filter_reason(token_info)
            if reason is None:
                result = analyze_record(
                    model,
                    tokenizer,
                    record,
                    token_info,
                    fx_catalog,
                    activation_chunk_size=args.activation_chunk_size,
                    candidate_chunk_size=args.candidate_chunk_size,
                )
            else:
                result = excluded_result(record, token_info, reason)
            output_handle.write(json.dumps(result, ensure_ascii=False) + "\n")
            output_handle.flush()
            counters.add(result["logit_lens"])
            if counters.input_records % args.progress_every == 0:
                print(f"Processed {counters.input_records} records", flush=True)

    summary = {
        "task": task,
        "model": MODEL_ID,
        "stage_one_revision": STAGE_ONE_REVISION,
        "model_commit": STAGE_ONE_COMMIT,
        "dtype": MODEL_DTYPE,
        "input": str(input_path),
        "candidate_catalog_source": str(catalog_path),
        "output": str(output_path),
        "start_index": args.start_index,
        "requested_num_records": args.num_records,
        "activation_chunk_size": args.activation_chunk_size,
        "candidate_chunk_size": args.candidate_chunk_size,
        "Fx_catalog": fx_catalog,
        "rank_scope": "complete_vocabulary",
        "target_definition": get_task_spec(task).target_definition,
        "query_positions": "tokens_covering_x_plus_newline_A_colon",
        "layers": "all_post_decoder_block_outputs",
        "processing_signature": "maximum_true_Fx_RR_over_query_positions_per_layer",
        "position_tie_break": "earliest_query_position",
        "composition_rr_threshold": COMPOSITION_RR_THRESHOLD,
        "shortcut_rr_threshold": SHORTCUT_RR_THRESHOLD,
        **counters.as_dict(),
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({key: value for key, value in summary.items() if key != "Fx_catalog"}, indent=2))


if __name__ == "__main__":
    main()
