from __future__ import annotations

import sys
import unittest
from pathlib import Path

import torch

EXPERIMENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(EXPERIMENT_DIR))

from multipath.gradient import (directional_gradient_scores, full_answer_log_probability,
    select_gradient_records, selected_vocabulary_rankings, target_answer_for_record,
    unit_transported_directions)


class GradientTests(unittest.TestCase):
    def test_full_answer_log_probability_scores_every_token(self) -> None:
        logits = torch.tensor([[2.0, 0.0, -1.0], [0.0, 1.0, 3.0]], requires_grad=True)
        value = full_answer_log_probability(logits, [0, 2])
        expected = logits.log_softmax(-1)[0, 0] + logits.log_softmax(-1)[1, 2]
        self.assertTrue(torch.allclose(value, expected))
        value.backward()
        self.assertIsNotNone(logits.grad)
        self.assertTrue(bool((logits.grad[0] != 0).any()))
        self.assertTrue(bool((logits.grad[1] != 0).any()))

    def test_transport_orientation_and_normalization(self) -> None:
        jacobian = torch.tensor([[2.0, 0.0], [1.0, 1.0]])
        rows = torch.tensor([[1.0, 0.0], [0.0, 1.0]])
        directions = unit_transported_directions(jacobian, rows)
        expected = torch.tensor([[1.0, 0.0], [1.0, 1.0]])
        expected = expected / expected.norm(dim=1, keepdim=True)
        self.assertTrue(torch.allclose(directions, expected))
        self.assertTrue(torch.allclose(directions.norm(dim=1), torch.ones(2)))

    def test_directional_scores_are_first_order_dot_products(self) -> None:
        directions = torch.tensor([[1.0, 0.0], [0.0, 1.0], [2 ** -0.5, 2 ** -0.5]])
        scores = directional_gradient_scores(torch.tensor([3.0, -1.0]), directions)
        self.assertTrue(torch.allclose(scores, torch.tensor([3.0, -1.0, 2 ** 0.5])))

    def test_selected_rankings_use_full_vocabulary_and_tie_best_rank(self) -> None:
        scores = torch.tensor([0.0, 3.0, 1.0, 3.0, -2.0])
        rows = selected_vocabulary_rankings(scores, [1, 2, 4], ["one", "two", "four"])
        self.assertEqual([row["full_vocabulary_rank"] for row in rows], [1, 3, 5])
        self.assertEqual([row["predicted_effect"] for row in rows], ["increase", "increase", "decrease"])
        self.assertEqual(rows[0]["word"], "one")
        self.assertEqual(rows[0]["full_vocabulary_percentile"], 1.0)

    def test_rejects_non_unit_directions(self) -> None:
        with self.assertRaisesRegex(ValueError, "unit norm"):
            directional_gradient_scores(torch.tensor([1.0, 2.0]), torch.tensor([[2.0, 0.0]]))

    def test_target_modes_and_ineligible_model_answers(self) -> None:
        row = {"true_answer": "Berlin", "model_answer_normalized": " Munich ",
               "answer_status": "eligible_wrong"}
        self.assertEqual(target_answer_for_record(row, "true"), "Berlin")
        self.assertEqual(target_answer_for_record(row, "model"), "Munich")
        self.assertIsNone(target_answer_for_record({**row, "answer_status": "ineligible"}, "model"))

    def test_prompt_shard_is_selected_after_split_and_eligibility(self) -> None:
        records = [
            {"task": "task", "split": "selection", "prompt_instance_id": "a",
             "true_answer": "A", "model_answer_normalized": "A", "answer_status": "correct"},
            {"task": "task", "split": "test", "prompt_instance_id": "b",
             "true_answer": "B", "model_answer_normalized": "noise", "answer_status": "ineligible"},
            {"task": "task", "split": "test", "prompt_instance_id": "c",
             "true_answer": "C", "model_answer_normalized": "wrong", "answer_status": "eligible_wrong"},
            {"task": "task", "split": "test", "prompt_instance_id": "d",
             "true_answer": "D", "model_answer_normalized": "answer", "answer_status": "correct"},
        ]
        selected = select_gradient_records(
            records, task="task", split="test", target_mode="model",
            association_answers={"wrong", "answer"}, start_index=1, num_prompts=1)
        self.assertEqual(selected[0]["prompt_instance_id"], "d")
        self.assertEqual(selected[0]["gradient_target_answer"], "answer")


if __name__ == "__main__":
    unittest.main()
