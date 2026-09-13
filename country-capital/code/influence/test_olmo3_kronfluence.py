"""Focused tests for the OLMo 3 Kronfluence integration."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest

import numpy as np
import torch
import torch.nn.functional as F
from torch import nn

from kronfluence_block_diagonal import block_diagonal_eigh
from olmo3_kronfluence import (
    EXPECTED_KRONFLUENCE_VERSION,
    NUM_LAYERS,
    Olmo3LanguageModelingTask,
    TokenWindowDataset,
    encode_conditional_query,
    factor_arguments,
    restore_torch_dtype,
    score_arguments,
    verify_kronfluence_version,
)


class CharacterTokenizer:
    def encode(self, text: str, *, add_special_tokens: bool) -> list[int]:
        if add_special_tokens:
            raise AssertionError("special tokens must remain disabled")
        return [ord(character) for character in text]


class FixedLogitModel(nn.Module):
    def __init__(self, logits: torch.Tensor) -> None:
        super().__init__()
        self.logits = nn.Parameter(logits)

    def forward(self, **_: torch.Tensor) -> SimpleNamespace:
        return SimpleNamespace(logits=self.logits)


class Olmo3KronfluenceTests(unittest.TestCase):
    def test_installed_kronfluence_is_pinned(self) -> None:
        self.assertEqual(verify_kronfluence_version(), EXPECTED_KRONFLUENCE_VERSION)

    def test_token_window_dataset_preserves_order_and_builds_labels(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tokens.npy"
            tokens = np.arange(2 * 512, dtype="<u4").reshape(2, 512)
            np.save(path, tokens)
            dataset = TokenWindowDataset(path, expected_rows=2)

            first = dataset[0]
            self.assertEqual(len(dataset), 2)
            self.assertEqual(first["input_ids"].dtype, torch.long)
            torch.testing.assert_close(first["input_ids"], first["labels"])
            self.assertTrue(bool(torch.all(first["attention_mask"] == 1)))

    def test_conditional_query_masks_prompt_tokens(self) -> None:
        encoded = encode_conditional_query(CharacterTokenizer(), "Q:", " A")
        self.assertEqual(encoded["input_ids"].tolist(), [81, 58, 32, 65])
        self.assertEqual(encoded["labels"].tolist(), [-100, -100, 32, 65])

    def test_measurement_is_summed_completion_loss(self) -> None:
        logits = torch.tensor(
            [[[3.0, 1.0, 0.0], [0.0, 2.0, 1.0], [1.0, 0.0, 4.0]]]
        )
        batch = {
            "input_ids": torch.tensor([[0, 1, 2]]),
            "attention_mask": torch.ones((1, 3), dtype=torch.long),
            "labels": torch.tensor([[-100, 1, 2]]),
        }
        model = FixedLogitModel(logits)
        actual = Olmo3LanguageModelingTask().compute_measurement(batch, model)
        expected = F.cross_entropy(
            logits[:, :-1].reshape(-1, 3),
            torch.tensor([1, 2]),
            reduction="sum",
        )
        torch.testing.assert_close(actual, expected)

    def test_task_tracks_all_and_only_mlp_projections(self) -> None:
        names = Olmo3LanguageModelingTask().get_influence_tracked_modules()
        self.assertEqual(len(names), NUM_LAYERS * 3)
        self.assertEqual(names[0], "model.layers.0.mlp.gate_proj")
        self.assertEqual(names[-1], "model.layers.31.mlp.down_proj")
        self.assertTrue(all(".mlp." in name for name in names))

    def test_ruis_settings_are_explicit(self) -> None:
        factors = factor_arguments()
        scores = score_arguments(query_count=64)
        self.assertEqual(factors.strategy, "ekfac")
        self.assertFalse(factors.use_empirical_fisher)
        self.assertIsNone(factors.covariance_max_examples)
        self.assertIsNone(factors.lambda_max_examples)
        self.assertEqual(scores.damping_factor, 0.1)
        self.assertEqual(scores.query_gradient_accumulation_steps, 64)
        self.assertEqual(scores.query_gradient_low_rank, 32)

    def test_two_block_eigendecomposition_discards_cross_block_entries(self) -> None:
        matrix = torch.tensor(
            [
                [2.0, 0.0, 9.0, 9.0],
                [0.0, 3.0, 9.0, 9.0],
                [9.0, 9.0, 5.0, 0.0],
                [9.0, 9.0, 0.0, 7.0],
            ]
        )
        values, vectors = block_diagonal_eigh(matrix, blocks=2)
        self.assertEqual(values.tolist(), [2.0, 3.0, 5.0, 7.0])
        torch.testing.assert_close(vectors, torch.eye(4))

    def test_serialized_dtype_is_restored(self) -> None:
        self.assertIs(restore_torch_dtype("torch.bfloat16"), torch.bfloat16)
        self.assertEqual(restore_torch_dtype("unchanged"), "unchanged")


if __name__ == "__main__":
    unittest.main()
