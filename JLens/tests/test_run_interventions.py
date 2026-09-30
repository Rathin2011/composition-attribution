"""Unit tests for the end-to-end intervention runner's pure logic."""

from __future__ import annotations

import argparse
from types import SimpleNamespace
import unittest

import torch

from jlens_experiments.run_interventions import (
    answer_from_completion,
    country_capital_pairs,
    greedy_completion,
    intervention_positions,
    resolve_swap_target,
    summarize_group,
    token_measurement,
    validate_settings,
)
from jlens_experiments.interventions import LayerIntervention


def settings(**overrides):
    values = {
        "layers": [12, 18],
        "kind": "ablate",
        "coefficient": None,
        "strength": None,
        "max_new_tokens": 20,
        "max_seq_len": 512,
        "progress_every": 10,
        "max_queries": None,
        "token_scope": "final",
        "allow_multitoken_country": False,
        "swap_target_country": "Japan",
        "swap_scale": None,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


class ValidateSettingsTests(unittest.TestCase):
    def test_ablation_defaults_to_full_projection(self) -> None:
        result = validate_settings(settings(), [12, 16, 18])
        self.assertEqual(result["layers"], [12, 18])
        self.assertEqual(result["strength"], 1.0)
        self.assertIsNone(result["coefficient"])

    def test_steering_requires_coefficient(self) -> None:
        with self.assertRaisesRegex(ValueError, "coefficient"):
            validate_settings(settings(kind="steer"), [12, 18])

    def test_unknown_lens_layer_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "absent"):
            validate_settings(settings(layers=[20]), [12, 18])

    def test_swap_defaults_to_full_swap_with_japan(self) -> None:
        result = validate_settings(settings(kind="swap"), [12, 18])
        self.assertEqual(result["swap_target_country"], "Japan")
        self.assertEqual(result["swap_scale"], 1.0)
        self.assertIsNone(result["strength"])
        self.assertIsNone(result["coefficient"])

    def test_swap_rejects_ablation_or_steering_arguments(self) -> None:
        with self.assertRaisesRegex(ValueError, "does not accept"):
            validate_settings(settings(kind="swap", strength=0.5), [12, 18])


class SwapTargetTests(unittest.TestCase):
    def test_pairs_include_context_and_query_examples(self) -> None:
        records = [
            {
                "context": [{"Fx": "Japan", "GFx": "Tokyo"}],
                "query": {"Fx": "Egypt", "GFx": "Cairo"},
            }
        ]
        self.assertEqual(
            country_capital_pairs(records),
            {"Japan": "Tokyo", "Egypt": "Cairo"},
        )

    def test_target_resolution_is_case_insensitive(self) -> None:
        self.assertEqual(
            resolve_swap_target("japan", {"Japan": "Tokyo"}),
            ("Japan", "Tokyo"),
        )


class PositionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = {"query_token_start": 7, "num_query_positions": 3}

    def test_final_scope(self) -> None:
        self.assertEqual(intervention_positions(self.record, "final"), (-1,))

    def test_query_scope(self) -> None:
        self.assertEqual(intervention_positions(self.record, "query"), (7, 8, 9))

    def test_all_scope(self) -> None:
        self.assertIsNone(intervention_positions(self.record, "all"))


class MeasurementTests(unittest.TestCase):
    def test_token_measurement_uses_full_vocabulary(self) -> None:
        result = token_measurement(torch.tensor([0.0, 2.0, 1.0]), token_id=2)
        self.assertEqual(result["rank"], 2)
        self.assertAlmostEqual(result["logit"], 1.0)
        self.assertAlmostEqual(
            result["probability"],
            torch.tensor([0.0, 2.0, 1.0]).softmax(-1)[2].item(),
        )

    def test_answer_uses_double_newline_boundary(self) -> None:
        self.assertEqual(answer_from_completion(" Paris\n\nQ:"), " Paris")

    def test_summary_aggregates_effect_direction(self) -> None:
        rows = [
            {
                "group": "compositional",
                "baseline": {"exact_match": True},
                "intervention": {"exact_match": False},
                "change": {
                    "generated_answer_changed": True,
                    "correct_token_logit": -2.0,
                    "correct_token_log_probability": -1.0,
                    "correct_token_probability": -0.2,
                },
            },
            {
                "group": "compositional",
                "baseline": {"exact_match": True},
                "intervention": {"exact_match": True},
                "change": {
                    "generated_answer_changed": False,
                    "correct_token_logit": 0.0,
                    "correct_token_log_probability": 0.0,
                    "correct_token_probability": 0.0,
                },
            },
        ]
        summary = summarize_group(rows, "compositional")
        self.assertEqual(summary["baseline_exact"], 2)
        self.assertEqual(summary["intervention_exact"], 1)
        self.assertEqual(summary["generated_answer_changed"], 1)
        self.assertEqual(summary["mean_correct_token_logit_change"], -1.0)


class GreedyCompletionTests(unittest.TestCase):
    def test_intervention_changes_initial_logits_and_generated_token(self) -> None:
        class TinyTokenizer:
            eos_token_id = 2

            def decode(self, token_ids, **kwargs):
                return "".join({0: " A", 1: " B", 2: ""}[item] for item in token_ids)

        class TinyModel(torch.nn.Module):
            def __init__(self) -> None:
                super().__init__()
                self.block = torch.nn.Identity()

            def forward(self, input_ids, past_key_values=None, use_cache=True):
                batch, sequence = input_ids.shape
                hidden = self.block(torch.zeros(batch, sequence, 2))
                logits = torch.zeros(batch, sequence, 3)
                logits[..., 0] = hidden[..., 0]
                logits[..., 1] = 1.0
                return SimpleNamespace(logits=logits, past_key_values=())

        model = TinyModel()
        tokenizer = TinyTokenizer()
        input_ids = torch.tensor([[7, 8]])
        baseline_logits, baseline_completion = greedy_completion(
            model,
            tokenizer,
            input_ids,
            max_new_tokens=1,
        )
        intervention = LayerIntervention(
            [model.block],
            layer_index=0,
            token_positions=(-1,),
            direction=torch.tensor([1.0, 0.0]),
            kind="steer",
            coefficient=2.0,
        )
        edited_logits, edited_completion = greedy_completion(
            model,
            tokenizer,
            input_ids,
            max_new_tokens=1,
            interventions=(intervention,),
        )

        self.assertEqual(baseline_completion, " B")
        self.assertEqual(edited_completion, " A")
        self.assertEqual(int(baseline_logits.argmax().item()), 1)
        self.assertEqual(int(edited_logits.argmax().item()), 0)


if __name__ == "__main__":
    unittest.main()
