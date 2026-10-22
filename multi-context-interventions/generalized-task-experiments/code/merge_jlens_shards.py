"""Validate and merge task-general J-Lens result shards."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from evaluate_baseline import open_text, read_jsonl
from evaluate_jlens import EXPECTED_SOURCE_LAYERS, RunningSummary
from evaluate_logit_lens import classify_rank
from tasks import TASKS, get_task_spec


PROJECT_DIR = Path(__file__).resolve().parent.parent
GROUPS = ("compositional", "ambiguous", "shortcut_candidate")
SHARED_SUMMARY_KEYS = (
    "task",
    "model",
    "stage_one_revision",
    "model_commit",
    "dtype",
    "jlens_commit",
    "lens",
    "lens_sha256",
    "lens_fit_prompts",
    "input",
    "candidate_catalog_source",
    "max_seq_len",
    "candidate_chunk_size",
    "Fx_catalog",
    "rank_scope",
    "target_definition",
    "query_positions",
    "source_layers",
    "processing_signature",
    "position_tie_break",
    "composition_rr_threshold",
    "shortcut_rr_threshold",
    "classification_rank_rule",
)


def companion_summary(shard: Path) -> Path:
    """Return the summary path paired with one JSONL shard."""

    for suffix in (".jsonl.gz", ".jsonl"):
        if shard.name.endswith(suffix):
            return shard.with_name(f"{shard.name[:-len(suffix)]}_summary.json")
    raise ValueError(f"unsupported shard filename: {shard}")


def ordered_shards(
    directory: Path,
) -> tuple[list[Path], list[dict[str, Any]], list[Path]]:
    """Find J-Lens shards and order them by their recorded source offset."""

    shards = list(directory.glob("jlens_shard_*.jsonl"))
    shards.extend(directory.glob("jlens_shard_*.jsonl.gz"))
    if not shards:
        raise ValueError(f"no J-Lens shards found in {directory}")
    entries = []
    for shard in shards:
        summary_path = companion_summary(shard)
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        if not isinstance(summary, dict):
            raise ValueError(f"summary must be an object: {summary_path}")
        entries.append((int(summary["start_index"]), shard, summary, summary_path))
    entries.sort(key=lambda entry: entry[0])
    return (
        [entry[1] for entry in entries],
        [entry[2] for entry in entries],
        [entry[3] for entry in entries],
    )


def validate_summaries(
    shards: Sequence[Path], summaries: Sequence[Mapping[str, Any]], *, task: str
) -> tuple[int, int]:
    """Require shared provenance and contiguous, complete shard boundaries."""

    if not summaries:
        raise ValueError("at least one shard summary is required")
    reference = summaries[0]
    if reference.get("task") != task:
        raise ValueError("J-Lens shard task does not match requested task")
    catalog = reference.get("Fx_catalog")
    if not isinstance(catalog, list) or not catalog:
        raise ValueError("J-Lens summaries lack a nonempty Fx catalog")
    if reference.get("source_layers") != list(EXPECTED_SOURCE_LAYERS):
        raise ValueError("unexpected J-Lens source layers")

    expected_start = 0
    for shard, summary in zip(shards, summaries, strict=True):
        for key in SHARED_SUMMARY_KEYS:
            if key not in summary:
                raise ValueError(f"J-Lens summary for {shard} is missing {key!r}")
            if summary.get(key) != reference.get(key):
                raise ValueError(f"J-Lens summaries disagree on {key!r}")
        if summary.get("output") != str(shard):
            raise ValueError(f"summary output path does not match {shard}")
        if int(summary["start_index"]) != expected_start:
            raise ValueError(
                f"noncontiguous shard start: expected {expected_start}, "
                f"found {summary['start_index']}"
            )
        completed = int(summary["num_input_records"])
        if completed <= 0 or int(summary["requested_num_records"]) != completed:
            raise ValueError(f"incomplete J-Lens shard: {shard}")
        expected_start += completed
    return expected_start, len(catalog)


def _numeric_vector(value: Any, length: int, name: str) -> None:
    if not isinstance(value, list) or len(value) != length:
        raise ValueError(f"{name} must have length {length}")
    if any(not isinstance(item, (int, float)) for item in value):
        raise ValueError(f"{name} must contain only numbers")


def validate_result(record: Mapping[str, Any], *, n_fx: int) -> None:
    """Validate one eligible or paper-filtered J-Lens record."""

    prompt_id = record.get("prompt_instance_id")
    llens = record.get("logit_lens")
    jlens = record.get("j_lens")
    if not isinstance(llens, Mapping) or not isinstance(jlens, Mapping):
        raise ValueError(f"result {prompt_id!r} lacks lens measurements")
    eligible = jlens.get("paper_token_eligible")
    if not isinstance(eligible, bool) or eligible != llens.get("paper_token_eligible"):
        raise ValueError(f"result {prompt_id!r} has inconsistent eligibility")
    if jlens.get("source_layers") != list(EXPECTED_SOURCE_LAYERS):
        raise ValueError(f"result {prompt_id!r} has unexpected source layers")

    if not eligible:
        if jlens.get("paper_token_filter_reason") != llens.get(
            "paper_token_filter_reason"
        ):
            raise ValueError(f"result {prompt_id!r} changed exclusion reason")
        if any(jlens.get(key) is not None for key in ("classification", "jlens_z", "jlens_rr")):
            raise ValueError(f"excluded result {prompt_id!r} contains measurements")
        return

    num_layers = len(EXPECTED_SOURCE_LAYERS)
    z = jlens.get("jlens_z")
    if not isinstance(z, list) or len(z) != n_fx:
        raise ValueError(f"jlens_z for {prompt_id!r} must have {n_fx} rows")
    for row in z:
        _numeric_vector(row, num_layers, f"jlens_z row for {prompt_id!r}")
    rr = jlens.get("jlens_rr")
    _numeric_vector(rr, num_layers, f"jlens_rr for {prompt_id!r}")
    classification = jlens.get("classification")
    if not isinstance(classification, Mapping):
        raise ValueError(f"result {prompt_id!r} lacks J-Lens classification")
    best_rank = classification.get("best_vocabulary_rank")
    if not isinstance(best_rank, int) or best_rank < 1:
        raise ValueError(f"result {prompt_id!r} has invalid best rank")
    if classification.get("group") != classify_rank(best_rank):
        raise ValueError(f"result {prompt_id!r} has an inexact rank classification")
    if classification.get("peak_reciprocal_rank") != 1.0 / best_rank:
        raise ValueError(f"result {prompt_id!r} has an inexact peak RR")
    if max(rr) != 1.0 / best_rank:
        raise ValueError(f"result {prompt_id!r} layerwise RR disagrees with best rank")
    if jlens.get("query_token_start") != llens.get("query_token_start") or jlens.get(
        "num_query_positions"
    ) != llens.get("num_query_positions"):
        raise ValueError(f"result {prompt_id!r} changed the query-token span")


def expected_counts(summaries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Sum repaired shard summaries for comparison with merged records."""

    groups: Counter[str] = Counter()
    transitions: Counter[str] = Counter()
    exclusions: Counter[str] = Counter()
    total = eligible = excluded = 0
    for summary in summaries:
        total += int(summary["num_input_records"])
        eligible += int(summary["num_paper_token_eligible"])
        excluded += int(summary["num_paper_token_excluded"])
        groups.update(summary["classification_counts"])
        transitions.update(summary["logit_lens_to_j_lens_transitions"])
        exclusions.update(summary["paper_token_exclusion_reasons"])
    return {
        "num_input_records": total,
        "num_paper_token_eligible": eligible,
        "num_paper_token_excluded": excluded,
        "paper_token_exclusion_reasons": dict(sorted(exclusions.items())),
        "classification_counts": {group: groups[group] for group in GROUPS},
        "logit_lens_to_j_lens_transitions": dict(sorted(transitions.items())),
    }


