import json
import tempfile
import unittest
from pathlib import Path

import torch

from evaluate_logit_lens import (
    RunningSummary,
    classify_reciprocal_rank,
    excluded_result,
    first_query_token_index,
    intermediate_classification,
    node_token_info,
    paper_token_filter_reason,
    read_correct_records,
    summarize_node_evidence,
)


class MappingTokenizer:
    """Tiny tokenizer exposing only the interface used by token metadata."""

    def __init__(self) -> None:
        self.encodings = {
            " Landmark": [10, 11],
            " Country": [20],
            " Capital": [30],
        }
        self.pieces = {
            10: " Land",
            11: "mark",
            20: " Country",
            30: " Capital",
        }

    def encode(self, text, *, add_special_tokens):
        if add_special_tokens:
            raise AssertionError("tests expect add_special_tokens=False")
        return self.encodings[text]

    def decode(self, token_ids):
        if isinstance(token_ids, int):
            token_ids = [token_ids]
        return "".join(self.pieces[token_id] for token_id in token_ids)


class CharacterTokenizer:
    """One-character-per-token tokenizer for query-boundary tests."""

    def __init__(self) -> None:
        self.characters = {}

    def encode(self, text, *, add_special_tokens):
        if add_special_tokens:
            raise AssertionError("tests expect add_special_tokens=False")
        token_ids = list(range(100, 100 + len(text)))
        self.characters = dict(zip(token_ids, text, strict=True))
        return token_ids

    def decode(self, token_id):
        if isinstance(token_id, (list, tuple)):
            return "".join(self.characters[item] for item in token_id)
        return self.characters[token_id]


def correct_record(prompt_id="p0"):
    return {
        "prompt_instance_id": prompt_id,
        "prompt": "Q: Demo\nA: Answer\n\nQ: Landmark\nA:",
        "query": {"x": "Landmark", "Fx": "Country", "GFx": "Capital"},
        "evaluation": {"exact_match": True},
    }


def token_info_fixture():
    return {
        "x": {
            "value": "Landmark",
            "token_ids": [10, 11],
            "tokens": [" Land", "mark"],
            "num_tokens": 2,
            "first_token_id": 10,
            "first_token": " Land",
        },
        "Fx": {
            "value": "Country",
            "token_ids": [20],
            "tokens": [" Country"],
            "num_tokens": 1,
            "first_token_id": 20,
            "first_token": " Country",
        },
        "GFx": {
            "value": "Capital",
            "token_ids": [30],
            "tokens": [" Capital"],
            "num_tokens": 1,
            "first_token_id": 30,
            "first_token": " Capital",
        },
    }


