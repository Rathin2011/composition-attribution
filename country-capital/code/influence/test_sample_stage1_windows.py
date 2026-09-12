from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import tempfile
import unittest

import sample_stage1_windows as sample
from stage1_data import (
    ANALYSIS_WINDOW_LENGTH,
    MANIFEST_SHA256,
    TOKEN_BYTES,
    TRAIN_SEQUENCE_LENGTH,
)


def make_inventory() -> dict[str, object]:
    return {
        "manifest_sha256": MANIFEST_SHA256,
        "token_bytes": TOKEN_BYTES,
        "train_sequence_length": TRAIN_SEQUENCE_LENGTH,
        "total_shards": 2,
        "total_complete_train_sequences": 3,
        "shards": [
            {
                "manifest_index": 0,
                "source": "first",
                "relative_path": "first.npy",
                "url": "https://example.test/first.npy",
                "complete_train_sequences": 1,
                "sequence_start": 0,
                "sequence_end": 1,
            },
            {
                "manifest_index": 1,
                "source": "second",
                "relative_path": "second.npy",
                "url": "https://example.test/second.npy",
                "complete_train_sequences": 2,
                "sequence_start": 1,
                "sequence_end": 3,
            },
        ],
    }


class SampleStageOneWindowsTest(unittest.TestCase):
    def test_load_and_validate_inventory_accepts_contiguous_offsets(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "inventory.json"
            path.write_text(json.dumps(make_inventory()), encoding="utf-8")
            loaded = sample.load_and_validate_inventory(path)
        self.assertEqual(loaded["total_complete_train_sequences"], 3)

    def test_load_and_validate_inventory_rejects_offset_gap(self) -> None:
        payload = make_inventory()
        payload["shards"][1]["sequence_start"] = 2
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "inventory.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "non-contiguous"):
                sample.load_and_validate_inventory(path)

    def test_selection_is_reproducible_unique_and_disjoint(self) -> None:
        first_hessian, first_ranking = sample.select_disjoint_window_ids(
            1_000, 10, 100, seed=0
        )
        second_hessian, second_ranking = sample.select_disjoint_window_ids(
            1_000, 10, 100, seed=0
        )

        self.assertEqual(first_hessian, second_hessian)
        self.assertEqual(first_ranking, second_ranking)
        self.assertEqual(len(set(first_hessian)), 10)
        self.assertEqual(len(set(first_ranking)), 100)
        self.assertFalse(set(first_hessian) & set(first_ranking))

    def test_map_window_ids_finds_shards_and_byte_ranges(self) -> None:
        inventory = make_inventory()
        records = sample.map_window_ids(
            [15, 16, 47], inventory["shards"], cohort="test"
        )

        self.assertEqual(records[0]["manifest_index"], 0)
        self.assertEqual(records[0]["window_slot"], 15)
        self.assertEqual(records[1]["manifest_index"], 1)
        self.assertEqual(records[1]["local_sequence_index"], 0)
        self.assertEqual(records[2]["local_sequence_index"], 1)
        for record in records:
            self.assertEqual(
                record["token_end"] - record["token_start"],
                ANALYSIS_WINDOW_LENGTH,
            )
            self.assertEqual(
                record["byte_end"] - record["byte_start"],
                ANALYSIS_WINDOW_LENGTH * TOKEN_BYTES,
            )

    def test_sample_windows_writes_requested_cohorts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            inventory_path = directory / "inventory.json"
            inventory_path.write_text(json.dumps(make_inventory()), encoding="utf-8")
            summary = sample.sample_windows(
                inventory_path,
                hessian_count=2,
                ranking_count=3,
                seed=0,
                hessian_output=directory / "hessian.jsonl",
                ranking_output=directory / "ranking.jsonl",
                summary_output=directory / "summary.json",
            )

            hessian = (directory / "hessian.jsonl").read_text().splitlines()
            ranking = (directory / "ranking.jsonl").read_text().splitlines()
            self.assertEqual(len(hessian), 2)
            self.assertEqual(len(ranking), 3)
            self.assertEqual(summary["hessian_count"], 2)
            self.assertEqual(summary["ranking_count"], 3)
            self.assertEqual(summary["hessian_unique_count"], 2)
            self.assertEqual(summary["ranking_unique_count"], 3)
            self.assertEqual(summary["overlap_count"], 0)
            self.assertTrue(summary["sets_are_disjoint"])

    def test_preview_prints_window_mapping(self) -> None:
        records = sample.map_window_ids(
            [16], make_inventory()["shards"], cohort="hessian"
        )
        output = StringIO()

        with redirect_stdout(output):
            sample.print_sample_preview("hessian", records, limit=1)

        printed = output.getvalue()
        self.assertIn("Hessian preview (1 windows)", printed)
        self.assertIn("window=16", printed)
        self.assertIn("shard=1", printed)
        self.assertIn("slot=0", printed)
        self.assertIn("tokens=[0,512)", printed)
        self.assertIn("bytes=[0,2048)", printed)


if __name__ == "__main__":
    unittest.main()
