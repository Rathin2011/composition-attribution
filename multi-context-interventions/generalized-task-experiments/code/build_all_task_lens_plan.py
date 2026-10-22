"""Build a deterministic full-run shard plan from GFx-correct populations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from evaluate_baseline import read_jsonl
from tasks import TASKS


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-root", type=Path, required=True)
    parser.add_argument("--records-per-shard", type=int, default=100)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.records_per_shard <= 0:
        raise ValueError("records-per-shard must be positive")
    root = args.results_root.resolve(strict=True)
    plan = []
    for task in sorted(TASKS):
        directory = root / task
        source = directory / "correct_instances.jsonl.gz"
        if not source.is_file():
            continue
        total = sum(1 for _ in read_jsonl(source))
        if total <= 0:
            continue
        for start in range(0, total, args.records_per_shard):
            plan.append({
                "task": task,
                "directory": str(directory),
                "start": start,
                "count": min(args.records_per_shard, total - start),
                "total": total,
            })
    if not plan:
        raise ValueError(f"no correct-instance populations under {root}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "results_root": str(root),
        "records_per_shard": args.records_per_shard,
        "tasks": len({row["task"] for row in plan}),
        "array_tasks": len(plan),
        "records": sum(row["count"] for row in plan),
        "output": str(args.output),
    }, indent=2))


if __name__ == "__main__":
    main()
