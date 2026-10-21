"""CPU-only contract tests for generalized J-Lens evaluation."""

from __future__ import annotations

import types
import unittest

import torch

from evaluate_jlens import (
    RunningSummary,
    analyze_record,
    candidate_logits_and_ranks,
    excluded_result,
    validate_loaded_lens,
    validate_logit_lens_record,
)


SOURCE_LAYERS = (12, 16)


def eligible_record() -> dict:
    return {
        "prompt_instance_id": "p0",
        "task": "landmark-country-capital",
        "prompt": "Q: Demo\nA: Paris\n\nQ: Landmark\nA:",
        "query": {"x": "Landmark", "Fx": "Country", "GFx": "Capital"},
        "evaluation": {"exact_match": True},
        "logit_lens": {
            "paper_token_eligible": True,
            "paper_token_filter_reason": None,
            "query_token_start": 4,
            "num_query_positions": 2,
            "classification": {"group": "compositional"},
            "node_token_info": {
                "x": {"value": "Landmark", "first_token_id": 0},
                "Fx": {"value": "Country", "first_token_id": 1},
                "GFx": {"value": "Capital", "first_token_id": 2},
            },
        },
    }


def excluded_record() -> dict:
    record = eligible_record()
    record["logit_lens"] = {
        "paper_token_eligible": False,
        "paper_token_filter_reason": "node_first_tokens_overlap",
        "classification": None,
        "node_token_info": {},
    }
    return record


class FakeLens:
    def __init__(self, logits_by_layer: dict[int, torch.Tensor]) -> None:
        self.logits_by_layer = logits_by_layer
        self.calls = []

    def apply(self, adapter, prompt, **kwargs):
        self.calls.append((adapter, prompt, kwargs))
        return self.logits_by_layer, torch.empty(0), torch.zeros(1, 8)


class EvaluateJLensTest(unittest.TestCase):
    def test_candidate_values_and_full_vocabulary_ranks(self) -> None:
        logits = {
            12: torch.tensor(
                [[3.0, 2.0, 2.0, 0.0], [0.0, 4.0, 1.0, 2.0]]
            ),
            16: torch.tensor(
                [[1.0, 0.0, 5.0, 2.0], [2.0, 3.0, 0.0, 1.0]]
            ),
        }
        selected, ranks = candidate_logits_and_ranks(
            logits,
            [0, 1, 2],
            SOURCE_LAYERS,
            candidate_chunk_size=2,
        )
        self.assertEqual(tuple(selected.shape), (2, 2, 3))
        self.assertEqual(tuple(ranks.shape), (2, 2, 3))
        torch.testing.assert_close(ranks[0, 0], torch.tensor([1, 2, 2]))
        torch.testing.assert_close(ranks[1, 1], torch.tensor([2, 1, 4]))

    def test_analyze_uses_saved_span_and_one_shared_position_per_layer(self) -> None:
        logits = {
            12: torch.tensor(
                [[5.0, 4.0, 0.0, 1.0], [1.0, 2.0, 3.0, 0.0]]
            ),
            16: torch.tensor(
                [[4.0, 1.0, 0.0, 2.0], [0.0, 5.0, 3.0, 1.0]]
            ),
        }
        lens = FakeLens(logits)
        catalog = [
            {"value": "Other", "token_ids": [0]},
            {"value": "Country", "token_ids": [1]},
            {"value": "Third", "token_ids": [2]},
        ]
        result = analyze_record(
            lens,
            object(),
            eligible_record(),
            catalog,
            source_layers=SOURCE_LAYERS,
            max_seq_len=512,
            candidate_chunk_size=2,
        )
        self.assertEqual(
            lens.calls[0][2],
            {
                "layers": [12, 16],
                "positions": [4, 5],
                "max_seq_len": 512,
                "use_jacobian": True,
            },
        )
        measurement = result["j_lens"]
        self.assertEqual(measurement["selected_query_position_by_layer"], [0, 1])
        self.assertEqual(
            measurement["jlens_z"],
            [[5.0, 0.0], [4.0, 5.0], [0.0, 3.0]],
        )
        self.assertEqual(measurement["jlens_rr"], [0.5, 1.0])
        self.assertEqual(measurement["classification"]["group"], "compositional")
        self.assertEqual(measurement["classification"]["peak_layers"], [16])

    def test_validation_exclusion_and_transition_summary(self) -> None:
        validate_logit_lens_record(eligible_record())
        excluded = excluded_result(excluded_record())
        self.assertIsNone(excluded["j_lens"]["jlens_z"])

        eligible = eligible_record()
        eligible["j_lens"] = {
            "paper_token_eligible": True,
            "classification": {"group": "shortcut_candidate"},
        }
        summary = RunningSummary()
        summary.add(eligible)
        summary.add(excluded)
        values = summary.as_dict()
        self.assertEqual(values["classification_counts"]["shortcut_candidate"], 1)
        self.assertEqual(
            values["logit_lens_to_j_lens_transitions"],
            {"compositional->shortcut_candidate": 1},
        )

    def test_loaded_lens_contract(self) -> None:
        lens = types.SimpleNamespace(
            source_layers=(12, 16, 18, 20, 22, 24),
            n_prompts=1000,
            d_model=4096,
            jacobians={
                layer: torch.empty(4096, 4096, device="meta")
                for layer in (12, 16, 18, 20, 22, 24)
            },
        )
        self.assertEqual(validate_loaded_lens(lens), lens.source_layers)
        lens.n_prompts = 999
        with self.assertRaisesRegex(ValueError, "1000 fitting prompts"):
            validate_loaded_lens(lens)


if __name__ == "__main__":
    unittest.main()
