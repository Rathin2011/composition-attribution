"""Small helpers for reading and editing decoder-layer activations."""

from __future__ import annotations

import torch


def hidden_from_output(output: torch.Tensor) -> torch.Tensor:
    """Validate and return one OLMo 3 decoder layer's activation tensor."""
    if not isinstance(output, torch.Tensor):
        raise TypeError("an OLMo 3 decoder layer must return a tensor")
    if output.ndim != 3 or output.shape[0] != 1:
        raise ValueError("layer output must have shape [1, positions, hidden]")
    return output


def add_to_position(
    output: torch.Tensor, position: int, delta: torch.Tensor
) -> torch.Tensor:
    """Add ``delta`` to one OLMo 3 token activation and preserve model dtype."""
    hidden = hidden_from_output(output)
    if not 0 <= position < hidden.shape[1]:
        raise ValueError("activation position is outside the sequence")
    if delta.shape != hidden.shape[2:]:
        raise ValueError("delta does not match the hidden dimension")

    patched = hidden.clone()
    patched[0, position] = (
        hidden[0, position].float() + delta.to(hidden.device)
    ).to(hidden.dtype)
    return patched
