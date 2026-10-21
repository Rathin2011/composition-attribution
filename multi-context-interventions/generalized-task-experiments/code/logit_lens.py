"""Task-independent OLMo residual capture and Logit-Lens projection.

This module contains only tensor operations.  It neither knows which
composition task is running nor reads/writes experiment files.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import torch


def _decoder_layers(model: Any) -> Any:
    """Return the ordered Hugging Face OLMo decoder blocks."""

    try:
        return model.model.layers
    except AttributeError as error:
        raise TypeError(
            "model must expose decoder layers at model.model.layers"
        ) from error


def _layer_hidden_state(output: Any) -> torch.Tensor:
    """Extract a ``[batch, positions, hidden]`` tensor from a block output."""

    hidden = output[0] if isinstance(output, (tuple, list)) else output
    if not isinstance(hidden, torch.Tensor) or hidden.ndim != 3:
        raise TypeError("decoder output must contain a rank-three hidden tensor")
    return hidden


def capture_residual_stream(
    model: Any,
    model_inputs: Mapping[str, torch.Tensor],
    *,
    position_slice: slice,
) -> torch.Tensor:
    """Run one prompt and return selected post-block activations.

    Input:
        One tokenized prompt and a slice selecting its final-query rows.
    Output:
        CPU tensor ``[query_positions, decoder_layers, hidden_size]``.
    """

    input_ids = model_inputs.get("input_ids")
    if input_ids is None or input_ids.ndim != 2 or input_ids.shape[0] != 1:
        raise ValueError("capture_residual_stream requires batch size one")

    layers = _decoder_layers(model)
    captured: list[torch.Tensor | None] = [None] * len(layers)
    handles = []

    def capture_layer(layer_index: int):
        def hook(_module: Any, _inputs: Any, output: Any) -> None:
            hidden = _layer_hidden_state(output)[0, position_slice]
            captured[layer_index] = hidden.detach().cpu()

        return hook

    try:
        for layer_index, layer in enumerate(layers):
            handles.append(layer.register_forward_hook(capture_layer(layer_index)))
        with torch.inference_mode():
            model(**model_inputs, use_cache=False)
    finally:
        for handle in handles:
            handle.remove()

    if any(value is None for value in captured):
        raise RuntimeError("not every decoder layer produced an activation")
    return torch.stack([value for value in captured if value is not None], dim=1)


def _readout_modules(model: Any) -> tuple[Any, Any]:
    """Return OLMo's final RMSNorm and vocabulary unembedding modules."""

    try:
        return model.model.norm, model.lm_head
    except AttributeError as error:
        raise TypeError("model must expose model.model.norm and model.lm_head") from error


def candidate_logits_and_ranks(
    model: Any,
    residual_stream: torch.Tensor,
    token_ids: Sequence[int],
    *,
    activation_chunk_size: int = 32,
    candidate_chunk_size: int = 16,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Project candidate tokens and rank each against the complete vocabulary.

    Inputs:
        ``residual_stream`` has shape ``[P,L,D]`` and ``token_ids`` contains
        one first-token ID for every possible ``Fx`` value in catalog order.
    Outputs:
        Raw logits and one-based full-vocabulary ranks, both ``[P,L,K]``.

    Candidates are rank-computed in small chunks.  This keeps the operation
    usable for tasks with many possible intermediates without changing the
    exact rank definition: ``1 + count(vocabulary_logit > target_logit)``.
    """

    if residual_stream.ndim != 3:
        raise ValueError("residual_stream must have shape [P,L,D]")
    if not token_ids:
        raise ValueError("token_ids must not be empty")
    if activation_chunk_size <= 0 or candidate_chunk_size <= 0:
        raise ValueError("chunk sizes must be positive")

    final_norm, lm_head = _readout_modules(model)
    positions, layers, hidden_size = residual_stream.shape
    flat = residual_stream.reshape(positions * layers, hidden_size)
    norm_device = next(final_norm.parameters()).device
    head_device = next(lm_head.parameters()).device
    token_index = torch.tensor(list(token_ids), dtype=torch.long, device=head_device)
    logit_chunks = []
    rank_chunks = []

    with torch.inference_mode():
        for start in range(0, len(flat), activation_chunk_size):
            activations = flat[start : start + activation_chunk_size].to(norm_device)
            normalized = final_norm(activations)
            vocabulary_logits = lm_head(normalized.to(head_device))
            selected = vocabulary_logits.index_select(1, token_index)

            candidate_ranks = []
            for candidate_start in range(0, len(token_ids), candidate_chunk_size):
                candidate_logits = selected[
                    :, candidate_start : candidate_start + candidate_chunk_size
                ]
                ranks = 1 + (
                    vocabulary_logits.unsqueeze(2) > candidate_logits.unsqueeze(1)
                ).sum(dim=1)
                candidate_ranks.append(ranks)

            logit_chunks.append(selected.cpu())
            rank_chunks.append(torch.cat(candidate_ranks, dim=1).cpu())

    shape = (positions, layers, len(token_ids))
    return (
        torch.cat(logit_chunks, dim=0).reshape(shape),
        torch.cat(rank_chunks, dim=0).reshape(shape),
    )
