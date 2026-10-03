import copy
import unittest

from filter_correct_baselines import filter_correct_records


def record(prompt_id: str, query_index: int, exact_match: bool) -> dict:
    return {
        "prompt_instance_id": prompt_id,
        "query_index": query_index,
        "context_variant": 0,
        "query": {"x": "landmark", "Fx": "country", "GFx": "capital"},
        "context": [{"x": "demo", "Fx": "demo-country", "GFx": "demo-capital"}],
        "prompt": "Q: demo\nA: demo-capital\n\nQ: landmark\nA:",
        "evaluation": {
            "prediction": " capital",
            "label": " capital",
            "exact_match": exact_match,
        },
    }


class FilterCorrectBaselinesTest(unittest.TestCase):
    def test_keeps_only_exact_correct_records_without_modification(self):
        rows = [record("p0", 0, True), record("p1", 0, False), record("p2", 1, True)]
        original = copy.deepcopy(rows)

        selected, summary = filter_correct_records(
            rows,
            expected_input_count=3,
            expected_correct_count=2,
        )

        self.assertEqual(selected, [original[0], original[2]])
        self.assertEqual(rows, original)
        self.assertEqual(summary["num_correct_prompt_instances"], 2)
        self.assertEqual(summary["num_queries_with_at_least_one_correct_context"], 2)
        self.assertEqual(summary["correct_context_count_histogram"], {"1": 2})

    def test_histogram_includes_queries_with_no_correct_context(self):
        rows = [record("p0", 0, False), record("p1", 1, True)]
        _, summary = filter_correct_records(rows)

        self.assertEqual(summary["correct_context_count_histogram"], {"0": 1, "1": 1})

    def test_rejects_duplicate_prompt_ids(self):
        with self.assertRaisesRegex(ValueError, "duplicate prompt_instance_id"):
            filter_correct_records([record("p0", 0, True), record("p0", 1, True)])

    def test_rejects_non_boolean_exact_match(self):
        row = record("p0", 0, True)
        row["evaluation"]["exact_match"] = 1
        with self.assertRaisesRegex(ValueError, "not Boolean"):
            filter_correct_records([row])

    def test_rejects_unexpected_counts(self):
        rows = [record("p0", 0, True)]
        with self.assertRaisesRegex(ValueError, "expected 2 input rows"):
            filter_correct_records(rows, expected_input_count=2)
        with self.assertRaisesRegex(ValueError, "expected 2 correct rows"):
            filter_correct_records(rows, expected_correct_count=2)


if __name__ == "__main__":
    unittest.main()
