"""Tests for exact-rank repair of completed lens outputs."""

from __future__ import annotations

import unittest

from repair_lens_classifications import exact_rank, repair_measurement


class RepairLensClassificationsTest(unittest.TestCase):
    def test_recovers_rank_five_from_float32_reciprocal(self) -> None:
        self.assertEqual(exact_rank(0.20000000298023224), 5)

    def test_repairs_rank_five_group_and_reciprocal(self) -> None:
        measurement = {
            "paper_token_eligible": True,
            "jlens_rr": [0.1666666716337204, 0.20000000298023224],
            "classification": {
                "group": "ambiguous",
                "best_vocabulary_rank": 5,
                "peak_reciprocal_rank": 0.20000000298023224,
            },
        }
        self.assertTrue(repair_measurement(measurement, "j_lens"))
        self.assertEqual(measurement["jlens_rr"], [1.0 / 6, 0.2])
        self.assertEqual(
            measurement["classification"]["group"], "shortcut_candidate"
        )
        self.assertEqual(
            measurement["classification"]["peak_reciprocal_rank"], 0.2
        )

    def test_excluded_measurement_is_unchanged(self) -> None:
        measurement = {"paper_token_eligible": False, "classification": None}
        self.assertFalse(repair_measurement(measurement, "logit_lens"))


if __name__ == "__main__":
    unittest.main()
