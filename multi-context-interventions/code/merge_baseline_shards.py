"""Validate and merge sharded baseline-evaluation outputs.

Inputs:
    The canonical prompt manifest and the ordered baseline JSONL shards.

Outputs:
    One JSONL file in canonical manifest order and one aggregate JSON summary.

The merger recomputes every aggregate from the per-prompt results.  It also
checks each result against the corresponding manifest row, so a missing,
duplicated, or misordered shard fails instead of silently producing a corrupt
combined file.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterator


PROJECT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = PROJECT_DIR / "results" / "all_queries_prompt_manifest.jsonl"
DEFAULT_SHARDS = tuple(
    PROJECT_DIR / "results" / f"baseline_full_shard_{index:02d}.jsonl"
    for index in range(1, 6)
)
DEFAULT_OUTPUT = PROJECT_DIR / "results" / "baseline_full.jsonl"
DEFAULT_SUMMARY = PROJECT_DIR / "results" / "baseline_full_summary.json"


def parse_args() -> argparse.Namespace:
    """Parse manifest, shard, and output paths from the command line."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--shards", type=Path, nargs="+", default=DEFAULT_SHARDS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def read_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    """Yield parsed nonempty JSON objects from one JSONL file."""

    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number} is not a JSON object")
            yield value


def validate_destinations(paths: tuple[Path, ...], *, overwrite: bool) -> None:
    """Create parent directories and prevent accidental replacement."""

    existing = [str(path) for path in paths if path.exists()]
    if existing and not overwrite:
        raise FileExistsError(
            "outputs already exist; pass --overwrite: " + ", ".join(existing)
        )
    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)


def load_and_validate_shard_summaries(
    shard_paths: list[Path] | tuple[Path, ...],
) -> tuple[list[Path], list[dict[str, Any]]]:
    """Load companion summaries and verify shared experimental parameters."""

    summary_paths = [
        path.with_name(f"{path.stem}_summary.json") for path in shard_paths
    ]
    summaries = [json.loads(path.read_text(encoding="utf-8")) for path in summary_paths]
    if not summaries:
        raise ValueError("at least one shard is required")

    shared_keys = (
        "model",
        "stage_one_revision",
        "model_commit",
        "dtype",
        "input",
        "batch_size",
        "max_new_tokens",
        "stop_sequence",
        "top_k_values",
        "rank_scope",
        "target_measurement",
    )
    reference = summaries[0]
    expected_start = 0
    for shard_path, shard_summary in zip(shard_paths, summaries, strict=True):
        for key in shared_keys:
            if shard_summary.get(key) != reference.get(key):
                raise ValueError(f"shard summaries disagree on {key!r}")
        if shard_summary.get("output") != str(shard_path):
            raise ValueError(f"summary output path does not match {shard_path}")
        if shard_summary.get("start_index") != expected_start:
            raise ValueError(
                f"noncontiguous shard start: expected {expected_start}, "
                f"got {shard_summary.get('start_index')}"
            )
        if shard_summary.get("requested_num_records") != shard_summary.get(
            "num_prompt_instances"
        ):
            raise ValueError(f"incomplete shard reported by {shard_path}")
        expected_start += int(shard_summary["num_prompt_instances"])

    return summary_paths, summaries


def main() -> None:
    args = parse_args()
    validate_destinations(
        (args.output, args.summary_output), overwrite=args.overwrite
    )

    shard_summary_paths, shard_summaries = load_and_validate_shard_summaries(
        args.shards
    )
    run_parameters = shard_summaries[0]
    top_ks = tuple(int(k) for k in run_parameters["top_k_values"])
    manifest_iterator = read_jsonl(args.manifest)
    seen_ids: set[str] = set()
    evaluated = 0
    exact_correct = 0
    rank_sum = 0
    top_k_correct = {k: 0 for k in top_ks}

    with args.output.open("w", encoding="utf-8") as output_handle:
        for shard_path in args.shards:
            for result in read_jsonl(shard_path):
                try:
                    manifest_record = next(manifest_iterator)
                except StopIteration as error:
                    raise ValueError("shards contain more rows than the manifest") from error

                prompt_id = result.get("prompt_instance_id")
                if prompt_id in seen_ids:
                    raise ValueError(f"duplicate prompt_instance_id: {prompt_id!r}")
                seen_ids.add(prompt_id)

                if prompt_id != manifest_record.get("prompt_instance_id"):
                    raise ValueError(
                        "result order does not match manifest: "
                        f"{prompt_id!r} != {manifest_record.get('prompt_instance_id')!r}"
                    )
                if result.get("prompt") != manifest_record.get("prompt"):
                    raise ValueError(f"prompt text mismatch for {prompt_id!r}")

                evaluation = result["evaluation"]
                final_gfx = evaluation["final_next_token_readout"][
                    "GFx_first_token"
                ]
                evaluated += 1
                exact_correct += int(evaluation["exact_match"])
                rank_sum += int(final_gfx["rank"])
                for k in top_k_correct:
                    top_k_correct[k] += int(final_gfx["in_top_k"][str(k)])

                output_handle.write(json.dumps(result, ensure_ascii=False) + "\n")

    try:
        extra_manifest_record = next(manifest_iterator)
    except StopIteration:
        extra_manifest_record = None
    if extra_manifest_record is not None:
        raise ValueError(
            "shards contain fewer rows than the manifest; first missing row is "
            f"{extra_manifest_record.get('prompt_instance_id')!r}"
        )

    denominator = evaluated or 1
    summary = {
        "model": run_parameters["model"],
        "stage_one_revision": run_parameters["stage_one_revision"],
        "model_commit": run_parameters["model_commit"],
        "dtype": run_parameters["dtype"],
        "input_manifest": str(args.manifest),
        "input_shards": [str(path) for path in args.shards],
        "input_shard_summaries": [str(path) for path in shard_summary_paths],
        "output": str(args.output),
        "batch_size_per_shard": run_parameters["batch_size"],
        "max_new_tokens": run_parameters["max_new_tokens"],
        "stop_sequence": run_parameters["stop_sequence"],
        "top_k_values": list(top_ks),
        "rank_scope": run_parameters["rank_scope"],
        "target_measurement": run_parameters["target_measurement"],
        "num_prompt_instances": evaluated,
        "num_unique_prompt_instance_ids": len(seen_ids),
        "num_exact_correct": exact_correct,
        "exact_accuracy": exact_correct / denominator,
        "final_next_token_readout": {
            "GFx_first_token_top_k": {
                str(k): {
                    "correct": correct,
                    "accuracy": correct / denominator,
                }
                for k, correct in top_k_correct.items()
            },
            "mean_GFx_first_token_rank": rank_sum / denominator,
        },
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
