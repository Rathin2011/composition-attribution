"""Khandelwal--Pavlick Logit Lens primitives adapted for OLMo 3.

The reference implementation is pinned at commit
``f12cef400ff946ab09cee988817daea939436698`` of
``apoorvkh/composing-functions``. It captures each decoder block's output,
applies the model's final normalization and language-model head, and measures
target tokens against the complete vocabulary.

PyTorch forward hooks replace the reference implementation's NNsight wrapper.
That changes only activation capture, not the residual-stream location or
Logit Lens projection.

File-level input
----------------
This is a library module, not a command-line program, so it does not read a
JSON file itself. Its public functions receive:

* a loaded Hugging Face causal language model exposing ``model.model.layers``,
  ``model.model.norm``, and ``model.lm_head``;
* tokenized prompt tensors such as ``input_ids``; and
* target vocabulary token IDs whose internal evidence should be measured.

The later experiment runner will obtain those inputs from one row of
``correct_query_contexts.jsonl`` and the pinned stage-one OLMo 3 checkpoint.

File-level output
-----------------
The functions return in-memory CPU tensors. This module does not write files.
The main outputs are:

* post-block residual activations, shaped ``[P, L, D]``;
* selected target-token logits, shaped ``[P, L, K]``; and
* selected target-token vocabulary ranks, shaped ``[P, L, K]``.

Here ``P`` is the number of retained prompt positions, ``L`` the number of
decoder blocks, ``D`` the model width, ``V`` the complete vocabulary size, and
``K`` the number of target token IDs. Layer indexing refers to post-decoder-
block outputs; the embedding state is not included as an additional layer.

High-level functional flow
--------------------------
The experiment runner will use these functions in this order:

1. Tokenize one complete ICL prompt and locate its final query positions.
2. ``capture_residual_stream`` runs one ordinary forward pass and captures the
   post-block activation at every layer for those positions.
3. ``target_token_logits_and_ranks`` applies the final RMSNorm and LM head to
   each captured activation, retaining the target logits and calculating their
   ranks against all ``V`` vocabulary entries.
4. The runner converts ranks to reciprocal ranks with ``1 / rank``.
5. ``processing_signature`` takes the best reciprocal rank across final-query
   positions separately at every layer, matching Khandelwal--Pavlick.

Function dependencies
---------------------
``capture_residual_stream`` uses ``_decoder_layers`` and
``_layer_hidden_state``. ``logit_lens`` and
``target_token_logits_and_ranks`` use ``_readout_modules``.
``target_token_ranks`` is a convenience wrapper around
``target_token_logits_and_ranks``. ``argsort_logits`` and ``reciprocal_rank``
provide the reference full-sort calculation used to verify the optimized rank
calculation in tests.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import torch


REFERENCE_CODE_COMMIT = "f12cef400ff946ab09cee988817daea939436698"


def _decoder_layers(model: Any) -> Any:
    """Locate the ordered decoder blocks in a Hugging Face OLMo model.

    Input:
        ``model``: a loaded causal language model.
    Output:
        The model's ordered, iterable decoder-block collection.
    Role:
        ``capture_residual_stream`` registers one hook on every returned block.
        Failing explicitly here prevents accidentally capturing activations
        from a different model component.
    """

    try:
        # OLMo's Hugging Face wrapper stores the bare transformer at
        # ``model.model`` and its sequential decoder blocks at ``layers``.
        return model.model.layers
    except AttributeError as error:
        raise TypeError(
            "model must expose decoder layers at model.model.layers"
        ) from error


def _layer_hidden_state(output: Any) -> torch.Tensor:
    """Extract the residual-stream tensor from one decoder block's output.

    Input:
        ``output``: the object produced by a decoder block's forward method.
        Hugging Face blocks may return the hidden tensor directly or place it
        first in a tuple/list alongside auxiliary values.
    Output:
        A tensor shaped ``[batch, positions, hidden_size]``.
    Role:
        Gives the hook in ``capture_residual_stream`` one consistent tensor
        representation independent of the block's container type.
    """

    # In tuple/list outputs, element zero is the updated hidden state. A direct
    # tensor output is already the hidden state.
    hidden_state = output[0] if isinstance(output, (tuple, list)) else output
    if not isinstance(hidden_state, torch.Tensor) or hidden_state.ndim != 3:
        raise TypeError(
            "decoder layer output must contain [batch, positions, hidden] activations"
        )
    return hidden_state


def capture_residual_stream(
    model: Any,
    model_inputs: Mapping[str, torch.Tensor],
    *,
    position_slice: slice | None = None,
) -> torch.Tensor:
    """Run one prompt and capture its post-block residual activations.

    Input:
        ``model``: the loaded causal language model.
        ``model_inputs``: tokenized prompt tensors. ``input_ids`` must have
        shape ``[1, sequence_length]`` because the paper analyzes one prompt at
        a time.
        ``position_slice``: optional positions to retain, normally the slice
        spanning the final ``Q: landmark\nA:`` query.
    Output:
        A CPU tensor shaped ``[positions, layers, hidden_size]``.
    Role:
        Supplies the internal states that Logit Lens will independently decode
        at every retained position and decoder layer.

    This matches ``composing_functions.lens.residual_stream``. Selecting only
    final-query positions during capture is equivalent to slicing the complete
    residual stream afterward and avoids retaining ICL-context activations.
    """

    # Validate batch size before hooks are installed. Variable-length prompts
    # are fine; only multi-prompt batching is intentionally disallowed here.
    input_ids = model_inputs.get("input_ids")
    if input_ids is None or input_ids.ndim != 2 or input_ids.shape[0] != 1:
        raise ValueError(
            "capture_residual_stream requires input_ids with batch size one"
        )

    layers = _decoder_layers(model)
    # Preallocate by layer index so the final tensor preserves model order even
    # though each hook stores its own output independently.
    captured: list[torch.Tensor | None] = [None] * len(layers)
    handles = []

    def capture_layer(layer_index: int):
        """Build a hook whose closure remembers which layer it belongs to."""

        def hook(_module: Any, _inputs: Any, output: Any) -> None:
            # Remove the one-element batch dimension: [1, T, D] -> [T, D].
            hidden_state = _layer_hidden_state(output)[0]
            if position_slice is not None:
                # Retain only final-query rows when requested. This operation
                # occurs after the block has processed the complete prompt, so
                # the retained rows still contain information from the ICL
                # context through causal attention.
                hidden_state = hidden_state[position_slice]
            # Logit Lens is an inference-only analysis. Detaching prevents an
            # autograd graph from being kept, and CPU transfer frees GPU memory.
            captured[layer_index] = hidden_state.detach().cpu()

        return hook

    try:
        # A forward hook fires after its corresponding decoder block and sees
        # that block's output residual state.
        for layer_index, layer in enumerate(layers):
            handles.append(layer.register_forward_hook(capture_layer(layer_index)))
        with torch.inference_mode():
            # use_cache=False avoids allocating autoregressive KV caches; this
            # is a single full-prompt forward pass rather than generation.
            model(**model_inputs, use_cache=False)
    finally:
        # Always remove hooks, including when the forward pass raises. Leaving
        # them installed would duplicate captures on later prompts.
        for handle in handles:
            handle.remove()

    if any(activation is None for activation in captured):
        raise RuntimeError("not every decoder layer produced a captured activation")

    activations = [activation for activation in captured if activation is not None]
    # Each item is [P, D]. Stacking on dimension one gives [P, L, D], which is
    # the same axis order used by the paper's implementation.
    return torch.stack(activations, dim=1)


def _readout_modules(model: Any) -> tuple[Any, Any]:
    """Locate OLMo's final RMSNorm and vocabulary unembedding modules.

    Input:
        ``model``: a loaded Hugging Face OLMo causal language model.
    Output:
        ``(final_norm, lm_head)``. ``final_norm`` maps residual activations to
        the representation normally consumed by the output head. ``lm_head``
        maps that representation to one logit per vocabulary entry.
    Role:
        Both Logit Lens projection functions use exactly the model's learned
        final readout path rather than inventing a separate decoder.
    """

    try:
        return model.model.norm, model.lm_head
    except AttributeError as error:
        raise TypeError(
            "model must expose model.model.norm and model.lm_head"
        ) from error


def logit_lens(
    model: Any,
    residual_stream: torch.Tensor,
    *,
    chunk_size: int | None = None,
) -> torch.Tensor:
    """Project every retained activation into full-vocabulary logits.

    Input:
        ``model``: supplies final RMSNorm and LM head.
        ``residual_stream``: CPU or accelerator tensor shaped ``[P, L, D]``.
        ``chunk_size``: number of flattened activation rows projected at once.
    Output:
        A CPU tensor shaped ``[P, L, V]`` containing every vocabulary logit.
    Role:
        This is the literal Logit Lens operation used in the reference paper.
        It is useful for validation and analyses that truly need all tokens.
        The main experiment uses ``target_token_logits_and_ranks`` to avoid
        retaining this much larger tensor.

    ``chunk_size`` changes only temporary accelerator memory use, not the
    mathematical result.
    """

    if residual_stream.ndim != 3:
        raise ValueError(
            "residual_stream must have shape [positions, layers, hidden_size]"
        )

    final_norm, lm_head = _readout_modules(model)
    positions, layers, hidden_size = residual_stream.shape
    # RMSNorm and the LM head operate on the final dimension. Flattening P and
    # L lets them process every position-layer pair as an ordinary batch row.
    flat_activations = residual_stream.reshape(positions * layers, hidden_size)
    if chunk_size is None:
        chunk_size = len(flat_activations)
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    # device_map="auto" may place the norm and head on specific devices, so
    # consult the modules rather than assuming a device.
    norm_device = next(final_norm.parameters()).device
    lm_head_device = next(lm_head.parameters()).device
    logits = []
    with torch.inference_mode():
        for start in range(0, len(flat_activations), chunk_size):
            # [chunk, D]
            activation_chunk = flat_activations[start : start + chunk_size].to(
                norm_device
            )
            # Apply the same final normalization used before normal next-token
            # prediction, but to an intermediate layer's residual state.
            normalized = final_norm(activation_chunk)
            # The LM head is the unembedding: [chunk, D] -> [chunk, V].
            logits.append(lm_head(normalized.to(lm_head_device)).cpu())

    # Restore separate prompt-position and model-layer axes.
    return torch.cat(logits, dim=0).reshape(positions, layers, -1)


def argsort_logits(logits: torch.Tensor) -> torch.Tensor:
    """Sort complete-vocabulary token IDs by descending logit.

    Input:
        Full logits shaped ``[P, L, V]``.
    Output:
        Integer token IDs shaped ``[P * L, V]``. Row position zero contains
        the highest-logit token ID for that position-layer pair.
    Role:
        Reproduces the reference paper's explicit sorting procedure. The tests
        use it as an independent check on the optimized rank calculation.
    """

    if logits.ndim != 3:
        raise ValueError("logits must have shape [positions, layers, vocab_size]")
    # Flattening P and L creates one independent vocabulary-ranking problem
    # for every position-layer pair.
    return torch.argsort(
        logits.reshape(-1, logits.shape[-1]), descending=True, dim=1
    )


def target_token_logits_and_ranks(
    model: Any,
    residual_stream: torch.Tensor,
    token_ids: list[int],
    *,
    chunk_size: int = 32,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Calculate selected raw logits and full-vocabulary ranks efficiently.

    Input:
        ``model``: supplies the final RMSNorm and LM head.
        ``residual_stream``: tensor shaped ``[P, L, D]``.
        ``token_ids``: ``K`` vocabulary IDs to measure, such as the first token
        IDs for ``x``, ``F(x)``, and ``G(F(x))``.
        ``chunk_size``: flattened activation rows processed simultaneously.
    Output:
        ``(target_logits, ranks)`` as two CPU tensors shaped ``[P, L, K]``.
        ``target_logits[p,l,k]`` is the raw Logit Lens logit of target ``k``.
        ``ranks[p,l,k]`` is its one-based rank among all ``V`` vocabulary
        entries at the same position and layer.
    Role:
        Provides the exact measurements saved by the upcoming experiment
        runner without storing a full ``[P, L, V]`` tensor per prompt.

    A rank is one plus the number of vocabulary logits strictly greater than
    the target logit. Tied tokens therefore receive their shared best rank.
    """

    if residual_stream.ndim != 3:
        raise ValueError(
            "residual_stream must have shape [positions, layers, hidden_size]"
        )
    if not token_ids:
        raise ValueError("token_ids must not be empty")
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    final_norm, lm_head = _readout_modules(model)
    positions, layers, hidden_size = residual_stream.shape
    # As in logit_lens(), treat every position-layer activation as a batch row.
    flat_activations = residual_stream.reshape(positions * layers, hidden_size)
    norm_device = next(final_norm.parameters()).device
    lm_head_device = next(lm_head.parameters()).device
    target_logit_chunks = []
    rank_chunks = []

    with torch.inference_mode():
        for start in range(0, len(flat_activations), chunk_size):
            # Project this activation chunk through the exact final readout.
            activation_chunk = flat_activations[start : start + chunk_size].to(
                norm_device
            )
            normalized = final_norm(activation_chunk)
            # logits: [chunk, V]
            logits = lm_head(normalized.to(lm_head_device))
            # Select only K target columns for the values we will save:
            # selected_logits: [chunk, K].
            selected_logits = logits[:, token_ids]
            # Broadcasting compares every vocabulary logit against each target:
            # [chunk,V,1] > [chunk,1,K] -> [chunk,V,K]. Summing over V counts
            # how many tokens outrank each target, producing [chunk,K].
            ranks = 1 + (logits.unsqueeze(2) > selected_logits.unsqueeze(1)).sum(
                dim=1
            )
            # Move only the small target outputs to CPU. The complete V-wide
            # logits tensor is released after this loop iteration.
            target_logit_chunks.append(selected_logits.cpu())
            rank_chunks.append(ranks.cpu())

    output_shape = (positions, layers, len(token_ids))
    # Undo the P*L flattening and restore semantically named axes.
    target_logits = torch.cat(target_logit_chunks, dim=0).reshape(output_shape)
    ranks = torch.cat(rank_chunks, dim=0).reshape(output_shape)
    return target_logits, ranks


