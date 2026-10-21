"""Focused tests for strict generalized Logit Lens shard merging."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from evaluate_baseline import open_text, read_jsonl
from merge_logit_lens_shards import (
    companion_summary,
    merge_logit_lens_shards,
)


FX_CATALOG = [
    {"value": "middle-a", "token_ids": [10]},
    {"value": "middle-b", "token_ids": [20]},
]


def source_row(index: int) -> dict:
    return {
        "prompt_instance_id": f"id-{index}",
        "task": "test-task",
        "query_index": index,
        "context_variant": 0,
        "query": {"x": f"x-{index}", "Fx": "middle-a", "GFx": "answer"},
        "context": [],
        "prompt": f"Q: x-{index}\nA:",
        "evaluation": {"exact_match": True},
    }


def result_row(index: int, group: str = "compositional") -> dict:
    output = source_row(index)
    rr = [0.5, 1.0] if group == "compositional" else [0.1, 0.2]
    output["logit_lens"] = {
        "paper_token_eligible": True,
        "paper_token_filter_reason": None,
        "query_token_start": 3,
        "num_query_positions": 2,
        "num_layers": 2,
        "selected_query_position_by_layer": [0, 1],
        "selected_prompt_position_by_layer": [3, 4],
        "llens_z": [[1.0, 2.0], [3.0, 4.0]],
        "llens_rr": rr,
        "classification": {
            "group": group,
            "peak_reciprocal_rank": max(rr),
        },
    }
    return output


def excluded_row(index: int) -> dict:
    output = source_row(index)
    output["logit_lens"] = {
        "paper_token_eligible": False,
        "paper_token_filter_reason": "node_first_tokens_overlap",
        "classification": None,
        "llens_z": None,
        "llens_rr": None,
    }
    return output


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with open_text(path, "wt") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")


def write_shard(root: Path, number: int, start: int, rows: list[dict]) -> None:
    shard = root / f"logit_lens_shard_{number:03d}.jsonl.gz"
    write_jsonl(shard, rows)
    groups = {"compositional": 0, "ambiguous": 0, "shortcut_candidate": 0}
    exclusions = {}
    eligible = 0
    for row in rows:
        lens = row["logit_lens"]
        if lens["paper_token_eligible"]:
            eligible += 1
            groups[lens["classification"]["group"]] += 1
        else:
            reason = lens["paper_token_filter_reason"]
            exclusions[reason] = exclusions.get(reason, 0) + 1
    summary = {
        "task": "test-task",
        "model": "model",
        "stage_one_revision": "revision",
        "model_commit": "commit",
        "dtype": "bfloat16",
        "input": str(root / "source.jsonl.gz"),
        "candidate_catalog_source": str(root / "baseline_summary.json"),
        "output": str(shard),
        "start_index": start,
        "requested_num_records": len(rows),
        "activation_chunk_size": 32,
        "candidate_chunk_size": 16,
        "Fx_catalog": FX_CATALOG,
        "rank_scope": "complete_vocabulary",
        "target_definition": "leading_space_first_token",
        "query_positions": "query",
        "layers": "all",
        "processing_signature": "maximum",
        "position_tie_break": "earliest",
        "composition_rr_threshold": 0.5,
        "shortcut_rr_threshold": 0.2,
        "num_input_records": len(rows),
        "num_paper_token_eligible": eligible,
        "num_paper_token_excluded": len(rows) - eligible,
        "paper_token_exclusion_reasons": exclusions,
        "classification_counts": groups,
    }
    companion_summary(shard).write_text(json.dumps(summary), encoding="utf-8")


class MergeLogitLensShardsTest(unittest.TestCase):
    def test_merges_and_recomputes_complete_results(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.jsonl.gz"
            write_jsonl(source, [source_row(index) for index in range(3)])
            write_shard(root, 1, 0, [result_row(0), result_row(1, "shortcut_candidate")])
            write_shard(root, 2, 2, [excluded_row(2)])
            output = root / "merged.jsonl.gz"
            summary = merge_logit_lens_shards(
                task="test-task",
                source=source,
                shard_directory=root,
                output=output,
                summary_output=root / "summary.json",
            )
            self.assertEqual(summary["num_input_records"], 3)
            self.assertEqual(summary["num_unique_prompt_instance_ids"], 3)
            self.assertEqual(summary["num_paper_token_eligible"], 2)
            self.assertEqual(summary["classification_counts"]["compositional"], 1)
            self.assertEqual(summary["classification_counts"]["shortcut_candidate"], 1)
            self.assertEqual(len(list(read_jsonl(output))), 3)

    def test_companion_summary_supports_compressed_shards(self) -> None:
        self.assertEqual(
            companion_summary(Path("logit_lens_shard_001.jsonl.gz")),
            Path("logit_lens_shard_001_summary.json"),
        )

    def test_rejects_noncontiguous_shards(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.jsonl.gz"
            write_jsonl(source, [source_row(index) for index in range(2)])
            write_shard(root, 1, 0, [result_row(0)])
            write_shard(root, 2, 2, [result_row(1)])
            with self.assertRaisesRegex(ValueError, "noncontiguous shard start"):
                merge_logit_lens_shards(
                    task="test-task",
                    source=source,
                    shard_directory=root,
                    output=root / "merged.jsonl.gz",
                    summary_output=root / "summary.json",
                )


if __name__ == "__main__":
    unittest.main()
