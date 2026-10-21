"""Freeze the exact-correct query-context instances from baseline evaluation.

Input
-----
One merged baseline JSONL or JSONL.GZ file produced by
``merge_baseline_shards.py``.  Every row is one query under one sampled ICL
context and contains ``evaluation.exact_match``.

Output
------
``correct_instances.jsonl.gz``
    Exact copies of rows whose complete greedy answer matched the expected
    ``GFx`` answer.  No fields are removed or renamed.

``correct_instances_summary.json``
    Input/output counts plus the number of correct contexts for every unique
    query, including queries that were never answered correctly.

This is a task-general, model-free pipeline stage.  It fixes the population
that later Logit-Lens, J-Lens, and intervention stages must share.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

from evaluate_baseline import ensure_outputs, open_text, read_jsonl
from tasks import TASKS, get_task_spec


PROJECT_DIR = Path(__file__).resolve().parent.parent


def parse_args() -> argparse.Namespace:
    """Parse the task and optional baseline/output path overrides."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, choices=sorted(TASKS))
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--summary-output", type=Path)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def _temporary_path(path: Path) -> Path:
    """Return a sibling temporary path that preserves gzip detection."""

    return path.with_name(f"{path.stem}.tmp{path.suffix}")


def _validated_query(
    record: Mapping[str, Any], *, line_number: int
) -> tuple[int, dict[str, str]]:
    """Validate and return one record's stable query identity.

    Input:
        A baseline result row and its one-based input line number.
    Output:
        ``(query_index, query)`` where ``query`` contains string ``x``, ``Fx``,
        and ``GFx`` values.
    """

    query_index = record.get("query_index")
    if isinstance(query_index, bool) or not isinstance(query_index, int):
        raise ValueError(f"line {line_number} has invalid query_index")
    query = record.get("query")
    if not isinstance(query, Mapping):
        raise ValueError(f"line {line_number} lacks a query object")
    output: dict[str, str] = {}
    for field in ("x", "Fx", "GFx"):
        value = query.get(field)
        if not isinstance(value, str) or not value:
            raise ValueError(f"line {line_number} has invalid query.{field}")
        output[field] = value
    return query_index, output


def select_correct_instances(
    *,
    task: str,
    input_path: Path,
    output_path: Path,
    summary_path: Path,
    overwrite: bool = False,
) -> dict[str, Any]:
    """Filter one merged baseline and return its selection summary.

    Functional flow:

    1. Stream baseline rows instead of loading the full file into memory.
    2. Validate task identity, unique prompt-instance IDs, stable query
       metadata, and the boolean full-answer exact-match field.
    3. Write exact-matching rows unchanged to a temporary compressed file.
    4. Atomically install the result and write aggregate/per-query counts.
    """

    ensure_outputs((output_path, summary_path), overwrite)
    temporary_output = _temporary_path(output_path)

    seen_prompt_ids: set[str] = set()
    queries: dict[int, dict[str, str]] = {}
    input_counts: dict[int, int] = {}
    correct_counts: dict[int, int] = {}
    num_input = 0
    num_correct = 0

    try:
        with open_text(temporary_output, "wt") as output_handle:
            for line_number, record in enumerate(read_jsonl(input_path), start=1):
                if record.get("task") != task:
                    raise ValueError(
                        f"line {line_number} has task {record.get('task')!r}, "
                        f"expected {task!r}"
                    )

                prompt_id = record.get("prompt_instance_id")
                if not isinstance(prompt_id, str) or not prompt_id:
                    raise ValueError(
                        f"line {line_number} has invalid prompt_instance_id"
                    )
                if prompt_id in seen_prompt_ids:
                    raise ValueError(f"duplicate prompt_instance_id: {prompt_id!r}")
                seen_prompt_ids.add(prompt_id)

                query_index, query = _validated_query(
                    record, line_number=line_number
                )
                previous_query = queries.setdefault(query_index, query)
                if previous_query != query:
                    raise ValueError(
                        f"query metadata changes across contexts for index "
                        f"{query_index}"
                    )

                evaluation = record.get("evaluation")
                if not isinstance(evaluation, Mapping):
                    raise ValueError(f"line {line_number} lacks evaluation")
                exact_match = evaluation.get("exact_match")
                if not isinstance(exact_match, bool):
                    raise ValueError(
                        f"line {line_number} has non-boolean exact_match"
                    )

                num_input += 1
                input_counts[query_index] = input_counts.get(query_index, 0) + 1
                if exact_match:
                    output_handle.write(
                        json.dumps(record, ensure_ascii=False) + "\n"
                    )
                    num_correct += 1
                    correct_counts[query_index] = (
                        correct_counts.get(query_index, 0) + 1
                    )

        temporary_output.replace(output_path)
    except Exception:
        temporary_output.unlink(missing_ok=True)
        raise

    per_query = [
        {
            "query_index": query_index,
            "query": queries[query_index],
            "num_input_contexts": input_counts[query_index],
            "num_correct_contexts": correct_counts.get(query_index, 0),
        }
        for query_index in sorted(queries)
    ]
    summary: dict[str, Any] = {
        "task": task,
        "input": str(input_path),
        "output": str(output_path),
        "selection": {
            "field": "evaluation.exact_match",
            "equals": True,
            "meaning": "complete_generated_answer_exact_match",
        },
        "num_input_prompt_instances": num_input,
        "num_correct_prompt_instances": num_correct,
        "num_unique_queries_in_input": len(queries),
        "num_unique_queries_with_correct_instance": len(correct_counts),
        "correct_contexts_per_query": per_query,
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return summary


def main() -> None:
    """Resolve task-default paths, run selection, and print concise counts."""

    args = parse_args()
    task = get_task_spec(args.task).dataset_task
    task_directory = PROJECT_DIR / "results" / task
    summary = select_correct_instances(
        task=task,
        input_path=args.input or task_directory / "baseline_evaluation.jsonl.gz",
        output_path=args.output or task_directory / "correct_instances.jsonl.gz",
        summary_path=(
            args.summary_output
            or task_directory / "correct_instances_summary.json"
        ),
        overwrite=args.overwrite,
    )
    concise = {
        key: value
        for key, value in summary.items()
        if key != "correct_contexts_per_query"
    }
    print(json.dumps(concise, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
