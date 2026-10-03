import types
import unittest

import torch
from torch import nn

from olmo3_logit_lens import (
    argsort_logits,
    capture_residual_stream,
    logit_lens,
    processing_signature,
    reciprocal_rank,
    target_token_logits_and_ranks,
    target_token_ranks,
)


class AddLayer(nn.Module):
    def __init__(self, value: float) -> None:
        super().__init__()
        self.value = value

    def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        return hidden_states + self.value


class ScaleNorm(nn.Module):
    def __init__(self, scale: float) -> None:
        super().__init__()
        self.weight = nn.Parameter(torch.tensor(scale))

    def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        return hidden_states * self.weight


class TinyCausalLM(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.model = nn.Module()
        self.model.layers = nn.ModuleList([AddLayer(1.0), AddLayer(2.0)])
        self.model.norm = ScaleNorm(2.0)
        self.lm_head = nn.Linear(2, 3, bias=False)
        with torch.no_grad():
            self.lm_head.weight.copy_(
                torch.tensor(
                    [
                        [1.0, 0.0],
                        [0.0, 1.0],
                        [-1.0, 0.0],
                    ]
                )
            )

    def forward(self, input_ids: torch.Tensor, use_cache: bool = False):
        del use_cache
        hidden_states = torch.stack(
            (input_ids.float(), input_ids.float() + 0.5), dim=-1
        )
        for layer in self.model.layers:
            hidden_states = layer(hidden_states)
        logits = self.lm_head(self.model.norm(hidden_states))
        return types.SimpleNamespace(logits=logits)


class Olmo3LogitLensTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = TinyCausalLM().eval()

    def test_capture_uses_post_layer_outputs_and_removes_hooks(self) -> None:
        residual = capture_residual_stream(
            self.model,
            {"input_ids": torch.tensor([[1, 3]])},
        )

        self.assertEqual(tuple(residual.shape), (2, 2, 2))
        torch.testing.assert_close(
            residual[:, 0], torch.tensor([[2.0, 2.5], [4.0, 4.5]])
        )
        torch.testing.assert_close(
            residual[:, 1], torch.tensor([[4.0, 4.5], [6.0, 6.5]])
        )
        self.assertEqual(len(self.model.model.layers[0]._forward_hooks), 0)
        self.assertEqual(len(self.model.model.layers[1]._forward_hooks), 0)

    def test_capture_can_retain_only_selected_positions(self) -> None:
        residual = capture_residual_stream(
            self.model,
            {"input_ids": torch.tensor([[1, 3, 5]])},
            position_slice=slice(1, None),
        )
        self.assertEqual(tuple(residual.shape), (2, 2, 2))

    def test_logit_lens_applies_final_norm_and_lm_head(self) -> None:
        residual = torch.tensor([[[1.0, 2.0], [3.0, 4.0]]])
        logits = logit_lens(self.model, residual, chunk_size=1)

        expected = torch.tensor([[[2.0, 4.0, -2.0], [6.0, 8.0, -6.0]]])
        torch.testing.assert_close(logits, expected)

    def test_reciprocal_rank_and_processing_signature_match_reference(self) -> None:
        logits = torch.tensor(
            [
                [[3.0, 2.0, 1.0], [1.0, 3.0, 2.0]],
                [[1.0, 2.0, 3.0], [2.0, 1.0, 3.0]],
            ]
        )
        sorted_ids = argsort_logits(logits)
        reciprocal_ranks = reciprocal_rank(
            sorted_ids, shape=(2, 2), token_id=1
        )

        torch.testing.assert_close(
            reciprocal_ranks, torch.tensor([[0.5, 1.0], [0.5, 1 / 3]])
        )
        torch.testing.assert_close(
            processing_signature(reciprocal_ranks), torch.tensor([0.5, 1.0])
        )

    def test_selected_logits_and_ranks_match_full_projection(self) -> None:
        residual = torch.tensor([[[1.0, 2.0], [3.0, 4.0]]])
        full_logits = logit_lens(self.model, residual)
        selected_logits, ranks = target_token_logits_and_ranks(
            self.model, residual, [0, 1, 2], chunk_size=1
        )

        torch.testing.assert_close(selected_logits, full_logits)
        expected_ranks = torch.stack(
            [
                1
                / reciprocal_rank(
                    argsort_logits(full_logits), shape=(1, 2), token_id=token_id
                )
                for token_id in (0, 1, 2)
            ],
            dim=2,
        ).long()
        torch.testing.assert_close(ranks, expected_ranks)
        torch.testing.assert_close(
            target_token_ranks(self.model, residual, [0, 1, 2], chunk_size=1),
            expected_ranks,
        )

    def test_capture_requires_one_prompt(self) -> None:
        with self.assertRaisesRegex(ValueError, "batch size one"):
            capture_residual_stream(
                self.model,
                {"input_ids": torch.tensor([[1, 2], [3, 4]])},
            )


if __name__ == "__main__":
    unittest.main()
