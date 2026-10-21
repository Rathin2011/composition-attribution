"""Focused tests for the generalized result-file contract."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from results import INTERVENTION_FIELDS, LENS_FIELDS, TOP_LEVEL_FIELDS, write_results


class ResultFileTest(unittest.TestCase):
    def test_writes_exact_requested_structure(self) -> None:
        lens = dict.fromkeys(LENS_FIELDS)
        lens.update(
            {
                "x": "KV3",
                "Fx": "Egypt",
                "GFx": "Cairo",
                "icl_ctx": "Brandenburg Gate->Berlin",
                "llens_z": [[1.0, 2.0], [3.0, 4.0]],
                "jlens_z": [[5.0], [6.0]],
                "llens_rr": [0.5, 1.0],
                "jlens_rr": [1.0],
                "llens_classification": "compositional",
                "jlens_classification": "shortcut_candidate",
            }
        )
        intervention = dict.fromkeys(INTERVENTION_FIELDS)
        intervention.update(
            {
                "x": "KV3",
                "Fx": "Egypt",
                "GFx": "Cairo",
                "icl_ctx": "Brandenburg Gate->Berlin",
                "intervention": "swap",
                "projection": "jlens",
                "target": "Germany",
                "z_max": "Berlin",
                "z_out_GFx": [7.0, 8.0],
                "z_out_Fx": [9.0, 10.0],
            }
        )

        with TemporaryDirectory() as directory:
            output = Path(directory) / "results.json"
            write_results(
                output,
                x=["KV3"],
                Fx=["Egypt", "Germany"],
                GFx=["Cairo", "Berlin"],
                results_lenses=[lens],
                results_intervention=[intervention],
            )
            saved = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(tuple(saved), TOP_LEVEL_FIELDS)
        self.assertEqual(tuple(saved["results_lenses"][0]), LENS_FIELDS)
        self.assertEqual(
            tuple(saved["results_intervention"][0]), INTERVENTION_FIELDS
        )

    def test_rejects_lens_matrix_missing_possible_fx_values(self) -> None:
        lens = dict.fromkeys(LENS_FIELDS)
        lens.update(
            {
                "x": "KV3",
                "Fx": "Egypt",
                "GFx": "Cairo",
                "icl_ctx": "A->B",
                "llens_z": [[1.0]],
                "jlens_z": [[2.0]],
                "llens_rr": [1.0],
                "jlens_rr": [1.0],
                "llens_classification": "compositional",
                "jlens_classification": "ambiguous",
            }
        )
        with TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "n_Fx=2"):
                write_results(
                    Path(directory) / "results.json",
                    x=["KV3"],
                    Fx=["Egypt", "Germany"],
                    GFx=["Cairo", "Berlin"],
                    results_lenses=[lens],
                    results_intervention=[],
                )

    def test_rejects_unknown_lens_classification(self) -> None:
        lens = dict.fromkeys(LENS_FIELDS)
        lens.update(
            {
                "x": "KV3",
                "Fx": "Egypt",
                "GFx": "Cairo",
                "icl_ctx": "A->B",
                "llens_z": [[1.0]],
                "jlens_z": [[2.0]],
                "llens_rr": [1.0],
                "jlens_rr": [1.0],
                "llens_classification": "unknown",
                "jlens_classification": "compositional",
            }
        )
        with TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "llens_classification"):
                write_results(
                    Path(directory) / "results.json",
                    x=["KV3"],
                    Fx=["Egypt"],
                    GFx=["Cairo"],
                    results_lenses=[lens],
                    results_intervention=[],
                )


if __name__ == "__main__":
    unittest.main()
