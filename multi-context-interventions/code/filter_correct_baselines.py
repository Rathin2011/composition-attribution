"""Select correctly answered query-context instances from baseline results.

Input:
    ``baseline_full.jsonl``. Each row is one complete query-context record with
    its baseline evaluation.

Output:
    ``correct_query_contexts.jsonl`` containing the original rows for which
    ``evaluation.exact_match`` is true, plus a compact JSON summary.

This step does not alter prompts, recompute model outputs, calculate lens
scores, or classify a record as compositional or shortcut.
"""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path
from typing import Any, Iterable


PROJECT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = PROJECT_DIR / "results" / "baseline_full.jsonl"
DEFAULT_OUTPUT = PROJECT_DIR / "results" / "correct_query_contexts.jsonl"
DEFAULT_SUMMARY = PROJECT_DIR / "results" / "correct_query_contexts_summary.json"
DEFAULT_EXPECTED_INPUT_COUNT = 13_850
DEFAULT_EXPECTED_CORRECT_COUNT = 5_491


def parse_args() -> argparse.Namespace:
    """Parse input, output, and expected-count validation options."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument(
        "--expected-input-count", type=int, default=DEFAULT_EXPECTED_INPUT_COUNT
    )
    parser.add_argument(
        "--expected-correct-count", type=int, default=DEFAULT_EXPECTED_CORRECT_COUNT
    )
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    """Read a JSONL file and require every nonempty line to be an object."""

    records = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError(f"{path}:{line_number} is not a JSON object")
            records.append(record)
    return records


def validate_baseline_record(record: dict[str, Any], index: int) -> None:
    """Require the identity, prompt data, and exact-match field used here."""

    required = {
        "prompt_instance_id",
        "query_index",
        "context_variant",
        "query",
        "context",
        "prompt",
        "evaluation",
    }
    missing = required - record.keys()
    if missing:
        raise ValueError(f"record {index} is missing fields: {sorted(missing)}")
    evaluation = record["evaluation"]
    if not isinstance(evaluation, dict):
        raise ValueError(f"record {index} evaluation is not an object")
    if not isinstance(evaluation.get("exact_match"), bool):
        raise ValueError(f"record {index} exact_match is not Boolean")


def filter_correct_records(
    records: Iterable[dict[str, Any]],
    *,
    expected_input_count: int | None = None,
    expected_correct_count: int | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Validate records and return unchanged rows with exact correct answers."""

    correct_records: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    all_query_indices: set[int] = set()
    correct_counts_by_query: collections.Counter[int] = collections.Counter()
    input_count = 0

    for input_count, record in enumerate(records, start=1):
        validate_baseline_record(record, input_count)
        prompt_id = record["prompt_instance_id"]
        if prompt_id in seen_ids:
            raise ValueError(f"duplicate prompt_instance_id: {prompt_id!r}")
        seen_ids.add(prompt_id)

        query_index = int(record["query_index"])
        all_query_indices.add(query_index)
        if record["evaluation"]["exact_match"]:
            # Keep the complete original object, including its context, prompt,
            # generated answer, and all final-readout measurements.
            correct_records.append(record)
            correct_counts_by_query[query_index] += 1

    if expected_input_count is not None and input_count != expected_input_count:
        raise ValueError(
            f"expected {expected_input_count} input rows, found {input_count}"
        )
    if (
        expected_correct_count is not None
        and len(correct_records) != expected_correct_count
    ):
        raise ValueError(
            f"expected {expected_correct_count} correct rows, "
            f"found {len(correct_records)}"
        )

    count_histogram = collections.Counter(
        correct_counts_by_query.get(query_index, 0)
        for query_index in all_query_indices
    )
    summary = {
        "num_input_prompt_instances": input_count,
        "num_unique_input_prompt_instance_ids": len(seen_ids),
        "num_correct_prompt_instances": len(correct_records),
        "correct_fraction": len(correct_records) / (input_count or 1),
        "num_queries": len(all_query_indices),
        "num_queries_with_at_least_one_correct_context": sum(
            count > 0 for count in correct_counts_by_query.values()
        ),
        "correct_context_count_histogram": {
            str(count): number_of_queries
            for count, number_of_queries in sorted(count_histogram.items())
        },
    }
    return correct_records, summary


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    """Write records as one JSON object per line."""

    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )


def main() -> None:
    args = parse_args()
    destinations = (args.output, args.summary_output)
    existing = [str(path) for path in destinations if path.exists()]
    if existing and not args.overwrite:
        raise FileExistsError(
            "outputs already exist; pass --overwrite: " + ", ".join(existing)
        )
    for path in destinations:
        path.parent.mkdir(parents=True, exist_ok=True)

    correct_records, summary = filter_correct_records(
        read_jsonl(args.input),
        expected_input_count=args.expected_input_count,
        expected_correct_count=args.expected_correct_count,
    )
    summary = {
        "input": str(args.input),
        "output": str(args.output),
        "selection_rule": "evaluation.exact_match == true",
        "records_preserved_without_modification": True,
        **summary,
    }
    write_jsonl(args.output, correct_records)
    args.summary_output.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))
    print(f"Wrote {args.output}")
    print(f"Wrote {args.summary_output}")


if __name__ == "__main__":
    main()
