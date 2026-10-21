"""Focused tests for strict baseline-shard merging."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from evaluate_baseline import open_text, read_jsonl
from merge_baseline_shards import companion_summary, merge_baseline_shards


def manifest_row(index: int) -> dict:
    return {
        "prompt_instance_id": f"id-{index}",
        "task": "test-task",
        "query_index": index,
        "context_variant": 0,
        "query": {"x": f"x-{index}", "Fx": "middle", "GFx": "answer"},
        "context": [],
        "prompt": f"Q: x-{index}\nA:",
    }


def result_row(index: int, correct: bool) -> dict:
    output = manifest_row(index)
    output["evaluation"] = {
        "exact_match": correct,
        "final_next_token_readout": {
            "target_GFx_first_token": {
                "rank": 1 if correct else 3,
                "in_top_k": {"1": correct, "5": True, "10": True},
            }
        },
    }
    return output


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with open_text(path, "wt") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")


def write_shard(
    root: Path,
    number: int,
    start: int,
    rows: list[dict],
    *,
    compressed: bool = False,
) -> None:
    suffix = ".jsonl.gz" if compressed else ".jsonl"
    shard = root / f"baseline_shard_{number:03d}{suffix}"
    write_jsonl(shard, rows)
    summary = {
        "task": "test-task",
        "model": "model",
        "stage_one_revision": "revision",
        "model_commit": "commit",
        "dtype": "bfloat16",
        "input": str(root / "manifest.jsonl"),
        "output": str(shard),
        "start_index": start,
        "requested_num_records": len(rows),
        "batch_size": 4,
        "max_new_tokens": 20,
        "stop_sequence": "\n\n",
        "rank_scope": "full_vocabulary",
        "target_measurement": "first_token_with_leading_space",
        "candidate_catalog": {"x": [], "Fx": [], "GFx": []},
        "num_prompt_instances": len(rows),
        "GFx_first_token_top_k": {"1": {}, "5": {}, "10": {}},
    }
    (root / f"baseline_shard_{number:03d}_summary.json").write_text(
        json.dumps(summary), encoding="utf-8"
    )


class MergeBaselineShardsTest(unittest.TestCase):
    def test_merges_complete_shards_and_recomputes_summary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "manifest.jsonl"
            write_jsonl(manifest, [manifest_row(index) for index in range(3)])
            write_shard(
                root, 1, 0, [result_row(0, True), result_row(1, False)], compressed=True
            )
            write_shard(root, 2, 2, [result_row(2, True)], compressed=True)
            summary = merge_baseline_shards(
                task="test-task",
                manifest=manifest,
                shard_directory=root,
                output=root / "merged.jsonl.gz",
                summary_output=root / "merged_summary.json",
            )
            self.assertEqual(summary["num_prompt_instances"], 3)
            self.assertEqual(summary["num_unique_prompt_instance_ids"], 3)
            self.assertEqual(summary["num_exact_correct"], 2)
            self.assertAlmostEqual(summary["exact_accuracy"], 2 / 3)
            self.assertEqual(len(list(read_jsonl(root / "merged.jsonl.gz"))), 3)

    def test_companion_summary_supports_plain_and_gzip_shards(self) -> None:
        self.assertEqual(
            companion_summary(Path("baseline_shard_001.jsonl")),
            Path("baseline_shard_001_summary.json"),
        )
        self.assertEqual(
            companion_summary(Path("baseline_shard_001.jsonl.gz")),
            Path("baseline_shard_001_summary.json"),
        )

    def test_rejects_noncontiguous_shards(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "manifest.jsonl"
            write_jsonl(manifest, [manifest_row(index) for index in range(2)])
            write_shard(root, 1, 0, [result_row(0, True)])
            write_shard(root, 2, 2, [result_row(1, True)])
            with self.assertRaisesRegex(ValueError, "noncontiguous shard start"):
                merge_baseline_shards(
                    task="test-task",
                    manifest=manifest,
                    shard_directory=root,
                    output=root / "merged.jsonl",
                    summary_output=root / "merged_summary.json",
                )


if __name__ == "__main__":
    unittest.main()