def merge_jlens_shards(
    *,
    task: str,
    source: Path,
    shard_directory: Path,
    output: Path,
    summary_output: Path,
    overwrite: bool = False,
) -> dict[str, Any]:
    """Validate, atomically merge, and summarize one task's J-Lens shards."""

    existing = [path for path in (output, summary_output) if path.exists()]
    if existing and not overwrite:
        raise FileExistsError(f"outputs already exist; use --overwrite: {existing}")
    output.parent.mkdir(parents=True, exist_ok=True)
    shards, summaries, summary_paths = ordered_shards(shard_directory)
    total_records, n_fx = validate_summaries(shards, summaries, task=task)
    source_rows = read_jsonl(source)
    counters = RunningSummary()
    seen: set[str] = set()
    temporary = output.with_name(f"{output.name[:-3]}.tmp.gz") if output.suffix == ".gz" else output.with_name(f"{output.name}.tmp")

    try:
        with open_text(temporary, "wt") as handle:
            for shard in shards:
                for result in read_jsonl(shard):
                    try:
                        expected = next(source_rows)
                    except StopIteration as error:
                        raise ValueError("J-Lens shards contain more rows than source") from error
                    prompt_id = result.get("prompt_instance_id")
                    if not isinstance(prompt_id, str) or prompt_id in seen:
                        raise ValueError(f"invalid or duplicate prompt ID: {prompt_id!r}")
                    seen.add(prompt_id)
                    source_part = dict(result)
                    source_part.pop("j_lens", None)
                    if source_part != expected:
                        raise ValueError(f"source fields changed for {prompt_id!r}")
                    validate_result(result, n_fx=n_fx)
                    counters.add(result)
                    handle.write(json.dumps(result, ensure_ascii=False) + "\n")
        try:
            missing = next(source_rows)
        except StopIteration:
            missing = None
        if missing is not None:
            raise ValueError(f"first missing source ID: {missing.get('prompt_instance_id')!r}")
        if len(seen) != total_records:
            raise ValueError(f"expected {total_records} unique rows, found {len(seen)}")
        counts = counters.as_dict()
        if counts != expected_counts(summaries):
            raise ValueError("record-level counts disagree with repaired shard summaries")
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, choices=sorted(TASKS))
    parser.add_argument("--source", type=Path)
    parser.add_argument("--shard-directory", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--summary-output", type=Path)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    task = get_task_spec(args.task).dataset_task
    task_directory = PROJECT_DIR / "results" / task
    summary = merge_jlens_shards(
        task=task,
        source=args.source or task_directory / "logit_lens_evaluation.jsonl.gz",
        shard_directory=args.shard_directory or task_directory / "jlens_shards",
        output=args.output or task_directory / "jlens_evaluation.jsonl.gz",
        summary_output=args.summary_output or task_directory / "jlens_summary.json",
        overwrite=args.overwrite,
    )
    print(json.dumps({key: value for key, value in summary.items() if key != "Fx_catalog"}, indent=2))


if __name__ == "__main__":
    main()