class EvaluateLogitLensTest(unittest.TestCase):
    def test_reads_only_exact_correct_records_and_supports_slicing(self):
        rows = [correct_record(f"p{index}") for index in range(3)]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "correct.jsonl"
            path.write_text("".join(json.dumps(row) + "\n" for row in rows))
            selected = list(read_correct_records(path, start_index=1, num_records=1))
        self.assertEqual([row["prompt_instance_id"] for row in selected], ["p1"])

        rows[0]["evaluation"]["exact_match"] = False
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "incorrect.jsonl"
            path.write_text(json.dumps(rows[0]) + "\n")
            with self.assertRaisesRegex(ValueError, "not exact-correct"):
                list(read_correct_records(path))

    def test_node_token_info_uses_leading_space_and_keeps_all_tokens(self):
        info = node_token_info(
            MappingTokenizer(),
            {"x": "Landmark", "Fx": "Country", "GFx": "Capital"},
        )
        self.assertEqual(info["x"]["token_ids"], [10, 11])
        self.assertEqual(info["x"]["first_token_id"], 10)
        self.assertEqual(info["x"]["tokens"], [" Land", "mark"])
        self.assertEqual(info["Fx"]["first_token"], " Country")

    def test_paper_token_filter_reproduces_both_exclusions(self):
        eligible = token_info_fixture()
        self.assertIsNone(paper_token_filter_reason(eligible))

        repeated_first = token_info_fixture()
        repeated_first["Fx"] = dict(repeated_first["Fx"], first_token_id=10)
        self.assertEqual(
            paper_token_filter_reason(repeated_first),
            "node_first_tokens_overlap",
        )

        target_inside_x = token_info_fixture()
        target_inside_x["x"] = dict(target_inside_x["x"], token_ids=[10, 20])
        self.assertEqual(
            paper_token_filter_reason(target_inside_x),
            "target_first_token_occurs_inside_x",
        )

    def test_query_boundary_keeps_x_newline_and_answer_prefix(self):
        tokenizer = CharacterTokenizer()
        prompt = "Q: Demo\nA: Answer\n\nQ: KV3\nA:"
        start = first_query_token_index(tokenizer, prompt, "KV3")
        self.assertEqual(start, len(prompt) - len("KV3\nA:"))
        with self.assertRaisesRegex(ValueError, "does not end"):
            first_query_token_index(tokenizer, prompt, "Wrong")

    def test_classification_threshold_boundaries(self):
        self.assertEqual(classify_reciprocal_rank(1.0), "compositional")
        self.assertEqual(classify_reciprocal_rank(0.5), "compositional")
        self.assertEqual(classify_reciprocal_rank(0.25), "ambiguous")
        self.assertEqual(classify_reciprocal_rank(0.2), "shortcut_candidate")
        self.assertEqual(classify_reciprocal_rank(0.01), "shortcut_candidate")

    def test_summary_preserves_all_values_and_uses_max_rr_over_positions(self):
        # P=2 retained query positions, L=3 layers, K=3 task nodes.
        logits = torch.arange(18, dtype=torch.float32).reshape(2, 3, 3)
        ranks = torch.tensor(
            [
                [[2, 10, 1], [2, 5, 1], [2, 4, 1]],
                [[2, 8, 1], [2, 2, 1], [2, 3, 1]],
            ]
        )
        evidence = summarize_node_evidence(
            logits,
            ranks,
            token_info_fixture(),
            prompt_position_offset=100,
        )

        fx = evidence["Fx"]
        self.assertEqual(
            fx["positionwise_layerwise_logits"], logits[:, :, 1].tolist()
        )
        self.assertEqual(fx["positionwise_layerwise_ranks"], ranks[:, :, 1].tolist())
        for actual, expected in zip(
            fx["layerwise_max_reciprocal_rank"],
            [0.125, 0.5, 1 / 3],
            strict=True,
        ):
            self.assertAlmostEqual(actual, expected, places=6)
        self.assertEqual(fx["peak_reciprocal_rank"], 0.5)
        self.assertEqual(fx["best_vocabulary_rank"], 2)
        self.assertEqual(fx["peak_layers"], [1])
        self.assertEqual(
            fx["peak_locations"],
            [{"query_position": 1, "prompt_position": 101, "layer": 1}],
        )
        classification = intermediate_classification(evidence)
        self.assertEqual(classification["group"], "compositional")
        self.assertEqual(classification["intermediate_value"], "Country")

    def test_running_summary_partitions_eligible_and_excluded_rows(self):
        evidence = {
            "Fx": {
                "value": "Country",
                "peak_reciprocal_rank": 0.5,
                "best_vocabulary_rank": 2,
                "peak_layers": [1],
                "first_peak_layer": 1,
            }
        }
        eligible = correct_record("eligible")
        eligible["logit_lens"] = {
            "paper_token_eligible": True,
            "classification": intermediate_classification(evidence),
        }
        excluded = excluded_result(
            correct_record("excluded"),
            token_info_fixture(),
            "node_first_tokens_overlap",
        )

        summary = RunningSummary()
        summary.add(eligible)
        summary.add(excluded)
        result = summary.as_dict()
        self.assertEqual(result["num_input_records"], 2)
        self.assertEqual(result["num_paper_token_eligible"], 1)
        self.assertEqual(result["num_paper_token_excluded"], 1)
        self.assertEqual(result["classification_counts"]["compositional"], 1)
        self.assertEqual(
            result["paper_token_exclusion_reasons"]["node_first_tokens_overlap"],
            1,
        )


if __name__ == "__main__":
    unittest.main()
