import json
import tempfile
import unittest
from pathlib import Path

from merge_logit_lens_shards import (
    load_and_validate_shard_summaries,
    merge_records,
    recomputed_counts_match_shard_summaries,
)


def source_record(prompt_id: str) -> dict:
    return {
        "prompt_instance_id": prompt_id,
        "prompt": f"Q: {prompt_id}\nA:",
        "evaluation": {"exact_match": True},
    }


def eligible_result(prompt_id: str, group: str) -> dict:
    row = source_record(prompt_id)
    row["logit_lens"] = {
        "paper_token_eligible": True,
        "paper_token_filter_reason": None,
        "classification": {"group": group},
        "node_evidence": {"x": {}, "Fx": {}, "GFx": {}},
    }
    return row


def excluded_result(prompt_id: str) -> dict:
    row = source_record(prompt_id)
    row["logit_lens"] = {
        "paper_token_eligible": False,
        "paper_token_filter_reason": "node_first_tokens_overlap",
        "classification": None,
        "node_evidence": None,
    }
    return row


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row) + "\n" for row in rows))


def shard_summary(
    shard: Path,
    *,
    start: int,
    requested: int,
    rows: int,
    eligible: int,
    excluded: int,
    compositional: int = 0,
    ambiguous: int = 0,
    shortcut: int = 0,
) -> dict:
    return {
        "model": "model",
        "stage_one_revision": "stage-one",
        "model_commit": "model-commit",
        "dtype": "bfloat16",
        "reference_code_commit": "reference-commit",
        "input": "/input.jsonl",
        "output": str(shard),
        "start_index": start,
        "requested_num_records": requested,
        "chunk_size": 32,
        "nodes": ["x", "Fx", "GFx"],
        "intermediate_node": "Fx",
        "rank_scope": "complete_vocabulary",
        "target_definition": "leading_space_first_token",
        "query_positions": "tokens_covering_x_plus_newline_A_colon",
        "layers": "all_32_post_decoder_block_outputs",
        "processing_signature": "maximum_RR_over_query_positions_per_layer",
        "overall_evidence": "maximum_RR_over_query_positions_and_layers",
        "composition_rr_threshold": 0.5,
        "shortcut_rr_threshold": 0.2,
        "num_input_records": rows,
        "num_paper_token_eligible": eligible,
        "num_paper_token_excluded": excluded,
        "paper_token_exclusion_reasons": (
            {"node_first_tokens_overlap": excluded} if excluded else {}
        ),
        "classification_counts": {
            "compositional": compositional,
            "ambiguous": ambiguous,
            "shortcut_candidate": shortcut,
        },
    }


class MergeLogitLensShardsTest(unittest.TestCase):
    def make_fixture(self, directory: str):
        root = Path(directory)
        source = root / "source.jsonl"
        shard_1 = root / "shard_01.jsonl"
        shard_2 = root / "shard_02.jsonl"
        output = root / "merged.jsonl"

        write_jsonl(source, [source_record("p0"), source_record("p1"), source_record("p2")])
        write_jsonl(
            shard_1,
            [eligible_result("p0", "compositional"), excluded_result("p1")],
        )
        write_jsonl(shard_2, [eligible_result("p2", "shortcut_candidate")])
        summaries = [
            shard_summary(
                shard_1,
                start=0,
                requested=2,
                rows=2,
                eligible=1,
                excluded=1,
                compositional=1,
            ),
            shard_summary(
                shard_2,
                start=2,
                requested=2,
                rows=1,
                eligible=1,
                excluded=0,
                shortcut=1,
            ),
        ]
        for shard, summary in zip((shard_1, shard_2), summaries, strict=True):
            shard.with_name(f"{shard.stem}_summary.json").write_text(
                json.dumps(summary)
            )
        return source, [shard_1, shard_2], output, summaries

    def test_validates_summaries_merges_in_order_and_recomputes_counts(self):
        with tempfile.TemporaryDirectory() as directory:
            source, shards, output, expected_summaries = self.make_fixture(directory)
            _, summaries = load_and_validate_shard_summaries(shards)
            self.assertEqual(summaries, expected_summaries)

            counts = merge_records(
                source, shards, output, expected_records=3
            )
            recomputed_counts_match_shard_summaries(counts, summaries)
            merged = [json.loads(line) for line in output.read_text().splitlines()]

        self.assertEqual(
            [row["prompt_instance_id"] for row in merged], ["p0", "p1", "p2"]
        )
        self.assertEqual(counts["num_input_records"], 3)
        self.assertEqual(counts["num_paper_token_eligible"], 2)
        self.assertEqual(counts["num_paper_token_excluded"], 1)
        self.assertEqual(counts["classification_counts"]["compositional"], 1)
        self.assertEqual(counts["classification_counts"]["shortcut_candidate"], 1)

    def test_rejects_result_order_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            source, shards, output, _ = self.make_fixture(directory)
            rows = [json.loads(line) for line in shards[0].read_text().splitlines()]
            write_jsonl(shards[0], list(reversed(rows)))
            with self.assertRaisesRegex(ValueError, "order does not match"):
                merge_records(source, shards, output, expected_records=3)

    def test_rejects_noncontiguous_or_methodologically_mixed_summaries(self):
        with tempfile.TemporaryDirectory() as directory:
            _, shards, _, _ = self.make_fixture(directory)
            second_summary = shards[1].with_name(f"{shards[1].stem}_summary.json")
            value = json.loads(second_summary.read_text())
            value["start_index"] = 3
            second_summary.write_text(json.dumps(value))
            with self.assertRaisesRegex(ValueError, "noncontiguous shard start"):
                load_and_validate_shard_summaries(shards)

            value["start_index"] = 2
            value["model_commit"] = "different"
            second_summary.write_text(json.dumps(value))
            with self.assertRaisesRegex(ValueError, "model_commit"):
                load_and_validate_shard_summaries(shards)


if __name__ == "__main__":
    unittest.main()
