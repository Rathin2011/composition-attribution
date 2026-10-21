"""Validate and merge task-general Logit Lens result shards.

The canonical ``correct_instances.jsonl.gz`` file defines the required row
order.  Every shard is checked against that source, and all aggregate counts
are recomputed from the result records rather than copied from summaries.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from evaluate_baseline import open_text, read_jsonl
from evaluate_logit_lens import RunningSummary
from tasks import TASKS, get_task_spec


PROJECT_DIR = Path(__file__).resolve().parent.parent
GROUPS = ("compositional", "ambiguous", "shortcut_candidate")
EXCLUSION_REASONS = {
    "node_first_tokens_overlap",
    "target_first_token_occurs_inside_x",
}
SHARED_SUMMARY_KEYS = (
    "task",
    "model",
    "stage_one_revision",
    "model_commit",
    "dtype",
    "input",
    "candidate_catalog_source",
    "activation_chunk_size",
    "candidate_chunk_size",
    "Fx_catalog",
    "rank_scope",
    "target_definition",
    "query_positions",
    "layers",
    "processing_signature",
    "position_tie_break",
    "composition_rr_threshold",
    "shortcut_rr_threshold",
)


def companion_summary(shard: Path) -> Path:
    """Return the summary filename paired with a JSONL or JSONL.GZ shard."""

    for ending in (".jsonl.gz", ".jsonl"):
        if shard.name.endswith(ending):
            return shard.with_name(f"{shard.name[:-len(ending)]}_summary.json")
    raise ValueError(f"unsupported shard filename: {shard}")


def ordered_shards(
    shard_directory: Path,
) -> tuple[list[Path], list[dict[str, Any]], list[Path]]:
    """Find shards and order them by the start index recorded in summaries."""

    shards = list(shard_directory.glob("logit_lens_shard_*.jsonl"))
    shards.extend(shard_directory.glob("logit_lens_shard_*.jsonl.gz"))
    if not shards:
        raise ValueError(f"no Logit Lens shards found in {shard_directory}")
    pairs = []
    for shard in shards:
        summary_path = companion_summary(shard)
        if not summary_path.exists():
            raise FileNotFoundError(f"missing summary for {shard}: {summary_path}")
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        if not isinstance(summary, dict):
            raise ValueError(f"summary must be a JSON object: {summary_path}")
        pairs.append((int(summary["start_index"]), shard, summary, summary_path))
    pairs.sort(key=lambda value: value[0])
    return (
        [value[1] for value in pairs],
        [value[2] for value in pairs],
        [value[3] for value in pairs],
    )


def validate_summaries(
    shard_paths: Sequence[Path],
    summaries: Sequence[Mapping[str, Any]],
    *,
    task: str,
) -> tuple[int, int]:
    """Verify common provenance and exact contiguous shard boundaries.

    Returns ``(total_records, n_Fx)`` for later record-level validation.
    """

    if not summaries:
        raise ValueError("at least one shard summary is required")
    reference = summaries[0]
    if reference.get("task") != task:
        raise ValueError(f"shard task {reference.get('task')!r} does not match {task!r}")
    fx_catalog = reference.get("Fx_catalog")
    if not isinstance(fx_catalog, list) or not fx_catalog:
        raise ValueError("Fx_catalog must be a nonempty list")

    expected_start = 0
    for shard, summary in zip(shard_paths, summaries, strict=True):
        for key in SHARED_SUMMARY_KEYS:
            if summary.get(key) != reference.get(key):
                raise ValueError(f"shard summaries disagree on {key!r}")
        if summary.get("output") != str(shard):
            raise ValueError(f"summary output path does not match {shard}")
        if int(summary["start_index"]) != expected_start:
            raise ValueError(
                f"noncontiguous shard start: expected {expected_start}, "
                f"got {summary['start_index']}"
            )
        completed = int(summary["num_input_records"])
        requested = summary.get("requested_num_records")
        if requested is None or int(requested) != completed or completed <= 0:
            raise ValueError(f"incomplete shard reported by {shard}")
        expected_start += completed
    return expected_start, len(fx_catalog)


def _numeric_vector(value: Any, length: int, name: str) -> None:
    """Require a numeric list with one exact expected length."""

    if not isinstance(value, list) or len(value) != length:
        raise ValueError(f"{name} must have length {length}")
    if any(not isinstance(item, (int, float)) for item in value):
        raise ValueError(f"{name} must contain only numbers")


def validate_lens_result(record: Mapping[str, Any], *, n_fx: int) -> None:
    """Validate one eligible or paper-filtered Logit Lens result."""

    prompt_id = record.get("prompt_instance_id")
    evaluation = record.get("evaluation")
    if not isinstance(evaluation, Mapping) or evaluation.get("exact_match") is not True:
        raise ValueError(f"result {prompt_id!r} is not exact-correct")
    lens = record.get("logit_lens")
    if not isinstance(lens, Mapping):
        raise ValueError(f"result {prompt_id!r} lacks logit_lens")
    eligible = lens.get("paper_token_eligible")
    if not isinstance(eligible, bool):
        raise ValueError(f"result {prompt_id!r} has invalid eligibility")

    if not eligible:
        if lens.get("paper_token_filter_reason") not in EXCLUSION_REASONS:
            raise ValueError(f"result {prompt_id!r} has invalid exclusion reason")
        if lens.get("classification") is not None:
            raise ValueError(f"excluded result {prompt_id!r} has classification")
        if lens.get("llens_z") is not None or lens.get("llens_rr") is not None:
            raise ValueError(f"excluded result {prompt_id!r} has lens values")
        return

    if lens.get("paper_token_filter_reason") is not None:
        raise ValueError(f"eligible result {prompt_id!r} has exclusion reason")
    num_layers = lens.get("num_layers")
    num_positions = lens.get("num_query_positions")
    if not isinstance(num_layers, int) or num_layers <= 0:
        raise ValueError(f"result {prompt_id!r} has invalid num_layers")
    if not isinstance(num_positions, int) or num_positions <= 0:
        raise ValueError(f"result {prompt_id!r} has invalid query positions")

    z = lens.get("llens_z")
    if not isinstance(z, list) or len(z) != n_fx:
        raise ValueError(f"llens_z for {prompt_id!r} must have n_Fx={n_fx} rows")
    for row in z:
        _numeric_vector(row, num_layers, f"llens_z row for {prompt_id!r}")
    rr = lens.get("llens_rr")
    _numeric_vector(rr, num_layers, f"llens_rr for {prompt_id!r}")
    if any(not 0.0 < float(value) <= 1.0 for value in rr):
        raise ValueError(f"llens_rr for {prompt_id!r} is outside (0, 1]")

    classification = lens.get("classification")
    if not isinstance(classification, Mapping) or classification.get("group") not in GROUPS:
        raise ValueError(f"result {prompt_id!r} has invalid classification")
    if float(classification.get("peak_reciprocal_rank", -1)) != max(rr):
        raise ValueError(f"result {prompt_id!r} peak RR disagrees with llens_rr")

    relative = lens.get("selected_query_position_by_layer")
    absolute = lens.get("selected_prompt_position_by_layer")
    _numeric_vector(relative, num_layers, f"selected query positions for {prompt_id!r}")
    _numeric_vector(absolute, num_layers, f"selected prompt positions for {prompt_id!r}")
    query_start = lens.get("query_token_start")
    if not isinstance(query_start, int):
        raise ValueError(f"result {prompt_id!r} has invalid query_token_start")
    for query_position, prompt_position in zip(relative, absolute, strict=True):
        if not isinstance(query_position, int) or not 0 <= query_position < num_positions:
            raise ValueError(f"result {prompt_id!r} has invalid selected position")
        if prompt_position != query_start + query_position:
            raise ValueError(f"result {prompt_id!r} has inconsistent prompt position")


def expected_aggregate(summaries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Sum shard-summary counts for comparison with per-record recomputation."""

    groups: Counter[str] = Counter()
    exclusions: Counter[str] = Counter()
    total = eligible = excluded = 0
    for summary in summaries:
        total += int(summary["num_input_records"])
        eligible += int(summary["num_paper_token_eligible"])
        excluded += int(summary["num_paper_token_excluded"])
        groups.update(summary["classification_counts"])
        exclusions.update(summary["paper_token_exclusion_reasons"])
    return {
        "num_input_records": total,
        "num_paper_token_eligible": eligible,
        "num_paper_token_excluded": excluded,
        "paper_token_exclusion_reasons": dict(sorted(exclusions.items())),
        "classification_counts": {group: groups[group] for group in GROUPS},
    }


