"""Prevent the disallowed association provider from entering gradient runs."""
import gzip
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


path = Path(__file__).resolve().parents[1] / "stages/03_gradient.py"
spec = importlib.util.spec_from_file_location("gradient_runner_manual_test", path)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class ManualSourceTests(unittest.TestCase):
    def load(self, settings, **changes):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "associations.jsonl.gz"
            with gzip.open(path, "wt") as handle:
                handle.write(json.dumps({"task": "task", "target_mode": "true", "answer": "city",
                    "associations": [{"text": "word", "token_id": 123}], "settings": settings,
                    **changes}) + "\n")
            return runner.load_associations(path, "task", "true")

    def test_accepts_manual_source_without_inference(self):
        self.assertIn("city", self.load({"provider": "static_reviewed_catalog", "model_inference": False}))

    def test_rejects_prompted_source(self):
        with self.assertRaisesRegex(ValueError, "manually written"):
            self.load({"provider": "prompted_next_token", "model_inference": True})

    def test_rejects_missing_provenance_and_mixed_claims(self):
        for settings in ({}, {"provider": "static_reviewed_catalog", "model_inference": True},
                         {"provider": "prompted_next_token", "model_inference": False}):
            with self.subTest(settings=settings), self.assertRaisesRegex(ValueError, "manually written"):
                self.load(settings)

    def test_retains_reviewed_targets_without_associations(self):
        settings = {"provider": "static_reviewed_catalog", "model_inference": False}
        rows = self.load(settings, associations=[], association_status="no_reliable_associations",
                         association_unavailable_reason="Malformed source target; meaning unspecified.")
        self.assertEqual(rows["city"]["associations"], [])

    def test_empty_list_requires_review_decision_with_reason(self):
        settings = {"provider": "static_reviewed_catalog", "model_inference": False}
        for changes in ({"associations": []},
                        {"associations": [], "association_status": "no_reliable_associations"},
                        {"association_status": "no_reliable_associations",
                         "association_unavailable_reason": "reason"}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.load(settings, **changes)


if __name__ == "__main__":
    unittest.main()
