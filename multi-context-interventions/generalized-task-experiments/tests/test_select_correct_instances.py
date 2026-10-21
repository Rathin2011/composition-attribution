"""Focused tests for freezing exact-correct baseline instances."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from evaluate_baseline import open_text, read_jsonl
from select_correct_instances import select_correct_instances


def baseline_row(
    prompt_id: str,
    query_index: int,
    *,
    exact_match: bool,
    task: str = "test-task",
) -> dict:
    """Build the minimum realistic baseline row used by these tests."""

    return {
        "prompt_instance_id": prompt_id,
        "task": task,
        "query_index": query_index,
        "context_variant": int(prompt_id.rsplit("-", 1)[-1]),
        "query": {
            "x": f"x-{query_index}",
            "Fx": f"middle-{query_index}",
            "GFx": f"answer-{query_index}",
        },
        "context": [],
        "prompt": f"Q: x-{query_index}\nA:",
        "evaluation": {
            "prediction": f" answer-{query_index}",
            "label": f" answer-{query_index}",
            "exact_match": exact_match,
        },
    }


def write_jsonl(path: Path, rows: list[dict]) -> None:
    """Write test rows using the production plain/gzip helper."""

    with open_text(path, "wt") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")


class SelectCorrectInstancesTest(unittest.TestCase):
    def test_preserves_only_exact_matches_and_reports_every_query(self) -> None:
        rows = [
            baseline_row("query-0-0", 0, exact_match=True),
            baseline_row("query-0-1", 0, exact_match=False),
            baseline_row("query-1-0", 1, exact_match=False),
            baseline_row("query-1-1", 1, exact_match=False),
        ]
        with TemporaryDirectory() as directory:
            root = Path(directory)
            input_path = root / "baseline.jsonl.gz"
            output_path = root / "correct.jsonl.gz"
            summary_path = root / "summary.json"
            write_jsonl(input_path, rows)

            summary = select_correct_instances(
                task="test-task",
                input_path=input_path,
                output_path=output_path,
                summary_path=summary_path,
            )

            self.assertEqual(list(read_jsonl(output_path)), [rows[0]])
            self.assertEqual(summary["num_input_prompt_instances"], 4)
            self.assertEqual(summary["num_correct_prompt_instances"], 1)
            self.assertEqual(summary["num_unique_queries_in_input"], 2)
            self.assertEqual(summary["num_unique_queries_with_correct_instance"], 1)
            self.assertEqual(
                [row["num_correct_contexts"] for row in summary["correct_contexts_per_query"]],
                [1, 0],
            )
            self.assertEqual(json.loads(summary_path.read_text()), summary)

    def test_rejects_duplicate_prompt_instance_ids(self) -> None:
        row = baseline_row("query-0-0", 0, exact_match=True)
        with TemporaryDirectory() as directory:
            root = Path(directory)
            input_path = root / "baseline.jsonl"
            write_jsonl(input_path, [row, row])
            with self.assertRaisesRegex(ValueError, "duplicate prompt_instance_id"):
                select_correct_instances(
                    task="test-task",
                    input_path=input_path,
                    output_path=root / "correct.jsonl.gz",
                    summary_path=root / "summary.json",
                )
            self.assertFalse((root / "correct.jsonl.gz").exists())

    def test_rejects_task_mismatch(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            input_path = root / "baseline.jsonl"
            write_jsonl(
                input_path,
                [baseline_row("query-0-0", 0, exact_match=True, task="wrong")],
            )
            with self.assertRaisesRegex(ValueError, "expected 'test-task'"):
                select_correct_instances(
                    task="test-task",
                    input_path=input_path,
                    output_path=root / "correct.jsonl.gz",
                    summary_path=root / "summary.json",
                )


if __name__ == "__main__":
    unittest.main()
