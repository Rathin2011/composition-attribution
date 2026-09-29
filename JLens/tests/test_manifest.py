"""CPU-only tests for fitting-manifest creation, validation, and sharding."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

from jlens_experiments.manifest import (
    persist_prompt_records,
    prepare_prompt_records,
    read_prompt_records,
    select_prompt_indices,
    select_prompt_shard,
)


class FakeTokenizer:
    def decode(self, token_ids, **kwargs):
        self.kwargs = kwargs
        return " ".join(f"T{token_id}" for token_id in token_ids)


class ManifestTests(unittest.TestCase):
    def test_selection_is_deterministic_unique_and_seeded(self) -> None:
        first = select_prompt_indices(num_windows=100, num_prompts=10, seed=7)
        second = select_prompt_indices(num_windows=100, num_prompts=10, seed=7)
        different = select_prompt_indices(num_windows=100, num_prompts=10, seed=8)
        self.assertEqual(first, second)
        self.assertNotEqual(first, different)
        self.assertEqual(len(first), len(set(first)))

    def test_prompt_records_preserve_tokens_and_provenance(self) -> None:
        windows = np.arange(6 * 8, dtype=np.uint32).reshape(6, 8)
        metadata = {
            index: {
                "sample_index": index,
                "global_window_id": 100 + index,
                "global_sequence_index": 200 + index,
                "manifest_index": 300 + index,
                "source": f"source-{index}",
                "relative_path": f"shard-{index}.npy",
            }
            for index in range(6)
        }
        tokenizer = FakeTokenizer()
        records = prepare_prompt_records(
            windows,
            metadata,
            tokenizer,
            num_prompts=3,
            prompt_tokens=4,
            seed=0,
        )
        self.assertEqual(len(records), 3)
        for record in records:
            row = record["sample_index"]
            self.assertEqual(record["token_ids"], windows[row, :4].tolist())
            self.assertEqual(record["global_window_id"], 100 + row)
            self.assertEqual(record["source_token_count"], 4)
            self.assertTrue(record["text"].startswith("T"))
        self.assertFalse(tokenizer.kwargs["skip_special_tokens"])

    def test_metadata_must_match_every_window(self) -> None:
        windows = np.zeros((2, 4), dtype=np.uint32)
        with self.assertRaisesRegex(ValueError, "metadata indices"):
            prepare_prompt_records(
                windows,
                {0: {"sample_index": 0}},
                FakeTokenizer(),
                num_prompts=1,
                prompt_tokens=4,
                seed=0,
            )

    def test_existing_prompt_artifact_must_match_for_resume(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "prompts.jsonl"
            records = [{"sample_index": 1, "text": "example"}]
            persist_prompt_records(path, records)
            persist_prompt_records(path, records)
            with self.assertRaisesRegex(ValueError, "differs"):
                persist_prompt_records(path, [{"sample_index": 2, "text": "other"}])

    def test_ten_shards_are_disjoint_and_cover_manifest(self) -> None:
        records = [
            {
                "selection_index": index,
                "sample_index": 1000 + index,
                "source_token_count": 1,
                "token_ids": [index],
                "text": f"prompt {index}",
            }
            for index in range(1000)
        ]
        shards = [
            select_prompt_shard(records, num_shards=10, shard_index=index)
            for index in range(10)
        ]
        self.assertTrue(all(len(shard) == 100 for shard in shards))
        indices = [record["selection_index"] for shard in shards for record in shard]
        self.assertEqual(indices, list(range(1000)))
        self.assertEqual(len(indices), len(set(indices)))

    def test_prompt_manifest_round_trip_and_validation(self) -> None:
        records = [
            {
                "selection_index": 100 + index,
                "sample_index": 10 + index,
                "source_token_count": 2,
                "token_ids": [index, index + 1],
                "text": f"prompt {index}",
            }
            for index in range(2)
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.jsonl"
            persist_prompt_records(path, records)
            self.assertEqual(read_prompt_records(path), records)
            records[1]["selection_index"] = 103
            path.write_text(
                "".join(json.dumps(record) + "\n" for record in records),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "selection_index"):
                read_prompt_records(path)


if __name__ == "__main__":
    unittest.main()
