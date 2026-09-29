"""Focused tests for ordinary logit-lens country-entity evaluation."""

from __future__ import annotations

import unittest

import torch

from jlens_experiments.evaluate_logit_lens_country_entities import (
    aggregate_entity,
    full_vocabulary_entity_target_ranks,
)


class EvaluateLogitLensCountryEntitiesTests(unittest.TestCase):
    def test_full_vocabulary_rank_excludes_constituent_tokens(self) -> None:
        logits = torch.tensor(
            [
                [10.0, 8.0, 7.0, 6.0],
                [2.0, 10.0, 9.0, 0.0],
            ]
        )
        # Row 1 entity mean is 8; its own 10-logit token is excluded and the
        # remaining 8-logit tie does not outrank it.  Row 2 entity mean is 1,
        # so two non-constituent tokens outrank it.
        self.assertEqual(full_vocabulary_entity_target_ranks(logits, [0, 3]), [1, 3])

    def test_full_vocabulary_max_uses_strongest_constituent(self) -> None:
        logits = torch.tensor([[10.0, 9.0, 8.0, 0.0]])
        self.assertEqual(full_vocabulary_entity_target_ranks(logits, [0, 3]), [3])
        self.assertEqual(
            full_vocabulary_entity_target_ranks(logits, [0, 3], reduction="max"),
            [1],
        )

    def test_aggregate_entity_counts_bands_and_ranks(self) -> None:
        rows = [
            {
                "original_group": "shortcut_candidate",
                "logit_lens_country_entity": {
                    "best_rank": 1,
                    "evidence_band": "compositional",
                },
            },
            {
                "original_group": "shortcut_candidate",
                "logit_lens_country_entity": {
                    "best_rank": 5,
                    "evidence_band": "shortcut_candidate",
                },
            },
        ]
        result = aggregate_entity(rows, "shortcut_candidate")
        self.assertEqual(result["num_queries"], 2)
        self.assertEqual(result["country_entity_evidence_bands"]["compositional"], 1)
        self.assertEqual(result["country_entity_evidence_bands"]["shortcut_candidate"], 1)
        self.assertEqual(result["median_country_entity_rank"], 3.0)


if __name__ == "__main__":
    unittest.main()
