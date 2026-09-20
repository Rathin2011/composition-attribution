"""The unchanged final-normalization/unembedding logit-lens readout."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import torch


def unit_vector(vector: torch.Tensor) -> torch.Tensor:
    """Return a finite, nonzero one-dimensional vector normalized on CPU."""
    vector = vector.detach().float().cpu()
    if vector.ndim != 1 or not torch.isfinite(vector).all() or vector.norm() <= 1e-12:
        raise ValueError("direction must be finite, one-dimensional, and nonzero")
    return vector / vector.norm()


def centered_token_direction(
    weight_row: torch.Tensor,
    vocabulary_mean: torch.Tensor,
    rms_weight: torch.Tensor,
) -> torch.Tensor:
    """Return a token's centered logit-numerator direction in residual space.

    OLMo 3's final RMS normalization scales ``h`` elementwise by ``gamma``.
    Consequently the numerator of ``logit(token) - mean(logits)`` points along
    ``gamma * (W_token - mean(W))``. This direction does not remove the
    nonlinear RMS denominator and is not a semantic concept direction.
    """
    if weight_row.shape != vocabulary_mean.shape or weight_row.shape != rms_weight.shape:
        raise ValueError("head row, vocabulary mean, and RMS weights must have equal shape")
    return unit_vector((weight_row.float().cpu() - vocabulary_mean.float().cpu()) * rms_weight.float().cpu())


@dataclass(frozen=True)
class ReadoutGeometry:
    """Cached output-head quantities used to construct token directions."""

    head: torch.Tensor
    vocabulary_mean: torch.Tensor
    rms_weight: torch.Tensor

    @classmethod
    def from_model(cls, model: Any) -> "ReadoutGeometry":
        head = model.lm_head.weight.detach()
        return cls(
            head=head,
            vocabulary_mean=head.mean(dim=0, dtype=torch.float32).cpu(),
            rms_weight=model.model.norm.weight.detach().float().cpu(),
        )

    def centered_token_direction(self, token_id: int) -> torch.Tensor:
        """Return the unit direction that raises one token relative to the mean.

        Input:
            One vocabulary token ID.
        Output:
            ``unit(gamma * (W_token - mean(W)))`` as a float32 CPU vector.
        """
        if not 0 <= token_id < self.head.shape[0]:
            raise ValueError("token ID is outside the output vocabulary")
        return centered_token_direction(
            self.head[token_id].detach().cpu(),
            self.vocabulary_mean,
            self.rms_weight,
        )

    def raw_token_direction(self, token_id: int) -> torch.Tensor:
        """Return one token's unnormalized RMS-weighted readout direction.

        Input:
            One vocabulary token ID.
        Output:
            ``gamma * W_token`` as a float64 CPU vector.

        The capital-preserving experiment uses this raw direction because it
        protects the capital's actual local logit numerator, not a unit-length
        or vocabulary-centered proxy.
        """
        if not 0 <= token_id < self.head.shape[0]:
            raise ValueError("token ID is outside the output vocabulary")
        return (
            self.head[token_id].detach().double().cpu()
            * self.rms_weight.double()
        )

    def vocabulary_mean_direction(self) -> torch.Tensor:
        """Return ``gamma * mean(W)`` as a float64 CPU vector.

        Protecting this direction together with the raw capital direction also
        protects the capital logit relative to the vocabulary-wide mean.
        """
        return self.vocabulary_mean.double() * self.rms_weight.double()


def measure_token_evidence(
    model: Any, hidden: torch.Tensor, targets: dict[str, int]
) -> dict[str, dict[str, float | int]]:
    """Apply final norm and unembedding, then report each target token's rank.

    Rank is one plus the number of vocabulary logits strictly larger than the
    target logit. Therefore rank 1 is the highest-scoring vocabulary token.
    """
    if hidden.ndim != 1:
        raise ValueError("logit-lens input must be one hidden vector")
    norm = model.model.norm
    head = model.lm_head
    with torch.inference_mode():
        normalized = norm(hidden.to(device=norm.weight.device, dtype=norm.weight.dtype))
        logits = head(
            normalized.to(device=head.weight.device, dtype=head.weight.dtype)
        ).float()
        logprobs = logits.log_softmax(dim=-1)

    result: dict[str, dict[str, float | int]] = {}
    for name, token_id in targets.items():
        if not 0 <= token_id < logits.shape[-1]:
            raise ValueError(f"target token {name!r} is outside the vocabulary")
        result[name] = {
            "token_id": token_id,
            "rank": 1 + (logits > logits[token_id]).sum().item(),
            "logit": logits[token_id].item(),
            "logprob": logprobs[token_id].item(),
        }
    return result