def target_token_ranks(
    model: Any,
    residual_stream: torch.Tensor,
    token_ids: list[int],
    *,
    chunk_size: int = 32,
) -> torch.Tensor:
    """Return only selected targets' one-based full-vocabulary ranks.

    Input:
        The same model, ``[P,L,D]`` residual stream, target IDs, and chunk size
        accepted by ``target_token_logits_and_ranks``.
    Output:
        An integer CPU tensor shaped ``[P,L,K]``.
    Role:
        Convenience interface for analyses that need ranks but do not save raw
        target logits. It delegates the calculation to the shared optimized
        implementation so the two interfaces cannot disagree.
    """

    _, ranks = target_token_logits_and_ranks(
        model,
        residual_stream,
        token_ids,
        chunk_size=chunk_size,
    )
    return ranks


def reciprocal_rank(
    sort_indices: torch.Tensor,
    shape: tuple[int, int],
    token_id: int,
) -> torch.Tensor:
    """Recover one token's reciprocal rank from explicitly sorted IDs.

    Input:
        ``sort_indices`` shaped ``[P*L,V]`` from ``argsort_logits``;
        ``shape=(P,L)``; and one target ``token_id``.
    Output:
        A floating tensor shaped ``[P,L]`` containing ``1 / rank``.
    Role:
        Mirrors the reference implementation exactly and serves as the
        independent correctness oracle for optimized rank tests. The runner can
        calculate reciprocal rank directly as ``1 / ranks.float()``.
    """

    # Each vocabulary ID should appear exactly once in every sorted row. The
    # second nonzero coordinate is its zero-based location in that row.
    ranks = (sort_indices == token_id).nonzero(as_tuple=False)[:, 1]
    expected = shape[0] * shape[1]
    if len(ranks) != expected:
        raise ValueError(
            "token_id must occur exactly once in every sorted vocabulary row"
        )
    # Add one to convert the zero-based location to conventional rank before
    # taking its reciprocal.
    return 1 / (ranks.reshape(*shape) + 1)


def processing_signature(reciprocal_ranks: torch.Tensor) -> torch.Tensor:
    """Collapse query positions into the paper's layerwise evidence curve.

    Input:
        Reciprocal ranks for one target token, shaped ``[P,L]``. ``P`` spans
        every token position in the final query and ``L`` spans model layers.
    Output:
        A tensor shaped ``[L]``. Each value is the maximum reciprocal rank over
        the ``P`` query positions at that layer.
    Role:
        Implements Khandelwal--Pavlick's processing signature. Later
        classification uses the largest value of this layerwise curve as the
        prompt's strongest intermediate-country evidence.
    """

    if reciprocal_ranks.ndim != 2:
        raise ValueError(
            "reciprocal_ranks must have shape [positions, layers]"
        )
    # dim=0 is the prompt-position axis, leaving one best-evidence value per
    # decoder layer.
    return reciprocal_ranks.max(dim=0).values
