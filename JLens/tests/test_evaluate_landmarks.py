"""Focused tests for landmark J-Lens evaluation helpers."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

import torch

from jlens_experiments.compatibility import MODEL_COMMIT
from jlens_experiments.evaluate_landmarks import (
    DEFAULT_LENS,
    aggregate,
    country_candidates,
    country_entity_target_ranks,
    evidence_band,
    measure_country_tokens,
    read_group,
    stored_logit_lens,
    summarize_readout,
    target_ranks,
)


class EvaluateLandmarksTests(unittest.TestCase):
    def test_default_lens_is_merged_1000_prompt_fit(self) -> None:
        self.assertEqual(
            DEFAULT_LENS.parts[-4:],
            ("results", "fit_1000", "merged", "jacobian_lens.pt"),
        )

    def test_target_ranks_use_one_based_shared_best_rank(self) -> None:
        logits = torch.tensor([[1.0, 3.0, 2.0], [4.0, 4.0, 0.0]])
        self.assertEqual(target_ranks(logits, 0), [3, 1])

    def test_country_entity_rank_uses_mean_over_complete_label(self) -> None:
        # The target's first token (1.0) trails the competing country (2.0),
        # but its complete two-token label has the higher mean score (3.0).
        logits = torch.tensor([[1.0, 5.0, 2.0], [1.0, 1.0, 2.0]])
        self.assertEqual(country_entity_target_ranks(logits, [[0, 1], [2]], 0), [1, 2])

    def test_summarize_readout_takes_best_position_and_layer(self) -> None:
        result = summarize_readout({12: [10, 4], 18: [2, 8]})
        self.assertEqual(result["best_rank"], 2)
        self.assertEqual(result["peak_layers"], [18])
        self.assertEqual(result["evidence_band"], "compositional")

    def test_evidence_bands_match_saved_analysis(self) -> None:
        self.assertEqual(evidence_band(0.5), "compositional")
        self.assertEqual(evidence_band(0.25), "ambiguous")
        self.assertEqual(evidence_band(0.2), "shortcut_candidate")

    def test_measure_country_tokens_keeps_tokens_separate(self) -> None:
        logits = {
            12: torch.tensor([[3.0, 2.0, 1.0], [1.0, 4.0, 2.0]]),
            18: torch.tensor([[1.0, 2.0, 3.0], [3.0, 2.0, 1.0]]),
        }
        result = measure_country_tokens(logits, [0, 2], [" United", " Kingdom"])
        self.assertEqual([item["token"] for item in result], [" United", " Kingdom"])
        self.assertEqual(result[0]["j_lens"]["best_rank"], 1)
        self.assertEqual(result[1]["j_lens"]["best_rank"], 1)

    def test_country_candidates_are_sorted_and_require_consistent_tokens(self) -> None:
        def row(country: str, token_ids: list[int]) -> dict:
            return {
                "query": {"Fx": country},
                "node_evidence": {"Fx": {"token_ids": token_ids}},
            }

        self.assertEqual(
            country_candidates([row("Zulu", [2]), row("Alpha", [1]), row("Zulu", [2])]),
            {"Alpha": (1,), "Zulu": (2,)},
        )
        with self.assertRaises(ValueError):
            country_candidates([row("Zulu", [2]), row("Zulu", [3])])

    def test_stored_logit_lens_selects_requested_layers(self) -> None:
        record = {
            "node_evidence": {
                "Fx": {"layerwise_max_reciprocal_rank": [0.1, 0.5, 0.25]}
            }
        }
        result = stored_logit_lens(record, [1, 2])
        self.assertEqual(result["best_rank"], 2)
        self.assertEqual(result["peak_layers"], [1])

    def test_read_group_validates_count_and_identity(self) -> None:
        record = {
            "model_commit": MODEL_COMMIT,
            "classification": {"group": "compositional"},
            "prediction": {"prompt": "Q: landmark\nA:"},
            "query": {"Fx": "Country"},
            "node_evidence": {"Fx": {"first_token_id": 7, "token_ids": [7]}},
            "query_token_start": 2,
            "num_query_positions": 1,
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "records.jsonl"
            path.write_text(json.dumps(record) + "\n", encoding="utf-8")
            self.assertEqual(len(read_group(path, "compositional", 1)), 1)
            with self.assertRaises(ValueError):
                read_group(path, "compositional", 2)

    def test_aggregate_compares_paired_best_ranks(self) -> None:
        def row(old: int, new: int) -> dict:
            return {
                "original_group": "compositional",
                "logit_lens_fitted_layers": {"best_rank": old},
                "j_lens": {
                    "best_rank": new,
                    "evidence_band": evidence_band(1.0 / new),
                },
            }

        summary = aggregate([row(5, 2), row(2, 2), row(1, 4)], "compositional")
        self.assertEqual(summary["j_lens_better_rank"], 1)
        self.assertEqual(summary["same_rank"], 1)
        self.assertEqual(summary["j_lens_worse_rank"], 1)


if __name__ == "__main__":
    unittest.main()
