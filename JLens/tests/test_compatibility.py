"""CPU-only tests for the OLMo/J-lens compatibility wrapper."""

from __future__ import annotations

from types import SimpleNamespace
import unittest

import torch

from jlens_experiments.compatibility import compare_logits, validate_adapter


class CompatibilityTests(unittest.TestCase):
    def test_expected_adapter_layout_is_accepted(self) -> None:
        adapter = SimpleNamespace(
            n_layers=32,
            d_model=4096,
            layers=[object() for _ in range(32)],
            layout=SimpleNamespace(
                path="model",
                layers="layers",
                norm="norm",
                embed="embed_tokens",
                lm_head="lm_head",
            ),
            input_device=torch.device("cpu"),
        )
        report = validate_adapter(adapter)
        self.assertEqual(report["num_layers"], 32)
        self.assertEqual(report["hidden_size"], 4096)
        self.assertEqual(report["layout"]["path"], "model")

    def test_wrong_layer_count_is_rejected(self) -> None:
        adapter = SimpleNamespace(n_layers=31, d_model=4096, layers=[])
        with self.assertRaisesRegex(ValueError, "expected 32 layers"):
            validate_adapter(adapter)

    def test_identical_logit_paths_are_accepted(self) -> None:
        logits = torch.randn(1, 5, 20)
        report = compare_logits(logits, logits.clone())
        self.assertEqual(report["max_absolute_difference"], 0.0)
        self.assertTrue(report["same_final_top_token"])

    def test_incorrect_unembedding_path_is_rejected(self) -> None:
        hf_logits = torch.zeros(1, 2, 4)
        hf_logits[0, -1, 0] = 2.0
        adapter_logits = torch.zeros_like(hf_logits)
        adapter_logits[0, -1, 1] = 2.0
        with self.assertRaisesRegex(ValueError, "does not reproduce"):
            compare_logits(hf_logits, adapter_logits)


if __name__ == "__main__":
    unittest.main()
