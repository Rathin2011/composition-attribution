#!/usr/bin/env python3
"""Run Stage 01: validate, split, and prepare existing baseline records."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


EXPERIMENT_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = EXPERIMENT_DIR.parent
sys.path.insert(0, str(EXPERIMENT_DIR))

from multipath.prepare import (  # noqa: E402
    DEFAULT_SELECTION_FRACTION,
    DEFAULT_SPLIT_SEED,
    load_alias_config,
    load_task_sources,
    prepare_task,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", action="append", default=[], help="Task to prepare; repeatable. Defaults to all configured tasks.")
    parser.add_argument("--task-config", type=Path, default=EXPERIMENT_DIR / "configs/tasks.json")
    parser.add_argument("--alias-config", type=Path, default=EXPERIMENT_DIR / "configs/answer_aliases.json")
    parser.add_argument("--output-root", type=Path, default=EXPERIMENT_DIR / "results")
    parser.add_argument("--selection-fraction", type=float, default=DEFAULT_SELECTION_FRACTION)
    parser.add_argument("--seed", type=int, default=DEFAULT_SPLIT_SEED)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    sources = load_task_sources(args.task_config, PROJECT_ROOT)
    selected = args.task or list(sources)
    unknown = sorted(set(selected) - set(sources))
    if unknown:
        raise ValueError(f"unconfigured tasks: {unknown}")
    aliases, eligibility = load_alias_config(args.alias_config, selected)
    summaries = []
    for task in selected:
        output = args.output_root / task / "icl_10" / "01_prepare"
        summary = prepare_task(
            sources[task],
            output_directory=output,
            aliases=aliases[task],
            eligibility=eligibility,
            selection_fraction=args.selection_fraction,
            seed=args.seed,
            overwrite=args.overwrite,
        )
        summaries.append(
            {
                "task": task,
                "output": str(output),
                "counts": summary["counts"],
            }
        )
    print(json.dumps(summaries, indent=2))


if __name__ == "__main__":
    main()

