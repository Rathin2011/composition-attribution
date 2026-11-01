"""Tests for conservative alias-result postprocessing."""

from __future__ import annotations

import unittest

from jlens_alias_reclassification.postprocess_alias_results import (
    aliases_by_status,
    build_alias_audit,
    build_query_results,
    filtered_measurement,
)


class FakeSpec:
    values = {
        "A": [1],
        "B": [2],
        "Good": [3],
        "CAR": [4],
        "US": [5],
        "Long Name": [6, 7],
        "Collide": [2],
        "SharedA": [8],
        "SharedB": [8],
    }

    def token_ids(self, tokenizer, node, value):
        return self.values[value]


class FakeTokenizer:
    def decode(self, ids):
        return f" token-{ids[0]}"


def alias_record(saved_rank=5, rerun_rank=5):
    return {
        "prompt_instance_id": "p0",
        "query_index": 0,
        "task": "landmark-country-capital",
        "query": {"x": "X", "Fx": "A", "GFx": "Y"},
        "original_classification": {
            "group": "shortcut_candidate",
            "best_vocabulary_rank": saved_rank,
        },
        "alias_reclassification": {
            "canonical_rerun_validation": {
                "saved_rank": saved_rank,
                "rerun_rank": rerun_rank,
                "rank_difference": rerun_rank - saved_rank,
                "exact_rank_match": rerun_rank == saved_rank,
                "saved_group": "shortcut_candidate",
                "rerun_group": "shortcut_candidate" if rerun_rank >= 5 else "ambiguous",
                "group_match": rerun_rank >= 5,
            },
            "surface_token_groups": [
                {
                    "best_vocabulary_rank": rerun_rank,
                    "surface_forms": [{"surface": "A", "kind": "canonical", "token_ids": [1]}],
                },
                {
                    "best_vocabulary_rank": 2,
                    "surface_forms": [{"surface": "Good", "kind": "alias", "token_ids": [3]}],
                },
                {
                    "best_vocabulary_rank": 1,
                    "surface_forms": [{"surface": "US", "kind": "alias", "token_ids": [5]}],
                },
            ],
        },
    }


class PostprocessAliasResultsTest(unittest.TestCase):
    def setUp(self):
        import jlens_alias_reclassification.postprocess_alias_results as module

        self.original_get_task_spec = module.get_task_spec
        module.get_task_spec = lambda task: FakeSpec()
        self.module = module

    def tearDown(self):
        self.module.get_task_spec = self.original_get_task_spec

    def test_mechanical_audit(self):
        aliases = {
            "A": ["Good", "CAR", "US", "Long Name", "Collide", "SharedA"],
            "B": ["SharedB"],
        }
        policy = {
            "version": 1,
            "explicit_reject": {"CAR": "common word"},
            "sensitivity_only": {"US": "pronoun"},
        }
        audit = build_alias_audit(
            aliases,
            ["A", "B"],
            FakeTokenizer(),
            policy,
            task="landmark-country-capital",
        )
        status = {row["alias"]: row["status"] for row in audit}
        self.assertEqual(status["Good"], "accepted")
        self.assertEqual(status["US"], "sensitivity_only")
        for rejected in ("CAR", "Long Name", "Collide", "SharedA", "SharedB"):
            self.assertEqual(status[rejected], "rejected")
        self.assertEqual(aliases_by_status(audit, "accepted"), {"A": ["Good"]})

    def test_primary_and_sensitivity_are_separate_from_drift(self):
        result = filtered_measurement(
            alias_record(), ["Good"], ["US"], policy_version=1
        )
        self.assertEqual(result["primary"]["best_vocabulary_rank"], 2)
        self.assertEqual(result["primary"]["group"], "compositional")
        self.assertEqual(result["sensitivity"]["best_vocabulary_rank"], 1)
        self.assertEqual(
            result["canonical_drift"]["transition"],
            "shortcut_candidate->shortcut_candidate",
        )

    def test_no_alias_cannot_change_canonical_rerun(self):
        result = filtered_measurement(alias_record(), [], [], policy_version=1)
        self.assertTrue(result["no_accepted_primary_alias"])
        self.assertEqual(result["primary"]["group"], "shortcut_candidate")
        self.assertFalse(result["primary"]["rank_improved"])

    def test_query_results_use_all_original_contexts(self):
        filtered = alias_record()
        filtered["filtered_alias_reclassification"] = filtered_measurement(
            filtered, ["Good"], [], policy_version=1
        )
        original = []
        for identifier, group in (("p0", "shortcut_candidate"), ("p1", "compositional")):
            original.append(
                {
                    "prompt_instance_id": identifier,
                    "query_index": 0,
                    "task": "landmark-country-capital",
                    "query": {"x": "X", "Fx": "A", "GFx": "Y"},
                    "j_lens": {"classification": {"group": group}},
                }
            )
        rows = build_query_results(original, [filtered], task="landmark-country-capital")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["original_shortcut_rate"], 0.5)
        self.assertEqual(rows[0]["final_shortcut_rate"], 0.0)
        self.assertFalse(rows[0]["original_majority_shortcut"])


if __name__ == "__main__":
    unittest.main()
