"""CPU tests for alias-aware J-Lens shortcut reclassification."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

import torch

from jlens_alias_reclassification.evaluate_aliases import (
    analyze_shortcut_record,
    load_aliases,
    read_shortcut_slice,
    surface_token_groups,
)


class FakeTokenizer:
    ids = {" Country": [1], " Britain": [2], " UK": [2]}

    def encode(self, text, add_special_tokens=False):
        return self.ids[text]

    def decode(self, ids):
        return {1: " Country", 2: " Britain"}[ids[0]]


class FakeLens:
    def apply(self, adapter, prompt, **kwargs):
        logits = {
            12: torch.tensor(
                [[9.0, 1.0, 8.0, 7.0, 6.0], [9.0, 2.0, 3.0, 8.0, 7.0]]
            ),
            16: torch.tensor(
                [[9.0, 2.0, 3.0, 8.0, 7.0], [9.0, 1.0, 8.0, 7.0, 6.0]]
            ),
        }
        return logits, torch.empty(0), torch.zeros(1, 8)


def shortcut_record(identifier="p0"):
    return {
        "prompt_instance_id": identifier,
        "query_index": 3,
        "context_variant": 2,
        "task": "landmark-country-capital",
        "prompt": "Q: Landmark\nA:",
        "query": {"x": "Landmark", "Fx": "Country", "GFx": "Capital"},
        "j_lens": {
            "query_token_start": 4,
            "num_query_positions": 2,
            "classification": {
                "group": "shortcut_candidate",
                "best_vocabulary_rank": 5,
                "peak_reciprocal_rank": 0.2,
            },
        },
    }


class AliasReclassificationTest(unittest.TestCase):
    def test_load_aliases_rejects_canonical_repetition(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "aliases.json"
            path.write_text(json.dumps({"aliases": {"A": ["a"]}}))
            with self.assertRaisesRegex(ValueError, "canonical value repeated"):
                load_aliases(path)

    def test_surface_forms_with_same_first_token_are_grouped(self):
        groups = surface_token_groups(
            FakeTokenizer(),
            task="landmark-country-capital",
            canonical="Country",
            aliases=["Britain", "UK"],
        )
        self.assertEqual(len(groups), 2)
        self.assertEqual(
            [value["surface"] for value in groups[1]["surface_forms"]],
            ["Britain", "UK"],
        )

    def test_alias_can_reclassify_shortcut_as_compositional(self):
        result = analyze_shortcut_record(
            FakeLens(),
            object(),
            FakeTokenizer(),
            shortcut_record(),
            ["Britain", "UK"],
            source_layers=(12, 16),
            max_seq_len=512,
            candidate_chunk_size=2,
        )
        alias = result["alias_reclassification"]
        self.assertEqual(alias["best_vocabulary_rank"], 2)
        self.assertEqual(alias["group"], "compositional")
        self.assertEqual(alias["transition"], "shortcut_candidate->compositional")
        self.assertEqual(alias["winning_surface_forms"], ["Britain", "UK"])
        self.assertTrue(alias["canonical_rerun_validation"]["exact_rank_match"])

    def test_small_canonical_rank_drift_is_recorded_not_rejected(self):
        record = shortcut_record()
        record["j_lens"]["classification"]["best_vocabulary_rank"] = 6
        result = analyze_shortcut_record(
            FakeLens(),
            object(),
            FakeTokenizer(),
            record,
            ["Britain"],
            source_layers=(12, 16),
            max_seq_len=512,
            candidate_chunk_size=2,
        )
        validation = result["alias_reclassification"]["canonical_rerun_validation"]
        self.assertEqual(validation["rank_difference"], -1)
        self.assertFalse(validation["exact_rank_match"])
        self.assertTrue(validation["group_match"])

    def test_shortcut_slice_is_indexed_only_over_shortcuts(self):
        records = [shortcut_record("s0"), shortcut_record("not"), shortcut_record("s1")]
        records[1]["j_lens"]["classification"]["group"] = "compositional"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "records.jsonl"
            path.write_text("".join(json.dumps(row) + "\n" for row in records))
            selected = list(
                read_shortcut_slice(
                    path,
                    task="landmark-country-capital",
                    start_index=1,
                    num_records=1,
                )
            )
        self.assertEqual([row["prompt_instance_id"] for row in selected], ["s1"])


if __name__ == "__main__":
    unittest.main()
