"""Contract tests for generalized Logit-Lens evaluation helpers."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import torch

from evaluate_baseline import open_text
from evaluate_logit_lens import (
    classify_rank,
    classify_reciprocal_rank,
    load_fx_catalog,
    paper_token_filter_reason,
    read_correct_slice,
    select_best_position_values,
)


class Tokenizer:
    def encode(self, text: str, *, add_special_tokens: bool) -> list[int]:
        if add_special_tokens:
            raise AssertionError
        return {" A": [10], " B": [20]}[text]


def correct_row(prompt_id: str, task: str = "test-task") -> dict:
    return {
        "prompt_instance_id": prompt_id,
        "task": task,
        "prompt": "Q: x\nA: y\n\nQ: x\nA:",
        "query": {"x": "x", "Fx": "A", "GFx": "y"},
        "evaluation": {"exact_match": True},
    }


class EvaluateLogitLensTest(unittest.TestCase):
    def test_reads_compressed_correct_slice(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "correct.jsonl.gz"
            with open_text(path, "wt") as handle:
                for index in range(3):
                    handle.write(json.dumps(correct_row(f"p{index}")) + "\n")
            rows = list(
                read_correct_slice(path, task="test-task", start_index=1, num_records=1)
            )
        self.assertEqual([row["prompt_instance_id"] for row in rows], ["p1"])

    def test_loads_catalog_and_checks_tokenizer_ids(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "summary.json"
            path.write_text(
                json.dumps(
                    {
                        "task": "landmark-country-capital",
                        "candidate_catalog": {
                            "Fx": [
                                {"value": "A", "token_ids": [10]},
                                {"value": "B", "token_ids": [20]},
                            ]
                        },
                    }
                )
            )
            catalog = load_fx_catalog(path, task="landmark-country-capital", tokenizer=Tokenizer())
        self.assertEqual([row["value"] for row in catalog], ["A", "B"])

    def test_selects_one_shared_position_per_layer(self) -> None:
        # P=2 positions, L=2 layers, K=3 candidate Fx values.
        logits = torch.tensor(
            [
                [[10.0, 11.0, 12.0], [20.0, 21.0, 22.0]],
                [[30.0, 31.0, 32.0], [40.0, 41.0, 42.0]],
            ]
        )
        ranks = torch.tensor(
            [
                [[9, 2, 8], [9, 5, 8]],
                [[9, 4, 8], [9, 1, 8]],
            ]
        )
        z, rr, positions = select_best_position_values(logits, ranks, target_index=1)
        self.assertEqual(positions, [0, 1])
        self.assertEqual(z, [[10.0, 40.0], [11.0, 41.0], [12.0, 42.0]])
        self.assertEqual(rr, [0.5, 1.0])

    def test_position_ties_choose_the_earliest_query_token(self) -> None:
        logits = torch.tensor([[[1.0, 2.0]], [[3.0, 4.0]]])
        ranks = torch.tensor([[[9, 2]], [[8, 2]]])
        z, rr, positions = select_best_position_values(logits, ranks, target_index=1)
        self.assertEqual(positions, [0])
        self.assertEqual(z, [[1.0], [2.0]])
        self.assertEqual(rr, [0.5])

    def test_rank_five_returns_exact_threshold_value(self) -> None:
        logits = torch.tensor([[[1.0]]])
        ranks = torch.tensor([[[5]]])
        _, rr, _ = select_best_position_values(logits, ranks, target_index=0)
        self.assertEqual(rr, [0.2])
        self.assertEqual(classify_rank(5), "shortcut_candidate")

    def test_thresholds_and_paper_filter(self) -> None:
        self.assertEqual(classify_rank(2), "compositional")
        self.assertEqual(classify_rank(3), "ambiguous")
        self.assertEqual(classify_rank(4), "ambiguous")
        self.assertEqual(classify_rank(5), "shortcut_candidate")
        self.assertEqual(classify_reciprocal_rank(0.5), "compositional")
        self.assertEqual(classify_reciprocal_rank(0.25), "ambiguous")
        self.assertEqual(classify_reciprocal_rank(0.2), "shortcut_candidate")
        token_info = {
            "x": {"first_token_id": 1, "token_ids": [1, 2]},
            "Fx": {"first_token_id": 2, "token_ids": [2]},
            "GFx": {"first_token_id": 3, "token_ids": [3]},
        }
        self.assertEqual(
            paper_token_filter_reason(token_info),
            "target_first_token_occurs_inside_x",
        )


if __name__ == "__main__":
    unittest.main()
