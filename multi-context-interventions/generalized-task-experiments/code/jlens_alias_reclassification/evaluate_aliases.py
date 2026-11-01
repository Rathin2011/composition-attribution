"""Re-evaluate J-Lens shortcut candidates using fixed aliases of ``Fx``.

This is a separate diagnostic; it never rewrites the original J-Lens output.
For each originally shortcut-classified prompt, the evaluator ranks the
canonical intermediate and its predeclared aliases against the complete
vocabulary at every original query position and fitted J-Lens layer.  The
alias-aware classification uses the best rank across those surface forms.

Only first-token ranks are used so that the result is directly comparable to
the existing Khandelwal--Pavlick-style classification.  Complete alias token
sequences and first-token collisions are retained in the output for auditing.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys
from typing import Any, Iterator, Mapping, Sequence

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
from evaluate_jlens import (
    DEFAULT_LENS,
    EXPECTED_LENS_SHA256,
    JLENS_COMMIT,
    VENDORED_JLENS,
    candidate_logits_and_ranks,
    file_sha256,
    validate_loaded_lens,
)
from evaluate_logit_lens import (
    COMPOSITION_RR_THRESHOLD,
    SHORTCUT_RR_THRESHOLD,
    classify_rank,
)
from tasks import get_task_spec


PROJECT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_ALIASES = Path(__file__).with_name("country_aliases.json")
SUPPORTED_TASKS = ("landmark-country-capital", "park-country-capital")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, choices=SUPPORTED_TASKS)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--aliases", type=Path, default=DEFAULT_ALIASES)
    parser.add_argument("--lens", type=Path, default=DEFAULT_LENS)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--summary-output", type=Path)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--num-records", type=int)
    parser.add_argument("--max-seq-len", type=int, default=512)
    parser.add_argument("--candidate-chunk-size", type=int, default=16)
    parser.add_argument("--progress-every", type=int, default=10)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--allow-download", action="store_true")
    return parser.parse_args()


def load_aliases(path: Path) -> tuple[dict[str, list[str]], Mapping[str, Any]]:
    """Load and strictly validate a fixed canonical-value-to-alias mapping."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, Mapping) or not isinstance(payload.get("aliases"), Mapping):
        raise ValueError("alias file must contain an aliases object")
    result: dict[str, list[str]] = {}
    for canonical, aliases in payload["aliases"].items():
        if not isinstance(canonical, str) or not canonical.strip():
            raise ValueError("canonical alias keys must be nonempty strings")
        if not isinstance(aliases, list) or not aliases:
            raise ValueError(f"aliases for {canonical!r} must be a nonempty list")
        if any(not isinstance(value, str) or not value.strip() for value in aliases):
            raise ValueError(f"aliases for {canonical!r} must be nonempty strings")
        if canonical.casefold() in {value.casefold() for value in aliases}:
            raise ValueError(f"canonical value repeated as alias: {canonical!r}")
        if len({value.casefold() for value in aliases}) != len(aliases):
            raise ValueError(f"duplicate aliases for {canonical!r}")
        result[canonical] = list(aliases)
    metadata = payload.get("metadata", {})
    if not isinstance(metadata, Mapping):
        raise ValueError("alias metadata must be an object")
    return result, metadata


def read_shortcut_slice(
    path: Path,
    *,
    task: str,
    start_index: int,
    num_records: int | None,
) -> Iterator[dict[str, Any]]:
    """Stream a slice indexed within originally shortcut-classified rows."""

    if start_index < 0 or (num_records is not None and num_records < 1):
        raise ValueError("start-index must be nonnegative and num-records positive")
    stop = None if num_records is None else start_index + num_records
    shortcut_index = 0
    for record in read_jsonl(path):
        if record.get("task") != task:
            raise ValueError("input contains a record for the wrong task")
        group = ((record.get("j_lens") or {}).get("classification") or {}).get("group")
        if group != "shortcut_candidate":
            continue
        if shortcut_index >= start_index and (stop is None or shortcut_index < stop):
            yield record
        shortcut_index += 1
        if stop is not None and shortcut_index >= stop:
            break


def surface_token_groups(
    tokenizer: Any,
    *,
    task: str,
    canonical: str,
    aliases: Sequence[str],
) -> list[dict[str, Any]]:
    """Tokenize surfaces and group those sharing the measured first token."""

    spec = get_task_spec(task)
    by_token: dict[int, dict[str, Any]] = {}
    for kind, surface in [("canonical", canonical), *[("alias", a) for a in aliases]]:
        token_ids = spec.token_ids(tokenizer, "Fx", surface)
        first = int(token_ids[0])
        group = by_token.setdefault(
            first,
            {
                "first_token_id": first,
                "first_token": tokenizer.decode([first]),
                "surface_forms": [],
            },
        )
        group["surface_forms"].append(
            {"surface": surface, "kind": kind, "token_ids": token_ids}
        )
    return list(by_token.values())