def merge_logit_lens_shards(
    *,
    task: str,
    source: Path,
    shard_directory: Path,
    output: Path,
    summary_output: Path,
    overwrite: bool = False,
) -> dict[str, Any]:
    """Validate, atomically merge, and summarize one task's lens shards."""

    existing = [path for path in (output, summary_output) if path.exists()]
    if existing and not overwrite:
        raise FileExistsError(f"outputs already exist; use --overwrite: {existing}")
    output.parent.mkdir(parents=True, exist_ok=True)
    summary_output.parent.mkdir(parents=True, exist_ok=True)

    shards, summaries, summary_paths = ordered_shards(shard_directory)
    total_records, n_fx = validate_summaries(shards, summaries, task=task)
    source_rows = read_jsonl(source)
    seen: set[str] = set()
    counters = RunningSummary()
    temporary = output.with_name(f"{output.stem}.tmp{output.suffix}")

    try:
        with open_text(temporary, "wt") as handle:
            for shard in shards:
                for result in read_jsonl(shard):
                    try:
                        expected = next(source_rows)
                    except StopIteration as error:
                        raise ValueError("shards contain more rows than source") from error
                    prompt_id = result.get("prompt_instance_id")
                    if not isinstance(prompt_id, str) or prompt_id in seen:
                        raise ValueError(f"invalid or duplicate prompt_instance_id: {prompt_id!r}")
                    seen.add(prompt_id)
                    for field, expected_value in expected.items():
                        if result.get(field) != expected_value:
                            raise ValueError(f"{field} mismatch for {prompt_id!r}")
                    validate_lens_result(result, n_fx=n_fx)
                    counters.add(result["logit_lens"])
                    handle.write(json.dumps(result, ensure_ascii=False) + "\n")

        try:
            missing = next(source_rows)
        except StopIteration:
            missing = None
        if missing is not None:
            raise ValueError(
                "shards contain fewer rows than source; first missing ID is "
                f"{missing.get('prompt_instance_id')!r}"
            )
        if len(seen) != total_records:
            raise ValueError(f"expected {total_records} unique records, found {len(seen)}")
        counts = counters.as_dict()
        if counts != expected_aggregate(summaries):
            raise ValueError("per-record aggregate counts disagree with shard summaries")
        temporary.replace(output)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise

    reference = summaries[0]
    summary = {
        **{key: reference[key] for key in SHARED_SUMMARY_KEYS},
        "source": str(source),
        "input_shards": [str(path) for path in shards],
        "input_shard_summaries": [str(path) for path in summary_paths],
        "output": str(output),
        "num_unique_prompt_instance_ids": len(seen),
        **counts,
    }
    summary_output.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def parse_args() -> argparse.Namespace:
    """Parse task and optional path overrides."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, choices=sorted(TASKS))
    parser.add_argument("--source", type=Path)
    parser.add_argument("--shard-directory", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--summary-output", type=Path)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    task = get_task_spec(args.task).dataset_task
    task_directory = PROJECT_DIR / "results" / task
    summary = merge_logit_lens_shards(
        task=task,
        source=args.source or task_directory / "correct_instances.jsonl.gz",
        shard_directory=(
            args.shard_directory or task_directory / "logit_lens_shards"
        ),
        output=args.output or task_directory / "logit_lens_evaluation.jsonl.gz",
        summary_output=args.summary_output or task_directory / "logit_lens_summary.json",
        overwrite=args.overwrite,
    )
    print(json.dumps({key: value for key, value in summary.items() if key != "Fx_catalog"}, indent=2))


if __name__ == "__main__":
    main()
