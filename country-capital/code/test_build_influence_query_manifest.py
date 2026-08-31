"""Focused tests for the strict landmark influence-query manifest."""

from __future__ import annotations

import copy
import unittest

from build_influence_query_manifest import (
    COMPOSITION_GROUP,
    EXPECTED_PAIRS,
    EXPECTED_QUERIES,
    SHORTCUT_GROUP,
    build_manifest,
    read_frozen_pairs,
    read_jsonl,
    validate_manifest,
    DEFAULT_COMPOSITIONAL_INPUT,
    DEFAULT_MATCHED_REPORT,
    DEFAULT_SHORTCUT_INPUT,
)


def build_current_manifest() -> list[dict]:
    return build_manifest(
        read_jsonl(DEFAULT_COMPOSITIONAL_INPUT),
        read_jsonl(DEFAULT_SHORTCUT_INPUT),
        read_frozen_pairs(DEFAULT_MATCHED_REPORT),
    )


class ManifestTests(unittest.TestCase):
    def test_current_manifest_is_the_reviewed_strict_cohort(self) -> None:
        records = build_current_manifest()
        summary = validate_manifest(records)

        self.assertEqual(summary["queries"], EXPECTED_QUERIES)
        self.assertEqual(summary["matched_pairs"], EXPECTED_PAIRS)
        self.assertEqual(
            summary["group_counts"],
            {
                COMPOSITION_GROUP: EXPECTED_PAIRS,
                SHORTCUT_GROUP: EXPECTED_PAIRS,
            },
        )
        for pair_index in range(EXPECTED_PAIRS):
            composition, shortcut = records[2 * pair_index : 2 * pair_index + 2]
            self.assertEqual(composition["group"], COMPOSITION_GROUP)
            self.assertEqual(shortcut["group"], SHORTCUT_GROUP)
            self.assertEqual(
                (composition["country"], composition["capital"]),
                (shortcut["country"], shortcut["capital"]),
            )

    def test_manifest_rejects_a_broken_fact_match(self) -> None:
        records = build_current_manifest()
        broken = copy.deepcopy(records)
        broken[1]["capital"] = "Not the matched capital"

        with self.assertRaisesRegex(ValueError, "not fact matched"):
            validate_manifest(broken)


if __name__ == "__main__":
    unittest.main()
