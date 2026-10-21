"""Tests for the requested generalized lens-results export."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from evaluate_baseline import open_text
from export_lens_results import lens_records, load_catalog, render_icl_context


class ExportLensResultsTest(unittest.TestCase):
    def test_loads_catalog_and_renders_context(self) -> None:
        summary = {
            "task": "test-task",
            "candidate_catalog": {
                "x": ["X1", "X2"],
                "Fx": [{"value": "F1"}, {"value": "F2"}],
                "GFx": [{"value": "G1"}, {"value": "G2"}],
            },
        }
        with TemporaryDirectory() as directory:
            path = Path(directory) / "summary.json"
            path.write_text(json.dumps(summary))
            catalog = load_catalog(path, task="test-task")
        self.assertEqual(catalog, (["X1", "X2"], ["F1", "F2"], ["G1", "G2"]))
        self.assertEqual(
            render_icl_context([{"x": "Demo1", "GFx": "A"}, {"x": "Demo2", "GFx": "B"}]),
            "Demo1->A;Demo2->B",
        )

    def test_exports_only_eligible_rows_with_requested_fields(self) -> None:
        base = {
            "task": "test-task",
            "prompt_instance_id": "p0",
            "query": {"x": "X", "Fx": "F1", "GFx": "G1"},
            "context": [{"x": "Demo", "Fx": "F2", "GFx": "G2"}],
            "logit_lens": {
                "paper_token_eligible": True,
                "llens_z": [[1.0, 2.0], [3.0, 4.0]],
                "llens_rr": [0.5, 1.0],
                "classification": {"group": "compositional"},
            },
            "j_lens": {
                "paper_token_eligible": True,
                "jlens_z": [[5.0], [6.0]],
                "jlens_rr": [0.25],
                "classification": {"group": "ambiguous"},
            },
        }
        excluded = json.loads(json.dumps(base))
        excluded["prompt_instance_id"] = "p1"
        excluded["logit_lens"]["paper_token_eligible"] = False
        excluded["j_lens"]["paper_token_eligible"] = False

        with TemporaryDirectory() as directory:
            path = Path(directory) / "input.jsonl.gz"
            with open_text(path, "wt") as handle:
                handle.write(json.dumps(base) + "\n")
                handle.write(json.dumps(excluded) + "\n")
            output = list(lens_records(path, task="test-task", expected_fx=2))

        self.assertEqual(len(output), 1)
        self.assertEqual(output[0]["icl_ctx"], "Demo->G2")
        self.assertEqual(output[0]["llens_classification"], "compositional")
        self.assertEqual(output[0]["jlens_classification"], "ambiguous")


if __name__ == "__main__":
    unittest.main()
