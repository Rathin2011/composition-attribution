"""Validation tests for the distributed J-Lens merge wrapper."""

from __future__ import annotations

from pathlib import Path
import unittest

from jlens_experiments.compatibility import JLENS_COMMIT, MODEL_COMMIT, MODEL_ID
from jlens_experiments.merge_lenses import (
    EXPECTED_HIDDEN_SIZE,
    EXPECTED_LAYERS,
    EXPECTED_PROMPTS_PER_SHARD,
    EXPECTED_SHARDS,
    EXPECTED_TARGET_LAYER,
    validate_shard_summary,
)


class MergeLensTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = Path("/fixed/prompts.jsonl")
        self.records = [
            {"sample_index": index} for index in range(EXPECTED_PROMPTS_PER_SHARD)
        ]
        self.summary = {
            "status": "complete",
            "model": MODEL_ID,
            "model_commit": MODEL_COMMIT,
            "jlens_commit": JLENS_COMMIT,
            "input": {
                "mode": "fixed_manifest",
                "prompt_manifest": str(self.manifest),
                "manifest_prompts": EXPECTED_SHARDS * EXPECTED_PROMPTS_PER_SHARD,
                "num_shards": EXPECTED_SHARDS,
                "shard_index": 0,
                "selected_sample_indices": list(range(EXPECTED_PROMPTS_PER_SHARD)),
            },
            "fit": {
                "requested_prompts": EXPECTED_PROMPTS_PER_SHARD,
                "successful_prompts": EXPECTED_PROMPTS_PER_SHARD,
                "source_layers": EXPECTED_LAYERS,
                "target_layer": EXPECTED_TARGET_LAYER,
                "hidden_size": EXPECTED_HIDDEN_SIZE,
                "max_seq_len": 128,
                "dim_batch": 8,
            },
        }

    def test_accepts_consistent_shard(self) -> None:
        validate_shard_summary(
            self.summary,
            shard_index=0,
            expected_records=self.records,
            manifest_path=self.manifest,
        )

    def test_rejects_wrong_membership_or_settings(self) -> None:
        self.summary["input"]["selected_sample_indices"][0] = 999
        self.summary["fit"]["source_layers"] = [12]
        with self.assertRaisesRegex(ValueError, "sample_indices.*source_layers"):
            validate_shard_summary(
                self.summary,
                shard_index=0,
                expected_records=self.records,
                manifest_path=self.manifest,
            )


if __name__ == "__main__":
    unittest.main()
