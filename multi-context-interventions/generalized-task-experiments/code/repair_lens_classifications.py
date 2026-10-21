"""Repair float-boundary lens classifications without rerunning the model.

The lens evaluators originally formed reciprocal ranks in float32.  Rank five
therefore appeared as ``0.20000000298`` and failed the intended ``RR <= 0.2``
shortcut test.  This utility reconstructs each exact integer rank, stores its
exact Python reciprocal, and classifies directly from the integer rank.

Only reciprocal-rank and classification fields are changed.  Prompts, logits,
selected positions, and all behavioral measurements remain untouched.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
from typing import Any, Mapping

from evaluate_baseline import open_text, read_jsonl
from evaluate_jlens import RunningSummary as JLensSummary
from evaluate_logit_lens import RunningSummary as LogitLensSummary, classify_rank
from tasks import TASKS, get_task_spec


PROJECT_DIR = Path(__file__).resolve().parent.parent
CLASSIFICATION_RULE = "rank<=2 compositional; rank 3-4 ambiguous; rank>=5 shortcut_candidate"


def exact_rank(reciprocal_rank: float) -> int:
    """Recover and verify the positive integer behind a stored reciprocal."""

    value = float(reciprocal_rank)
    if not math.isfinite(value) or not 0.0 < value <= 1.0:
        raise ValueError("reciprocal rank must be finite and in (0, 1]")
    rank = round(1.0 / value)
    if rank < 1 or not math.isclose(value, 1.0 / rank, rel_tol=1e-6, abs_tol=1e-9):
        raise ValueError(f"value is not an integer reciprocal rank: {value}")
    return rank


def repair_measurement(measurement: dict[str, Any], lens_name: str) -> bool:
    """Repair one eligible lens object and report whether it changed."""

    if lens_name not in {"logit_lens", "j_lens"}:
        raise ValueError("lens_name must be logit_lens or j_lens")
    if not measurement.get("paper_token_eligible"):
        return False
    rr_key = "llens_rr" if lens_name == "logit_lens" else "jlens_rr"
    reciprocal_ranks = measurement.get(rr_key)
    classification = measurement.get("classification")
    if not isinstance(reciprocal_ranks, list) or not reciprocal_ranks:
        raise ValueError(f"eligible {lens_name} lacks {rr_key}")
    if not isinstance(classification, dict):
        raise ValueError(f"eligible {lens_name} lacks classification")

    ranks = [exact_rank(value) for value in reciprocal_ranks]
    exact_rr = [1.0 / rank for rank in ranks]
    best_rank = min(ranks)
    saved_best_rank = classification.get("best_vocabulary_rank")
    if saved_best_rank != best_rank:
        raise ValueError(
            f"{lens_name} best rank disagrees with layerwise ranks: "
            f"{saved_best_rank} != {best_rank}"
        )
    exact_peak = 1.0 / best_rank
    exact_group = classify_rank(best_rank)
    changed = (
        reciprocal_ranks != exact_rr
        or classification.get("peak_reciprocal_rank") != exact_peak
        or classification.get("group") != exact_group
    )
    measurement[rr_key] = exact_rr
    classification["peak_reciprocal_rank"] = exact_peak
    classification["group"] = exact_group
    return changed


def _temporary_jsonl(path: Path) -> Path:
    """Choose a sibling temporary path preserving gzip detection."""

    if path.suffix == ".gz":
        return path.with_name(f"{path.name[:-3]}.tmp.{os.getpid()}.gz")
    return path.with_name(f"{path.name}.tmp.{os.getpid()}")


def repair_jsonl(path: Path, *, include_jlens: bool) -> tuple[int, int, Any]:
    """Atomically repair one result file and recompute its aggregate counts."""

    temporary = _temporary_jsonl(path)
    changed = records = 0
    counters: Any = JLensSummary() if include_jlens else LogitLensSummary()
    try:
        with open_text(temporary, "wt") as handle:
            for record in read_jsonl(path):
                records += 1
                changed += int(repair_measurement(record["logit_lens"], "logit_lens"))
                if include_jlens:
                    changed += int(repair_measurement(record["j_lens"], "j_lens"))
                    counters.add(record)
                else:
                    counters.add(record["logit_lens"])
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)
    return records, changed, counters


def update_summary(path: Path, counts: Mapping[str, Any]) -> None:
    """Replace aggregate fields while preserving the original provenance."""

    summary = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(summary, dict):
        raise ValueError(f"summary must be an object: {path}")
    aggregate_keys = {
        "num_input_records",
        "num_paper_token_eligible",
        "num_paper_token_excluded",
        "paper_token_exclusion_reasons",
        "classification_counts",
        "logit_lens_to_j_lens_transitions",
    }
    for key in aggregate_keys:
        if key in counts:
            summary[key] = counts[key]
        elif key in summary:
            summary.pop(key)
    summary["classification_rank_rule"] = CLASSIFICATION_RULE
    temporary = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    try:
        temporary.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def companion_summary(path: Path) -> Path:
    """Return the summary path paired with one JSONL shard."""

    for suffix in (".jsonl.gz", ".jsonl"):
        if path.name.endswith(suffix):
            return path.with_name(f"{path.name[:-len(suffix)]}_summary.json")
    raise ValueError(f"unsupported result suffix: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, choices=sorted(TASKS))
    args = parser.parse_args()

    task = get_task_spec(args.task).dataset_task
    task_directory = PROJECT_DIR / "results" / task
    logit_path = task_directory / "logit_lens_evaluation.jsonl.gz"
    logit_summary = task_directory / "logit_lens_summary.json"
    records, changes, counters = repair_jsonl(logit_path, include_jlens=False)
    update_summary(logit_summary, counters.as_dict())
    report = {
        "logit_lens": {"records": records, "changed_measurements": changes},
        "j_lens_shards": [],
    }

    shard_paths = sorted((task_directory / "jlens_shards").glob("jlens_shard_*.jsonl.gz"))
    if not shard_paths:
        raise ValueError("no J-Lens shards found")
    for shard in shard_paths:
        records, changes, counters = repair_jsonl(shard, include_jlens=True)
        update_summary(companion_summary(shard), counters.as_dict())
        report["j_lens_shards"].append(
            {"path": str(shard), "records": records, "changed_measurements": changes}
        )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
