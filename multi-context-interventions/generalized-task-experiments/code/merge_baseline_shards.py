"""Validate and merge task-general baseline-evaluation shards.

Each GPU shard evaluates one contiguous slice of the canonical prompt
manifest.  This file verifies that the slices are complete, non-overlapping,
and in manifest order before producing one baseline JSONL and summary.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

from evaluate_baseline import RunningSummary, open_text, read_jsonl
from tasks import TASKS, get_task_spec


PROJECT_DIR = Path(__file__).resolve().parent.parent


def companion_summary(shard: Path) -> Path:
    """Return the evaluator summary path corresponding to one shard."""

    name = shard.name
    for ending in (".jsonl.gz", ".jsonl"):
        if name.endswith(ending):
            return shard.with_name(f"{name[:-len(ending)]}_summary.json")
    raise ValueError(f"unsupported shard filename: {shard}")


def ordered_shards(shard_directory: Path) -> tuple[list[Path], list[dict[str, Any]]]:
    """Find shards and order them by their recorded manifest start index."""

    shard_paths = list(shard_directory.glob("baseline_shard_*.jsonl"))
    shard_paths.extend(shard_directory.glob("baseline_shard_*.jsonl.gz"))
    if not shard_paths:
        raise ValueError(f"no baseline shards found in {shard_directory}")
    pairs = []
    for shard in shard_paths:
        summary_path = companion_summary(shard)
        if not summary_path.exists():
            raise FileNotFoundError(f"missing summary for {shard}: {summary_path}")
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        pairs.append((int(summary["start_index"]), shard, summary))
    pairs.sort(key=lambda value: value[0])
    return [value[1] for value in pairs], [value[2] for value in pairs]


def validate_summaries(
    shard_paths: Sequence[Path], summaries: Sequence[dict[str, Any]], task: str
) -> tuple[int, ...]:
    """Verify common parameters and exact contiguous shard boundaries."""

    if not summaries:
        raise ValueError("at least one shard summary is required")
    shared_keys = (
        "task",
        "model",
        "stage_one_revision",
        "model_commit",
        "dtype",
        "input",
        "batch_size",
        "max_new_tokens",
        "stop_sequence",
        "rank_scope",
        "target_measurement",
        "candidate_catalog",
    )
    reference = summaries[0]
    if reference.get("task") != task:
        raise ValueError(f"shard task {reference.get('task')!r} does not match {task!r}")
    expected_start = 0
    for shard, summary in zip(shard_paths, summaries, strict=True):
        for key in shared_keys:
            if summary.get(key) != reference.get(key):
                raise ValueError(f"shard summaries disagree on {key!r}")
        if summary.get("output") != str(shard):
            raise ValueError(f"summary output path does not match {shard}")
        if int(summary["start_index"]) != expected_start:
            raise ValueError(
                f"noncontiguous shard start: expected {expected_start}, "
                f"got {summary['start_index']}"
            )
        requested = summary.get("requested_num_records")
        completed = int(summary["num_prompt_instances"])
        if requested is None or int(requested) != completed:
            raise ValueError(f"incomplete shard reported by {shard}")
        expected_start += completed

    top_k_keys = tuple(
        sorted(int(value) for value in reference["GFx_first_token_top_k"])
    )
    return top_k_keys


def merge_baseline_shards(
    *,
    task: str,
    manifest: Path,
    shard_directory: Path,
    output: Path,
    summary_output: Path,
    overwrite: bool = False,
) -> dict[str, Any]:
    """Merge verified shards and return the aggregate summary."""

    existing = [path for path in (output, summary_output) if path.exists()]
    if existing and not overwrite:
        raise FileExistsError(f"outputs already exist; use --overwrite: {existing}")
    output.parent.mkdir(parents=True, exist_ok=True)
    summary_output.parent.mkdir(parents=True, exist_ok=True)

    shard_paths, shard_summaries = ordered_shards(shard_directory)
    top_ks = validate_summaries(shard_paths, shard_summaries, task)
    manifest_rows = read_jsonl(manifest)
    counters = RunningSummary(top_ks)
    seen_ids: set[str] = set()
    temporary_output = output.with_name(f"{output.stem}.tmp{output.suffix}")

    try:
        with open_text(temporary_output, "wt") as handle:
            for shard in shard_paths:
                for result in read_jsonl(shard):
                    try:
                        expected = next(manifest_rows)
                    except StopIteration as error:
                        raise ValueError("shards contain more rows than manifest") from error
                    prompt_id = result.get("prompt_instance_id")
                    if prompt_id in seen_ids:
                        raise ValueError(f"duplicate prompt_instance_id: {prompt_id!r}")
                    seen_ids.add(prompt_id)
                    if prompt_id != expected.get("prompt_instance_id"):
                        raise ValueError(
                            f"result order mismatch: {prompt_id!r} != "
                            f"{expected.get('prompt_instance_id')!r}"
                        )
                    for field in ("task", "query_index", "context_variant", "query", "context", "prompt"):
                        if result.get(field) != expected.get(field):
                            raise ValueError(f"{field} mismatch for {prompt_id!r}")
                    counters.add(result)
                    handle.write(json.dumps(result, ensure_ascii=False) + "\n")

        try:
            missing = next(manifest_rows)
        except StopIteration:
            missing = None
        if missing is not None:
            raise ValueError(
                "shards contain fewer rows than manifest; first missing row is "
                f"{missing.get('prompt_instance_id')!r}"
            )
        temporary_output.replace(output)
    except Exception:
        temporary_output.unlink(missing_ok=True)
        raise

    reference = shard_summaries[0]
    summary = {
        "task": task,
        "model": reference["model"],
        "stage_one_revision": reference["stage_one_revision"],
        "model_commit": reference["model_commit"],
        "dtype": reference["dtype"],
        "input": str(manifest),
        "input_shards": [str(path) for path in shard_paths],
        "output": str(output),
        "batch_size": reference["batch_size"],
        "max_new_tokens": reference["max_new_tokens"],
        "stop_sequence": reference["stop_sequence"],
        "rank_scope": reference["rank_scope"],
        "target_measurement": reference["target_measurement"],
        "candidate_catalog": reference["candidate_catalog"],
        "num_unique_prompt_instance_ids": len(seen_ids),
        **counters.as_dict(),
    }
    summary_output.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def parse_args() -> argparse.Namespace:
    """Parse task and optional path overrides."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, choices=sorted(TASKS))
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--shard-directory", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--summary-output", type=Path)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    task = get_task_spec(args.task).dataset_task
    task_directory = PROJECT_DIR / "results" / task
    summary = merge_baseline_shards(
        task=task,
        manifest=args.manifest or task_directory / "prompt_manifest.jsonl",
        shard_directory=args.shard_directory or task_directory / "baseline_shards",
        output=args.output or task_directory / "baseline_evaluation.jsonl.gz",
        summary_output=args.summary_output or task_directory / "baseline_summary.json",
        overwrite=args.overwrite,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
