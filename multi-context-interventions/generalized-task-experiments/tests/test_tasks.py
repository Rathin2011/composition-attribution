"""Focused tests for the task interface."""

from __future__ import annotations

import unittest

from tasks import LANDMARK_COUNTRY_CAPITAL, TASKS, TaskExample, get_task_spec


class TaskInterfaceTest(unittest.TestCase):
    def test_selects_and_canonicalizes_only_requested_task(self) -> None:
        spec = LANDMARK_COUNTRY_CAPITAL
        # Use a copy without the production row-count assertion for this unit test.
        test_spec = type(spec)(
            dataset_task=spec.dataset_task,
            x_name=spec.x_name,
            fx_name=spec.fx_name,
            gfx_name=spec.gfx_name,
        )
        rows = [
            {
                "task": "landmark-country-capital",
                "x": "KV3",
                "Fx": "Egypt",
                "GFx": "Cairo",
            },
            {
                "task": "another-task",
                "x": "ignored",
                "Fx": "ignored",
                "GFx": "ignored",
            },
        ]

        self.assertEqual(
            test_spec.select_examples(rows),
            [TaskExample(x="KV3", Fx="Egypt", GFx="Cairo")],
        )

    def test_renders_the_shared_composition_prompt(self) -> None:
        prompt = LANDMARK_COUNTRY_CAPITAL.render_prompt(
            [TaskExample("Brandenburg Gate", "Germany", "Berlin")],
            TaskExample("KV3", "Egypt", "Cairo"),
        )

        self.assertEqual(
            prompt,
            "Q: Brandenburg Gate\nA: Berlin\n\nQ: KV3\nA:",
        )

    def test_overlap_is_defined_over_all_three_values(self) -> None:
        query = TaskExample("KV3", "Egypt", "Cairo")

        self.assertTrue(query.overlaps(TaskExample("Other", "Egypt", "Elsewhere")))
        self.assertFalse(query.overlaps(TaskExample("Other", "Italy", "Rome")))

    def test_intervention_target_supplies_a_distinct_pair(self) -> None:
        query = TaskExample("KV3", "Egypt", "Cairo")
        LANDMARK_COUNTRY_CAPITAL.validate_intervention_target(
            query, TaskExample("Colosseum", "Italy", "Rome")
        )

        with self.assertRaisesRegex(ValueError, "different Fx"):
            LANDMARK_COUNTRY_CAPITAL.validate_intervention_target(
                query, TaskExample("Other", "Egypt", "Alexandria")
            )

    def test_registry_reports_unknown_tasks(self) -> None:
        self.assertIs(get_task_spec("landmark-country-capital"), LANDMARK_COUNTRY_CAPITAL)
        self.assertEqual(len(TASKS), 18)
        with self.assertRaisesRegex(ValueError, "available tasks"):
            get_task_spec("unknown")


if __name__ == "__main__":
    unittest.main()
