"""Focused tests for generalized multi-context prompt construction."""

from __future__ import annotations

import unittest

from build_prompt_manifest import build_prompt_manifest, select_query_indices
from tasks import TaskExample, TaskSpec


SPEC = TaskSpec("test-task", "input", "intermediate", "answer")


def example(index: int) -> TaskExample:
    return TaskExample(f"x-{index}", f"Fx-{index}", f"GFx-{index}")


class PromptManifestTest(unittest.TestCase):
    def setUp(self) -> None:
        self.examples = [example(index) for index in range(40)]

    def test_builds_reproducible_multi_context_prompts(self) -> None:
        first, first_summary = build_prompt_manifest(
            SPEC, self.examples, [3, 7], contexts_per_query=3, icl_examples=10
        )
        second, second_summary = build_prompt_manifest(
            SPEC, self.examples, [3, 7], contexts_per_query=3, icl_examples=10
        )
        self.assertEqual(first, second)
        self.assertEqual(first_summary, second_summary)
        self.assertEqual(len(first), 6)
        self.assertEqual(first_summary["num_prompt_instances"], 6)
        self.assertNotIn("icl_examples_per_context", first_summary)
        self.assertTrue(all("icl_examples" not in record for record in first))
        self.assertTrue(all("context_seed" not in record for record in first))

    def test_context_and_prompt_follow_shared_task_contract(self) -> None:
        records, _ = build_prompt_manifest(
            SPEC, self.examples, [3], contexts_per_query=2, icl_examples=10
        )
        for record in records:
            query = TaskExample(**record["query"])
            context = [TaskExample(**value) for value in record["context"]]
            self.assertEqual(len(context), 10)
            self.assertEqual(len(set(context)), 10)
            self.assertTrue(all(not value.overlaps(query) for value in context))
            self.assertEqual(record["prompt"], SPEC.render_prompt(context, query))
            self.assertTrue(record["prompt"].endswith("Q: x-3\nA:"))

    def test_each_variant_stream_advances_across_queries(self) -> None:
        records, _ = build_prompt_manifest(
            SPEC, self.examples, [38, 39], contexts_per_query=1, icl_examples=10
        )
        self.assertNotEqual(records[0]["context"], records[1]["context"])

    def test_selects_all_or_explicit_indices(self) -> None:
        self.assertEqual(
            select_query_indices(4, query_indices=[], all_queries=True),
            [0, 1, 2, 3],
        )
        self.assertEqual(
            select_query_indices(4, query_indices=[3, 1, 3], all_queries=False),
            [3, 1],
        )
        with self.assertRaisesRegex(ValueError, "use --all-queries"):
            select_query_indices(4, query_indices=[], all_queries=False)


if __name__ == "__main__":
    unittest.main()