def _score_groups(
    ranks: torch.Tensor,
    groups: Sequence[Mapping[str, Any]],
    source_layers: Sequence[int],
) -> list[dict[str, Any]]:
    """Summarize each distinct first token over positions and layers."""

    output = []
    for candidate_index, group in enumerate(groups):
        candidate_ranks = ranks[:, :, candidate_index]
        best_rank = int(candidate_ranks.min().item())
        locations = []
        for position, layer_index in torch.nonzero(
            candidate_ranks == best_rank, as_tuple=False
        ).tolist():
            locations.append(
                {"query_position": int(position), "layer": int(source_layers[layer_index])}
            )
        output.append(
            {
                **dict(group),
                "best_vocabulary_rank": best_rank,
                "peak_reciprocal_rank": 1.0 / best_rank,
                "peak_locations": locations,
            }
        )
    return output


def analyze_shortcut_record(
    lens: Any,
    adapter: Any,
    tokenizer: Any,
    record: Mapping[str, Any],
    aliases: Sequence[str],
    *,
    source_layers: Sequence[int],
    max_seq_len: int,
    candidate_chunk_size: int,
) -> dict[str, Any]:
    """Rerun one shortcut prompt and classify the best canonical/alias rank."""

    measurement = record["j_lens"]
    classification = measurement["classification"]
    if classification["group"] != "shortcut_candidate":
        raise ValueError("alias analysis accepts only shortcut candidates")
    query_start = int(measurement["query_token_start"])
    num_positions = int(measurement["num_query_positions"])
    positions = list(range(query_start, query_start + num_positions))
    canonical = record["query"]["Fx"]
    groups = surface_token_groups(
        tokenizer, task=record["task"], canonical=canonical, aliases=aliases
    )

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
    _, ranks = candidate_logits_and_ranks(
        logits_by_layer,
        [int(group["first_token_id"]) for group in groups],
        source_layers,
        candidate_chunk_size=candidate_chunk_size,
    )
    scored = _score_groups(ranks, groups, source_layers)
    canonical_scores = [
        row
        for row in scored
        if any(surface["kind"] == "canonical" for surface in row["surface_forms"])
    ]
    if len(canonical_scores) != 1:
        raise RuntimeError("canonical surface must map to exactly one token group")
    rerun_rank = canonical_scores[0]["best_vocabulary_rank"]
    saved_rank = int(classification["best_vocabulary_rank"])
    rerun_canonical_group = classify_rank(rerun_rank)
    saved_group = classification["group"]

    best_rank = min(row["best_vocabulary_rank"] for row in scored)
    winning = [
        surface["surface"]
        for row in scored
        if row["best_vocabulary_rank"] == best_rank
        for surface in row["surface_forms"]
    ]
    new_group = classify_rank(best_rank)
    return {
        "prompt_instance_id": record.get("prompt_instance_id"),
        "query_index": record.get("query_index"),
        "context_variant": record.get("context_variant"),
        "task": record["task"],
        "query": dict(record["query"]),
        "original_classification": dict(classification),
        "alias_reclassification": {
            "scoring_rule": "best_full_vocabulary_first_token_rank_over_surfaces_layers_and_query_positions",
            "canonical_rerun_validation": {
                "saved_rank": saved_rank,
                "rerun_rank": rerun_rank,
                "rank_difference": rerun_rank - saved_rank,
                "exact_rank_match": rerun_rank == saved_rank,
                "saved_group": saved_group,
                "rerun_group": rerun_canonical_group,
                "group_match": rerun_canonical_group == saved_group,
            },
            "surface_token_groups": scored,
            "num_alternate_surface_forms": len(aliases),
            "num_distinct_first_tokens": len(groups),
            "best_vocabulary_rank": best_rank,
            "peak_reciprocal_rank": 1.0 / best_rank,
            "winning_surface_forms": winning,
            "group": new_group,
            "transition": f"shortcut_candidate->{new_group}",
        },
    }


