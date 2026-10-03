import json
import tempfile
import unittest
from pathlib import Path

import torch

from evaluate_baseline import (
    RunningSummary,
    batched,
    leading_space_token_ids,
    read_manifest,
    token_measurement,
    validate_top_ks,
)


class FakeTokenizer:
    def encode(self, text, *, add_special_tokens):
        self.last_encoded = text
        self.last_add_special_tokens = add_special_tokens
        return [11, 12]


class EvaluateBaselineTest(unittest.TestCase):
    def test_default_and_custom_top_ks(self):
        self.assertEqual(validate_top_ks([]), (1, 5, 10))
        self.assertEqual(validate_top_ks([10, 1, 5, 5]), (1, 5, 10))
        with self.assertRaises(ValueError):
            validate_top_ks([0])

    def test_reads_validated_manifest_slice(self):
        rows = [
            {
                "prompt_instance_id": f"p{index}",
                "prompt": "Q: landmark\nA:",
                "query": {"x": "landmark", "Fx": "country", "GFx": "capital"},
            }
            for index in range(4)
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.jsonl"
            path.write_text("".join(json.dumps(row) + "\n" for row in rows))
            selected = list(read_manifest(path, start_index=1, num_records=2))
        self.assertEqual([row["prompt_instance_id"] for row in selected], ["p1", "p2"])

    def test_rejects_manifest_with_missing_query_node(self):
        row = {
            "prompt_instance_id": "p0",
            "prompt": "Q: landmark\nA:",
            "query": {"x": "landmark", "GFx": "capital"},
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.jsonl"
            path.write_text(json.dumps(row) + "\n")
            with self.assertRaisesRegex(ValueError, "Fx"):
                list(read_manifest(path))

    def test_batches_stream_and_keeps_final_partial_batch(self):
        self.assertEqual(
            list(batched(iter([1, 2, 3, 4, 5]), 2)),
            [[1, 2], [3, 4], [5]],
        )

    def test_answer_tokenization_adds_leading_space(self):
        tokenizer = FakeTokenizer()
        self.assertEqual(leading_space_token_ids(tokenizer, "Egypt"), [11, 12])
        self.assertEqual(tokenizer.last_encoded, " Egypt")
        self.assertFalse(tokenizer.last_add_special_tokens)

    def test_token_measurement_uses_full_vocabulary_rank(self):
        logits = torch.tensor([0.0, 3.0, 1.0, 2.0])
        measurement = token_measurement(logits, token_id=3, top_ks=(1, 2, 5))
        self.assertEqual(measurement["rank"], 2)
        self.assertEqual(measurement["reciprocal_rank"], 0.5)
        self.assertEqual(
            measurement["in_top_k"], {"1": False, "2": True, "5": True}
        )
        expected = float(torch.log_softmax(logits, dim=-1)[3])
        self.assertAlmostEqual(measurement["log_probability"], expected, places=6)

    def test_running_summary_aggregates_exact_and_top_k(self):
        summary = RunningSummary((1, 5))
        summary.add(
            {
                "evaluation": {
                    "exact_match": True,
                    "final_next_token_readout": {
                        "GFx_first_token": {
                            "rank": 3,
                            "in_top_k": {"1": False, "5": True},
                        }
                    },
                }
            }
        )
        result = summary.as_dict()
        self.assertEqual(result["num_exact_correct"], 1)
        self.assertEqual(result["exact_accuracy"], 1.0)
        readout = result["final_next_token_readout"]
        self.assertEqual(readout["GFx_first_token_top_k"]["1"]["correct"], 0)
        self.assertEqual(readout["GFx_first_token_top_k"]["5"]["correct"], 1)
        self.assertEqual(readout["mean_GFx_first_token_rank"], 3.0)


if __name__ == "__main__":
    unittest.main()
