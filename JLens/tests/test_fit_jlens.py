"""CPU-only tests for fixed-manifest J-Lens fitting configuration."""

from __future__ import annotations

import unittest

from jlens_experiments.fit_jlens import validate_fit_settings


class FitJLensTests(unittest.TestCase):
    def test_fit_layers_are_sorted_unique_and_below_target(self) -> None:
        self.assertEqual(
            validate_fit_settings(
                source_layers=[24, 12, 18, 18], target_layer=31, dim_batch=8
            ),
            [12, 18, 24],
        )
        with self.assertRaisesRegex(ValueError, "below target"):
            validate_fit_settings(
                source_layers=[12, 31], target_layer=31, dim_batch=8
            )


if __name__ == "__main__":
    unittest.main()