def _import_runtime() -> tuple[Any, Any, Any]:
    if not (VENDORED_JLENS / "jlens" / "__init__.py").is_file():
        raise FileNotFoundError(f"missing official J-Lens checkout: {VENDORED_JLENS}")
    if str(VENDORED_JLENS) not in sys.path:
        sys.path.insert(0, str(VENDORED_JLENS))
    import jlens
    from transformers import AutoModelForCausalLM, AutoTokenizer

    return jlens, AutoModelForCausalLM, AutoTokenizer


def main() -> None:
    args = parse_args()
    if min(args.max_seq_len, args.candidate_chunk_size, args.progress_every) <= 0:
        raise ValueError("sequence length, chunk size, and progress must be positive")
    task_dir = PROJECT_DIR / "results" / args.task
    input_path = args.input or task_dir / "jlens_evaluation.jsonl.gz"
    output_dir = PROJECT_DIR / "results" / "jlens_alias_reclassification" / args.task
    output_path = args.output or output_dir / "alias_reclassification.jsonl.gz"
    summary_path = args.summary_output or output_dir / "alias_reclassification_summary.json"
    ensure_outputs((output_path, summary_path), args.overwrite)

    alias_map, alias_metadata = load_aliases(args.aliases)
    lens_sha256 = file_sha256(args.lens)
    if lens_sha256 != EXPECTED_LENS_SHA256:
        raise ValueError(f"unexpected fitted J-Lens SHA-256: {lens_sha256}")
    jlens, model_class, tokenizer_class = _import_runtime()
    lens = jlens.JacobianLens.load(str(args.lens))
    source_layers = validate_loaded_lens(lens)
    tokenizer = tokenizer_class.from_pretrained(
        MODEL_ID, revision=STAGE_ONE_COMMIT, local_files_only=not args.allow_download
    )
    model = model_class.from_pretrained(
        MODEL_ID,
        revision=STAGE_ONE_COMMIT,
        dtype=torch.bfloat16,
        device_map="auto",
        local_files_only=not args.allow_download,
    )
    model.eval()
    adapter = jlens.from_hf(model, tokenizer, compile=False, force_bos=False)
    lens.jacobians = {
        layer: matrix.to(adapter.input_device) for layer, matrix in lens.jacobians.items()
    }

    transitions: Counter[str] = Counter()
    canonical_rank_mismatches = 0
    canonical_group_mismatches = 0
    alternate_records = 0
    processed = 0
    with open_text(output_path, "wt") as handle:
        for record in read_shortcut_slice(
            input_path,
            task=args.task,
            start_index=args.start_index,
            num_records=args.num_records,
        ):
            aliases = alias_map.get(record["query"]["Fx"], [])
            result = analyze_shortcut_record(
                lens,
                adapter,
                tokenizer,
                record,
                aliases,
                source_layers=source_layers,
                max_seq_len=args.max_seq_len,
                candidate_chunk_size=args.candidate_chunk_size,
            )
            handle.write(json.dumps(result, ensure_ascii=False) + "\n")
            handle.flush()
            processed += 1
            alternate_records += int(bool(aliases))
            validation = result["alias_reclassification"]["canonical_rerun_validation"]
            canonical_rank_mismatches += int(not validation["exact_rank_match"])
            canonical_group_mismatches += int(not validation["group_match"])
            transitions[result["alias_reclassification"]["transition"]] += 1
            if processed % args.progress_every == 0:
                print(f"Processed {processed} shortcut records", flush=True)

    summary = {
        "task": args.task,
        "model": MODEL_ID,
        "stage_one_revision": STAGE_ONE_REVISION,
        "model_commit": STAGE_ONE_COMMIT,
        "dtype": MODEL_DTYPE,
        "jlens_commit": JLENS_COMMIT,
        "lens": str(args.lens),
        "lens_sha256": lens_sha256,
        "source_layers": list(source_layers),
        "input": str(input_path),
        "aliases": str(args.aliases),
        "alias_metadata": dict(alias_metadata),
        "output": str(output_path),
        "start_index_within_shortcuts": args.start_index,
        "requested_num_shortcut_records": args.num_records,
        "num_shortcut_records": processed,
        "num_records_with_alternate_aliases": alternate_records,
        "num_canonical_rerun_rank_mismatches": canonical_rank_mismatches,
        "num_canonical_rerun_group_mismatches": canonical_group_mismatches,
        "classification_transitions": dict(sorted(transitions.items())),
        "rank_scope": "complete_vocabulary",
        "surface_measurement": "task_aware_first_token",
        "composition_rr_threshold": COMPOSITION_RR_THRESHOLD,
        "shortcut_rr_threshold": SHORTCUT_RR_THRESHOLD,
    }
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
