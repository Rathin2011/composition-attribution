"""Focused tests for the shared OLMo baseline evaluator."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import torch

from evaluate_baseline import (
    CandidateValues,
    RunningSummary,
    candidate_values,
    leading_space_token_ids,
    open_text,
    read_jsonl,
    selected_logits,
    token_measurement,
    tokenize_candidates,
)


class FakeTokenizer:
    def encode(self, text: str, *, add_special_tokens: bool) -> list[int]:
        self.calls.append((text, add_special_tokens))
        return [len(text), 99] if "United" in text else [len(text)]

    def __init__(self) -> None:
        self.calls = []


class BaselineTest(unittest.TestCase):
    def test_gzip_jsonl_round_trip(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "rows.jsonl.gz"
            expected = [{"row": 1}, {"row": 2}]
            with open_text(path, "wt") as handle:
                for row in expected:
                    handle.write(json.dumps(row) + "\n")
            self.assertEqual(list(read_jsonl(path)), expected)

    def test_derives_stable_complete_candidate_order(self) -> None:
        rows = [
            {
                "task": "test-task",
                "query": {"x": "x1", "Fx": "b", "GFx": "B"},
            },
            {
                "task": "test-task",
                "query": {"x": "x2", "Fx": "a", "GFx": "A"},
            },
            {
                "task": "test-task",
                "query": {"x": "x1", "Fx": "b", "GFx": "B"},
            },
        ]
        with TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.jsonl"
            path.write_text("".join(json.dumps(row) + "\n" for row in rows))
            values = candidate_values(path, "test-task")
        self.assertEqual(values.x, ("x1", "x2"))
        self.assertEqual(values.Fx, ("b", "a"))
        self.assertEqual(values.GFx, ("B", "A"))

    def test_catalog_preserves_complete_multitoken_encoding(self) -> None:
        tokenizer = FakeTokenizer()
        catalog = tokenize_candidates(
            tokenizer,
            CandidateValues("landmark-country-capital", ("x",), ("United Kingdom", "Italy"), ("A",)),
        )
        self.assertEqual(catalog["Fx"][0]["token_ids"], [15, 99])
        self.assertEqual(catalog["measurement"], "first_token_with_leading_space")
        self.assertEqual(leading_space_token_ids(tokenizer, "Italy"), [6])

    def test_saves_all_candidate_logits_in_catalog_order(self) -> None:
        logits = torch.tensor([0.0, 1.0, 2.0, 3.0])
        self.assertEqual(selected_logits(logits, [3, 1, 2]), [3.0, 1.0, 2.0])

    def test_rank_is_against_full_vocabulary(self) -> None:
        logits = torch.tensor([0.0, 3.0, 1.0, 2.0])
        result = token_measurement(logits, 3, (1, 2, 5))
        self.assertEqual(result["rank"], 2)
        self.assertEqual(result["reciprocal_rank"], 0.5)
        self.assertEqual(result["in_top_k"], {"1": False, "2": True, "5": True})

    def test_summary_counts_complete_answer_accuracy(self) -> None:
        summary = RunningSummary((1, 5))
        summary.add(
            {
                "evaluation": {
                    "exact_match": True,
                    "final_next_token_readout": {
                        "target_GFx_first_token": {
                            "rank": 3,
                            "in_top_k": {"1": False, "5": True},
                        }
                    },
                }
            }
        )
        output = summary.as_dict()
        self.assertEqual(output["num_exact_correct"], 1)
        self.assertEqual(output["exact_accuracy"], 1.0)


if __name__ == "__main__":
    unittest.main()
