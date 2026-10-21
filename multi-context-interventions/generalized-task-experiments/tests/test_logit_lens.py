"""Tensor-level tests for the generalized Logit-Lens implementation."""

from __future__ import annotations

import types
import unittest

import torch
from torch import nn

from logit_lens import candidate_logits_and_ranks, capture_residual_stream


class AddLayer(nn.Module):
    def __init__(self, value: float) -> None:
        super().__init__()
        self.value = value

    def forward(self, hidden: torch.Tensor) -> torch.Tensor:
        return hidden + self.value


class ScaleNorm(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.weight = nn.Parameter(torch.tensor(2.0))

    def forward(self, hidden: torch.Tensor) -> torch.Tensor:
        return hidden * self.weight


class TinyModel(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.model = nn.Module()
        self.model.layers = nn.ModuleList([AddLayer(1.0), AddLayer(2.0)])
        self.model.norm = ScaleNorm()
        self.lm_head = nn.Linear(2, 4, bias=False)
        with torch.no_grad():
            self.lm_head.weight.copy_(
                torch.tensor([[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0], [0.5, 0.5]])
            )

    def forward(self, input_ids: torch.Tensor, use_cache: bool = False):
        del use_cache
        hidden = torch.stack((input_ids.float(), input_ids.float() + 0.5), dim=-1)
        for layer in self.model.layers:
            hidden = layer(hidden)
        return types.SimpleNamespace(logits=self.lm_head(self.model.norm(hidden)))


class LogitLensTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = TinyModel().eval()

    def test_capture_and_candidate_ranks_match_full_vocabulary(self) -> None:
        residual = capture_residual_stream(
            self.model,
            {"input_ids": torch.tensor([[1, 3, 5]])},
            position_slice=slice(1, None),
        )
        self.assertEqual(tuple(residual.shape), (2, 2, 2))
        logits, ranks = candidate_logits_and_ranks(
            self.model,
            residual,
            [0, 1, 3],
            activation_chunk_size=1,
            candidate_chunk_size=1,
        )
        self.assertEqual(tuple(logits.shape), (2, 2, 3))
        self.assertEqual(tuple(ranks.shape), (2, 2, 3))

        full = self.model.lm_head(self.model.model.norm(residual))
        torch.testing.assert_close(logits, full[:, :, [0, 1, 3]])
        expected = torch.stack(
            [1 + (full > full[:, :, token_id].unsqueeze(2)).sum(dim=2) for token_id in (0, 1, 3)],
            dim=2,
        )
        torch.testing.assert_close(ranks, expected)


if __name__ == "__main__":
    unittest.main()
