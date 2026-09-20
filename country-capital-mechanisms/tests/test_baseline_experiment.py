"""CPU tests for baseline record construction and summary aggregation."""

from __future__ import annotations

import importlib.util
import hashlib
import math
from pathlib import Path
import tempfile
import unittest


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "experiments"
    / "00_validate_baseline.py"
)
SPEC = importlib.util.spec_from_file_location("validate_baseline_experiment", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load baseline experiment")
baseline_experiment = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(baseline_experiment)


def query_fixture(index=0):
    return {
        "evaluation_index": index,
        "landmark": "KV3",
        "country": "Egypt",
        "capital": "Cairo",
        "answer_ids": [10, 11],
        "original_prediction": " Cairo",
    }


def result_fixture(*, prediction=" Cairo", logprob=-0.75):
    return {
        "prediction": prediction,
        "label": " Cairo",
        "full_answer_correct": prediction == " Cairo",
        "completion_logprob": logprob,
        "completion_token_logprobs": [-0.25, -0.5],
        "greedy_next_token_id": 10,
        "correct_first_token_top1": True,
        "generated_token_ids": [10, 11],
    }


class BaselineExperimentTests(unittest.TestCase):
    def test_record_contains_probabilities_derived_from_logprobabilities(self):
        record = baseline_experiment.make_record(query_fixture(), result_fixture())
        self.assertAlmostEqual(
            record["baseline"]["completion_probability"], math.exp(-0.75)
        )
        self.assertEqual(
            record["baseline"]["completion_token_probabilities"],
            [math.exp(-0.25), math.exp(-0.5)],
        )
        self.assertTrue(record["fresh_matches_saved_prediction"])
        self.assertEqual(record["answer_token_count"], 2)

    def test_summary_reports_incomplete_and_complete_runs(self):
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "input.jsonl"
            input_path.write_text("{}\n")
            input_sha256 = hashlib.sha256(input_path.read_bytes()).hexdigest()
            first = baseline_experiment.make_record(
                query_fixture(0), result_fixture()
            )
            second = baseline_experiment.make_record(
                query_fixture(1), result_fixture(prediction=" Wrong", logprob=-2.0)
            )

            incomplete = baseline_experiment.summarize(
                [first],
                expected_queries=2,
                input_path=input_path,
                input_sha256=input_sha256,
            )
            self.assertFalse(incomplete["complete"])
            self.assertEqual(incomplete["fresh_baseline_correct"], 1)

            complete = baseline_experiment.summarize(
                [first, second],
                expected_queries=2,
                input_path=input_path,
                input_sha256=input_sha256,
            )
            self.assertTrue(complete["complete"])
            self.assertEqual(complete["fresh_baseline_correct"], 1)
            self.assertEqual(complete["fresh_matches_saved_prediction"], 1)
            self.assertEqual(complete["multi_token_answers"], 2)


if __name__ == "__main__":
    unittest.main()
