"""Logit-lens primitives adapted from Khandelwal and Pavlick for OLMo 3.

The reference implementation is pinned at commit
``f12cef400ff946ab09cee988817daea939436698`` of
``apoorvkh/composing-functions``.  It captures each decoder layer's output,
applies the model's final normalization and language-model head, and measures
the reciprocal rank of task-variable tokens in the resulting vocabulary
logits.

This module uses PyTorch forward hooks instead of the reference code's NNsight
wrapper.  The substitution is limited to activation capture; the residual
stream location and logit-lens projection are the same.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import torch


REFERENCE_CODE_COMMIT = "f12cef400ff946ab09cee988817daea939436698"


def _decoder_layers(model: Any) -> Any:
    try:
        return model.model.layers
    except AttributeError as error:
        raise TypeError("model must expose decoder layers at model.model.layers") from error


def _layer_hidden_state(output: Any) -> torch.Tensor:
    hidden_state = output[0] if isinstance(output, (tuple, list)) else output
    if not isinstance(hidden_state, torch.Tensor) or hidden_state.ndim != 3:
        raise TypeError("decoder layer output must contain [batch, positions, hidden] activations")
    return hidden_state


def capture_residual_stream(
    model: Any,
    model_inputs: Mapping[str, torch.Tensor],
    *,
    position_slice: slice | None = None,
) -> torch.Tensor:
    """Capture post-layer residual streams for one prompt.

    Returns a CPU tensor with shape ``[positions, layers, hidden_size]``.  This
    matches ``composing_functions.lens.residual_stream`` in the paper code.
    A batch size of one is required because the reference analysis processes
    one query at a time. ``position_slice`` can retain only the query-token
    positions during capture, which is equivalent to slicing the completed
    residual stream and avoids transferring the ICL context activations.
    """

    input_ids = model_inputs.get("input_ids")
    if input_ids is None or input_ids.ndim != 2 or input_ids.shape[0] != 1:
        raise ValueError("capture_residual_stream requires input_ids with batch size one")

    layers = _decoder_layers(model)
    captured: list[torch.Tensor | None] = [None] * len(layers)
    handles = []

    def capture_layer(layer_index: int):
        def hook(_module: Any, _inputs: Any, output: Any) -> None:
            hidden_state = _layer_hidden_state(output)[0]
            if position_slice is not None:
                hidden_state = hidden_state[position_slice]
            captured[layer_index] = hidden_state.detach().cpu()

        return hook

    try:
        for layer_index, layer in enumerate(layers):
            handles.append(layer.register_forward_hook(capture_layer(layer_index)))

        with torch.inference_mode():
            model(**model_inputs, use_cache=False)
    finally:
        for handle in handles:
            handle.remove()

    if any(activation is None for activation in captured):
        raise RuntimeError("not every decoder layer produced a captured activation")

    activations = [activation for activation in captured if activation is not None]
    return torch.stack(activations, dim=1)


def logit_lens(
    model: Any,
    residual_stream: torch.Tensor,
    *,
    chunk_size: int | None = None,
) -> torch.Tensor:
    """Project residual streams into vocabulary space.

    The returned CPU tensor has shape ``[positions, layers, vocab_size]``.
    ``chunk_size`` only limits temporary accelerator memory and does not change
    the calculation.
    """

    if residual_stream.ndim != 3:
        raise ValueError("residual_stream must have shape [positions, layers, hidden_size]")

    try:
        final_norm = model.model.norm
        lm_head = model.lm_head
    except AttributeError as error:
        raise TypeError("model must expose model.model.norm and model.lm_head") from error

    positions, layers, hidden_size = residual_stream.shape
    flat_activations = residual_stream.reshape(positions * layers, hidden_size)
    if chunk_size is None:
        chunk_size = len(flat_activations)
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    norm_device = next(final_norm.parameters()).device
    lm_head_device = next(lm_head.parameters()).device
    logits = []
    with torch.inference_mode():
        for start in range(0, len(flat_activations), chunk_size):
            activation_chunk = flat_activations[start : start + chunk_size].to(norm_device)
            normalized = final_norm(activation_chunk)
            chunk_logits = lm_head(normalized.to(lm_head_device))
            logits.append(chunk_logits.cpu())

    return torch.cat(logits, dim=0).reshape(positions, layers, -1)


def argsort_logits(logits: torch.Tensor) -> torch.Tensor:
    """Sort vocabulary indices by descending logit, as in the paper code."""

    if logits.ndim != 3:
        raise ValueError("logits must have shape [positions, layers, vocab_size]")
    return torch.argsort(logits.reshape(-1, logits.shape[-1]), descending=True, dim=1)


def target_token_ranks(
    model: Any,
    residual_stream: torch.Tensor,
    token_ids: list[int],
    *,
    chunk_size: int = 32,
) -> torch.Tensor:
    """Calculate selected vocabulary ranks without retaining full logits.

    Returns a CPU integer tensor with shape
    ``[positions, layers, len(token_ids)]``. A rank is one plus the number of
    vocabulary logits strictly greater than the target logit. This matches a
    descending vocabulary sort whenever logits are distinct and gives tied
    tokens their shared best rank.
    """

    if residual_stream.ndim != 3:
        raise ValueError("residual_stream must have shape [positions, layers, hidden_size]")
    if not token_ids:
        raise ValueError("token_ids must not be empty")
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    try:
        final_norm = model.model.norm
        lm_head = model.lm_head
    except AttributeError as error:
        raise TypeError("model must expose model.model.norm and model.lm_head") from error

    positions, layers, hidden_size = residual_stream.shape
    flat_activations = residual_stream.reshape(positions * layers, hidden_size)
    norm_device = next(final_norm.parameters()).device
    lm_head_device = next(lm_head.parameters()).device
    rank_chunks = []

    with torch.inference_mode():
        for start in range(0, len(flat_activations), chunk_size):
            activation_chunk = flat_activations[start : start + chunk_size].to(norm_device)
            normalized = final_norm(activation_chunk)
            logits = lm_head(normalized.to(lm_head_device))
            ranks = [
                1 + (logits > logits[:, token_id, None]).sum(dim=1)
                for token_id in token_ids
            ]
            rank_chunks.append(torch.stack(ranks, dim=1).cpu())

    return torch.cat(rank_chunks, dim=0).reshape(positions, layers, len(token_ids))


def reciprocal_rank(
    sort_indices: torch.Tensor,
    shape: tuple[int, int],
    token_id: int,
) -> torch.Tensor:
    """Return a target token's reciprocal rank for every position and layer."""

    ranks = (sort_indices == token_id).nonzero(as_tuple=False)[:, 1]
    expected = shape[0] * shape[1]
    if len(ranks) != expected:
        raise ValueError("token_id must occur exactly once in every sorted vocabulary row")
    return 1 / (ranks.reshape(*shape) + 1)


def processing_signature(reciprocal_ranks: torch.Tensor) -> torch.Tensor:
    """Take maximum reciprocal rank across query-token positions per layer."""

    if reciprocal_ranks.ndim != 2:
        raise ValueError("reciprocal_ranks must have shape [positions, layers]")
    return reciprocal_ranks.max(dim=0).values
