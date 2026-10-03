"""Validate and merge the full multi-context Logit Lens shard outputs.

Inputs
======
* The canonical exact-correct input JSONL, used as the authoritative ordering.
* Five ordered ``logit_lens_full_shard_XX.jsonl`` result files.
* Their automatically inferred ``*_summary.json`` companion files.

Outputs
=======
* ``logit_lens_full.jsonl``: every result in the exact order of the canonical
  input, with no missing or duplicate prompt-instance IDs.
* ``logit_lens_full_summary.json``: recomputed eligible/excluded and evidence-
  group counts plus shared model and measurement provenance.

The program does not trust concatenation alone. It validates shared shard
parameters, contiguous shard boundaries, each shard's reported row count,
record identity and prompt text against the source, and the internal
eligible/excluded classification schema. All aggregate counts are recomputed
from per-record outputs and compared with the shard summaries.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterator, Sequence

from evaluate_logit_lens import RunningSummary


PROJECT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = PROJECT_DIR / "results" / "correct_query_contexts.jsonl"
DEFAULT_SHARDS = tuple(
    PROJECT_DIR / "results" / f"logit_lens_full_shard_{index:02d}.jsonl"
    for index in range(1, 6)
)
DEFAULT_OUTPUT = PROJECT_DIR / "results" / "logit_lens_full.jsonl"
DEFAULT_SUMMARY = PROJECT_DIR / "results" / "logit_lens_full_summary.json"
EXPECTED_RECORDS = 5_491

# Every shard must agree on these methodological settings. Shard-specific
# paths, row offsets, and counts are intentionally checked separately.
SHARED_SUMMARY_KEYS = (
    "model",
    "stage_one_revision",
    "model_commit",
    "dtype",
    "reference_code_commit",
    "input",
    "chunk_size",
    "nodes",
    "intermediate_node",
    "rank_scope",
    "target_definition",
    "query_positions",
    "layers",
    "processing_signature",
    "overall_evidence",
    "composition_rr_threshold",
    "shortcut_rr_threshold",
)


def parse_args() -> argparse.Namespace:
    """Read canonical input, ordered shards, outputs, and overwrite permission."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--shards", type=Path, nargs="+", default=DEFAULT_SHARDS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--expected-records", type=int, default=EXPECTED_RECORDS)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def read_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    """Yield nonempty JSON objects from ``path`` with source-aware errors."""

    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number} is not a JSON object")
            yield value


def validate_destinations(paths: Sequence[Path], *, overwrite: bool) -> None:
    """Protect existing final artifacts and create missing parent directories."""

    existing = [str(path) for path in paths if path.exists()]
    if existing and not overwrite:
        raise FileExistsError(
            "outputs already exist; pass --overwrite: " + ", ".join(existing)
        )
    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)


def companion_summary_path(shard_path: Path) -> Path:
    """Return ``foo_summary.json`` for a shard named ``foo.jsonl``."""

    return shard_path.with_name(f"{shard_path.stem}_summary.json")


def load_and_validate_shard_summaries(
    shard_paths: Sequence[Path],
) -> tuple[list[Path], list[dict[str, Any]]]:
    """Load companion summaries and validate provenance and row boundaries.

    Input:
        Ordered JSONL shard paths.
    Output:
        Ordered companion-summary paths and decoded summary dictionaries.
    Role:
        Detects mixing results from different checkpoints, definitions, or
        noncontiguous array tasks before the large files are merged.
    """

    if not shard_paths:
        raise ValueError("at least one shard is required")
    summary_paths = [companion_summary_path(path) for path in shard_paths]
    summaries = [
        json.loads(path.read_text(encoding="utf-8")) for path in summary_paths
    ]
    if not all(isinstance(summary, dict) for summary in summaries):
        raise ValueError("each shard summary must be a JSON object")

    reference = summaries[0]
    expected_start = 0
    for shard_path, summary in zip(shard_paths, summaries, strict=True):
        for key in SHARED_SUMMARY_KEYS:
            if summary.get(key) != reference.get(key):
                raise ValueError(f"shard summaries disagree on {key!r}")
        if summary.get("output") != str(shard_path):
            raise ValueError(f"summary output path does not match {shard_path}")
        if summary.get("start_index") != expected_start:
            raise ValueError(
                f"noncontiguous shard start: expected {expected_start}, "
                f"got {summary.get('start_index')}"
            )
        shard_count = summary.get("num_input_records")
        if not isinstance(shard_count, int) or shard_count <= 0:
            raise ValueError(f"invalid row count in summary for {shard_path}")
        requested = summary.get("requested_num_records")
        if not isinstance(requested, int) or shard_count > requested:
            raise ValueError(f"shard count exceeds requested rows for {shard_path}")
        expected_start += shard_count
    return summary_paths, summaries


def validate_lens_result(record: dict[str, Any], prompt_id: str) -> None:
    """Require one result to have a consistent eligible/excluded lens schema."""

    evaluation = record.get("evaluation")
    if not isinstance(evaluation, dict) or evaluation.get("exact_match") is not True:
        raise ValueError(f"result {prompt_id!r} is not exact-correct")
    lens = record.get("logit_lens")
    if not isinstance(lens, dict):
        raise ValueError(f"result {prompt_id!r} has no logit_lens object")
    eligible = lens.get("paper_token_eligible")
    if not isinstance(eligible, bool):
        raise ValueError(f"result {prompt_id!r} has invalid eligibility")

    if eligible:
        classification = lens.get("classification")
        evidence = lens.get("node_evidence")
        if not isinstance(classification, dict):
            raise ValueError(f"eligible result {prompt_id!r} lacks classification")
        if classification.get("group") not in {
            "compositional",
            "ambiguous",
            "shortcut_candidate",
        }:
            raise ValueError(f"result {prompt_id!r} has invalid evidence group")
        if not isinstance(evidence, dict) or set(evidence) != {"x", "Fx", "GFx"}:
            raise ValueError(f"eligible result {prompt_id!r} lacks node evidence")
        if lens.get("paper_token_filter_reason") is not None:
            raise ValueError(f"eligible result {prompt_id!r} has exclusion reason")
    else:
        if lens.get("paper_token_filter_reason") not in {
            "node_first_tokens_overlap",
            "target_first_token_occurs_inside_x",
        }:
            raise ValueError(f"excluded result {prompt_id!r} has invalid reason")
        if lens.get("classification") is not None or lens.get("node_evidence") is not None:
            raise ValueError(f"excluded result {prompt_id!r} contains lens analysis")


def recomputed_counts_match_shard_summaries(
    recomputed: dict[str, Any], summaries: Sequence[dict[str, Any]]
) -> None:
    """Compare per-record aggregate counts with the sum of shard summaries."""

    expected_groups: Counter[str] = Counter()
    expected_exclusions: Counter[str] = Counter()
    expected_input = 0
    expected_eligible = 0
    expected_excluded = 0
    for summary in summaries:
        expected_input += int(summary["num_input_records"])
        expected_eligible += int(summary["num_paper_token_eligible"])
        expected_excluded += int(summary["num_paper_token_excluded"])
        expected_groups.update(summary["classification_counts"])
        expected_exclusions.update(summary["paper_token_exclusion_reasons"])

    comparisons = {
        "num_input_records": expected_input,
        "num_paper_token_eligible": expected_eligible,
        "num_paper_token_excluded": expected_excluded,
        "classification_counts": {
            group: expected_groups[group]
            for group in ("compositional", "ambiguous", "shortcut_candidate")
        },
        "paper_token_exclusion_reasons": dict(sorted(expected_exclusions.items())),
    }
    for key, expected in comparisons.items():
        if recomputed[key] != expected:
            raise ValueError(
                f"per-record {key} does not match shard summaries: "
                f"{recomputed[key]!r} != {expected!r}"
            )


def merge_records(
    source_path: Path,
    shard_paths: Sequence[Path],
    output_path: Path,
    *,
    expected_records: int | None,
) -> dict[str, Any]:
    """Merge shards while checking every result against the canonical source.

    Inputs:
        Canonical source, ordered result shards, output path, and optional exact
        expected count.
    Output:
        Counts recomputed through ``RunningSummary`` plus unique-ID count.
    Role:
        This is the core integrity check: it rejects missing, duplicated,
        reordered, or prompt-mismatched results rather than silently merging.
    """

    source_iterator = read_jsonl(source_path)
    seen_ids: set[str] = set()
    counters = RunningSummary()

    with output_path.open("w", encoding="utf-8") as output_handle:
        for shard_path in shard_paths:
            for result in read_jsonl(shard_path):
                try:
                    source = next(source_iterator)
                except StopIteration as error:
                    raise ValueError("shards contain more rows than source") from error

                prompt_id = result.get("prompt_instance_id")
                if not isinstance(prompt_id, str):
                    raise ValueError("result has invalid prompt_instance_id")
                if prompt_id in seen_ids:
                    raise ValueError(f"duplicate prompt_instance_id: {prompt_id!r}")
                seen_ids.add(prompt_id)

                if prompt_id != source.get("prompt_instance_id"):
                    raise ValueError(
                        "result order does not match source: "
                        f"{prompt_id!r} != {source.get('prompt_instance_id')!r}"
                    )
                if result.get("prompt") != source.get("prompt"):
                    raise ValueError(f"prompt mismatch for {prompt_id!r}")
                validate_lens_result(result, prompt_id)

                counters.add(result)
                output_handle.write(json.dumps(result, ensure_ascii=False) + "\n")

    try:
        missing_source = next(source_iterator)
    except StopIteration:
        missing_source = None
    if missing_source is not None:
        raise ValueError(
            "shards contain fewer rows than source; first missing ID is "
            f"{missing_source.get('prompt_instance_id')!r}"
        )

    counts = counters.as_dict()
    counts["num_unique_prompt_instance_ids"] = len(seen_ids)
    if expected_records is not None and counts["num_input_records"] != expected_records:
        raise ValueError(
            f"expected {expected_records} merged rows, "
            f"found {counts['num_input_records']}"
        )
    if counts["num_unique_prompt_instance_ids"] != counts["num_input_records"]:
        raise ValueError("merged IDs are not unique")
    return counts


def main() -> None:
    """Validate shard metadata, merge records, and write final provenance."""

    args = parse_args()
    if args.expected_records <= 0:
        raise ValueError("expected-records must be positive")
    validate_destinations(
        (args.output, args.summary_output), overwrite=args.overwrite
    )
    summary_paths, shard_summaries = load_and_validate_shard_summaries(args.shards)
    counts = merge_records(
        args.source,
        args.shards,
        args.output,
        expected_records=args.expected_records,
    )
    recomputed_counts_match_shard_summaries(counts, shard_summaries)

    parameters = shard_summaries[0]
    summary = {
        "model": parameters["model"],
        "stage_one_revision": parameters["stage_one_revision"],
        "model_commit": parameters["model_commit"],
        "dtype": parameters["dtype"],
        "reference_code_commit": parameters["reference_code_commit"],
        "source": str(args.source),
        "input_shards": [str(path) for path in args.shards],
        "input_shard_summaries": [str(path) for path in summary_paths],
        "output": str(args.output),
        "chunk_size": parameters["chunk_size"],
        "nodes": parameters["nodes"],
        "intermediate_node": parameters["intermediate_node"],
        "rank_scope": parameters["rank_scope"],
        "target_definition": parameters["target_definition"],
        "query_positions": parameters["query_positions"],
        "layers": parameters["layers"],
        "processing_signature": parameters["processing_signature"],
        "overall_evidence": parameters["overall_evidence"],
        "composition_rr_threshold": parameters["composition_rr_threshold"],
        "shortcut_rr_threshold": parameters["shortcut_rr_threshold"],
        **counts,
    }
    args.summary_output.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))
    print(f"Wrote {args.output}")
    print(f"Wrote {args.summary_output}")


if __name__ == "__main__":
    main()
