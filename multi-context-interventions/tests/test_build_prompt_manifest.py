import unittest

from build_prompt_manifest import (
    Example,
    build_prompt_manifest,
    select_query_indices,
)


def example(index: int) -> Example:
    return Example(
        x=f"landmark-{index}",
        Fx=f"country-{index}",
        GFx=f"capital-{index}",
    )


class BuildPromptManifestTest(unittest.TestCase):
    def setUp(self):
        self.examples = [example(index) for index in range(40)]

    def test_builds_ten_reproducible_contexts_per_query(self):
        first, first_summary = build_prompt_manifest(
            self.examples,
            [3, 7],
            contexts_per_query=10,
            icl_examples=10,
            seed=0,
        )
        second, second_summary = build_prompt_manifest(
            self.examples,
            [3, 7],
            contexts_per_query=10,
            icl_examples=10,
            seed=0,
        )

        self.assertEqual(first, second)
        self.assertEqual(first_summary, second_summary)
        self.assertEqual(len(first), 20)
        self.assertEqual(first_summary["num_prompt_instances"], 20)
        self.assertEqual(
            [record["context_variant"] for record in first if record["query_index"] == 3],
            list(range(10)),
        )

    def test_contexts_are_valid_and_prompts_match_authors_format(self):
        records, _ = build_prompt_manifest(
            self.examples,
            [3],
            contexts_per_query=2,
            icl_examples=10,
            seed=0,
        )

        for record in records:
            query = Example(**record["query"])
            context = [Example(**item) for item in record["context"]]
            self.assertEqual(len(context), 10)
            self.assertEqual(len(set(context)), 10)
            self.assertTrue(all(not item.overlaps(query) for item in context))
            self.assertTrue(record["prompt"].endswith("Q: landmark-3\nA:"))
            self.assertEqual(record["prompt"].count("Q: "), 11)

    def test_selects_queries_by_landmark_and_index_without_duplicates(self):
        selected = select_query_indices(
            self.examples,
            landmarks=["landmark-3", "landmark-7"],
            query_indices=[3],
        )

        self.assertEqual(selected, [3, 7])

    def test_requires_a_query_selection(self):
        with self.assertRaisesRegex(ValueError, "select at least one query"):
            select_query_indices(self.examples, landmarks=[], query_indices=[])

    def test_selects_all_queries(self):
        selected = select_query_indices(
            self.examples,
            landmarks=[],
            query_indices=[],
            all_queries=True,
        )

        self.assertEqual(selected, list(range(len(self.examples))))

    def test_all_queries_rejects_individual_selection(self):
        with self.assertRaisesRegex(ValueError, "cannot be combined"):
            select_query_indices(
                self.examples,
                landmarks=["landmark-3"],
                query_indices=[],
                all_queries=True,
            )


if __name__ == "__main__":
    unittest.main()
