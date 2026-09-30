"""Activation-space primitives and model hooks for J-Lens interventions.

This module constructs token directions, performs the paper's steering,
ablation, and coordinate-swap edits, and temporarily installs one edit at a
selected transformer layer. It does not load a model, choose an experimental
layer, or run queries.

The J-Lens convention used here is:

    final_residual_change = J_l @ layer_l_residual_change

If ``w_t`` is the unembedding row for token ``t``, then the layer-``l``
direction that locally changes token ``t``'s final logit is:

    v_t = J_l.T @ w_t
"""

from __future__ import annotations

from collections.abc import Sequence
import math
from typing import Literal

import torch
from torch import nn


InterventionKind = Literal["steer", "ablate", "swap"]


def _validate_direction_for(
    activations: torch.Tensor,
    direction: torch.Tensor,
) -> torch.Tensor:
    """Validate a direction and place it beside the activation tensor.

    Args:
        activations: Floating tensor shaped ``[..., d_model]``.
        direction: Floating one-dimensional tensor shaped ``[d_model]``.

    Returns:
        A detached copy of ``direction`` on the activation device in float32.

    Raises:
        ValueError: If either tensor has an invalid shape, contains non-finite
            values, or if the direction has zero norm.
        TypeError: If either tensor is not floating point.
    """

    if activations.ndim < 1:
        raise ValueError("activations must have at least one dimension")
    if not activations.is_floating_point():
        raise TypeError("activations must be floating point")
    if not torch.isfinite(activations).all():
        raise ValueError("activations must contain only finite values")

    if direction.ndim != 1:
        raise ValueError("direction must have shape [d_model]")
    if direction.shape[0] != activations.shape[-1]:
        raise ValueError(
            "direction width must match the activation hidden dimension: "
            f"{direction.shape[0]} != {activations.shape[-1]}"
        )
    if not direction.is_floating_point():
        raise TypeError("direction must be floating point")
    if not torch.isfinite(direction).all():
        raise ValueError("direction must contain only finite values")

    converted = direction.detach().to(device=activations.device, dtype=torch.float32)
    if torch.linalg.vector_norm(converted) == 0:
        raise ValueError("direction must have nonzero norm")
    return converted


def jlens_token_direction(
    jacobian: torch.Tensor,
    unembedding_row: torch.Tensor,
) -> torch.Tensor:
    """Construct a layer-space direction for one vocabulary token.

    Args:
        jacobian: Averaged J-Lens Jacobian ``J_l`` with shape
            ``[d_model, d_model]``. It maps a layer-``l`` residual change into
            the corresponding first-order change in the final residual stream.
        unembedding_row: The language-model head row ``w_t`` for the target
            token, shaped ``[d_model]``.

    Returns:
        Float32 vector ``v_t = J_l.T @ w_t`` in layer-``l`` space.

    This orientation is important: for any small layer perturbation ``delta``,
    ``dot(v_t, delta)`` equals the corresponding linearized target-logit change
    ``dot(w_t, J_l @ delta)``.
    """

    if jacobian.ndim != 2 or jacobian.shape[0] != jacobian.shape[1]:
        raise ValueError("jacobian must be square with shape [d_model, d_model]")
    if not jacobian.is_floating_point():
        raise TypeError("jacobian must be floating point")
    if not torch.isfinite(jacobian).all():
        raise ValueError("jacobian must contain only finite values")

    width = jacobian.shape[0]
    if unembedding_row.ndim != 1 or unembedding_row.shape[0] != width:
        raise ValueError("unembedding_row must have shape [d_model]")
    if not unembedding_row.is_floating_point():
        raise TypeError("unembedding_row must be floating point")
    if not torch.isfinite(unembedding_row).all():
        raise ValueError("unembedding_row must contain only finite values")

    work_jacobian = jacobian.detach().to(dtype=torch.float32)
    work_unembedding_row = unembedding_row.detach().to(
        device=work_jacobian.device,
        dtype=torch.float32,
    )
    direction = work_jacobian.T @ work_unembedding_row
    if torch.linalg.vector_norm(direction) == 0:
        raise ValueError("the requested J-Lens token direction is zero")
    return direction


def steer_along_direction(
    activations: torch.Tensor,
    direction: torch.Tensor,
    *,
    coefficient: float,
) -> torch.Tensor:
    """Add a J-Lens direction to one or more activation vectors.

    Args:
        activations: Tensor shaped ``[..., d_model]``. A runner can pass one
            token vector or a complete activation matrix.
        direction: Layer-space direction shaped ``[d_model]``.
        coefficient: Signed steering amount ``alpha``.

    Returns:
        A new tensor with ``alpha * direction`` added to every supplied vector.
        The original tensor is not modified, and dtype/device are preserved.

    The direction is deliberately not unit-normalized: this implements the
    paper's edit ``h <- h + alpha v_t`` literally. Consequently, coefficients
    are meaningful only for directions built using the same convention.
    """

    if not math.isfinite(coefficient):
        raise ValueError("coefficient must be finite")
    work_direction = _validate_direction_for(activations, direction)
    edited = activations.float() + float(coefficient) * work_direction
    return edited.to(dtype=activations.dtype)


def ablate_direction(
    activations: torch.Tensor,
    direction: torch.Tensor,
    *,
    strength: float = 1.0,
) -> torch.Tensor:
    """Remove some or all of an activation's component along a direction.

    Args:
        activations: Tensor shaped ``[..., d_model]``.
        direction: Direction shaped ``[d_model]``; it need not be normalized.
        strength: Fraction of the parallel component to remove. ``0`` leaves
            the activation unchanged and ``1`` performs full projection-out.

    Returns:
        A new tensor computed as
        ``h - strength * dot(h, v) / dot(v, v) * v`` along the final dimension.
        The original tensor is not modified, and dtype/device are preserved.

    This is the paper's projection-out form of ablation. It is invariant to
    rescaling ``direction``, unlike negative additive steering.
    """

    if not math.isfinite(strength) or not 0.0 <= strength <= 1.0:
        raise ValueError("strength must be finite and lie in [0, 1]")
    work_direction = _validate_direction_for(activations, direction)
    work_activations = activations.float()
    denominator = torch.dot(work_direction, work_direction)
    coordinates = (work_activations * work_direction).sum(
        dim=-1,
        keepdim=True,
    ) / denominator
    edited = work_activations - float(strength) * coordinates * work_direction
    return edited.to(dtype=activations.dtype)


def swap_direction_coordinates(
    activations: torch.Tensor,
    source_direction: torch.Tensor,
    target_direction: torch.Tensor,
    *,
    scale: float = 1.0,
) -> torch.Tensor:
    """Swap source and target coordinates in their two-direction subspace.

    Args:
        activations: Floating tensor shaped ``[..., d_model]``.
        source_direction: J-Lens vector ``v_s`` for the source concept.
        target_direction: J-Lens vector ``v_t`` for the target concept.
        scale: Multiplier on the swap update. ``1`` performs the paper's full
            coordinate swap and ``0`` leaves the activation unchanged.

    Returns:
        A new tensor implementing
        ``h + scale * V @ (swap(V_pinv @ h) - V_pinv @ h)``, where
        ``V = [v_s, v_t]``. The component orthogonal to both directions is
        unchanged, and the original activation is not modified.
    """

    if not math.isfinite(scale):
        raise ValueError("swap scale must be finite")
    source = _validate_direction_for(activations, source_direction)
    target = _validate_direction_for(activations, target_direction)
    direction_matrix = torch.stack((source, target), dim=1)
    if int(torch.linalg.matrix_rank(direction_matrix).item()) < 2:
        raise ValueError("source and target directions must be linearly independent")

    work_activations = activations.float()
    pseudoinverse = torch.linalg.pinv(direction_matrix)
    coordinates = work_activations @ pseudoinverse.T
    swapped_coordinates = coordinates.flip(dims=(-1,))
    update = (swapped_coordinates - coordinates) @ direction_matrix.T
    edited = work_activations + float(scale) * update
    return edited.to(dtype=activations.dtype)


def _normalize_token_positions(
    token_positions: Sequence[int] | None,
    *,
    sequence_length: int,
) -> tuple[int, ...]:
    """Resolve token positions against the current activation sequence.

    ``None`` means every token position. Negative positions use normal Python
    indexing, so ``-1`` means the final token. Duplicate positions are removed
    while preserving their first occurrence.
    """

    if sequence_length <= 0:
        raise ValueError("activation sequence must contain at least one token")
    if token_positions is None:
        return tuple(range(sequence_length))
    if not token_positions:
        raise ValueError("token_positions must not be empty")

    normalized: list[int] = []
    seen: set[int] = set()
    for position in token_positions:
        if isinstance(position, bool) or not isinstance(position, int):
            raise TypeError("every token position must be an integer")
        resolved = position if position >= 0 else sequence_length + position
        if not 0 <= resolved < sequence_length:
            raise IndexError(
                f"token position {position} is outside a sequence of length "
                f"{sequence_length}"
            )
        if resolved not in seen:
            normalized.append(resolved)
            seen.add(resolved)
    return tuple(normalized)


def intervene_on_token_positions(
    hidden_states: torch.Tensor,
    direction: torch.Tensor,
    *,
    token_positions: Sequence[int] | None,
    kind: InterventionKind,
    coefficient: float | None = None,
    strength: float | None = None,
    target_direction: torch.Tensor | None = None,
    swap_scale: float | None = None,
) -> torch.Tensor:
    """Apply one intervention to selected rows of a hidden-state matrix.

    Args:
        hidden_states: Residual stream shaped ``[batch, sequence, d_model]``.
        direction: J-Lens direction shaped ``[d_model]`` for this layer.
        token_positions: Sequence positions to edit for every batch item.
            ``None`` edits every position.
        kind: ``"steer"``, ``"ablate"``, or ``"swap"``.
        coefficient: Required only for steering; this is ``alpha`` in
            ``h <- h + alpha * v_t``.
        strength: Optional only for ablation; defaults to full projection-out
            when omitted.
        target_direction: Required only for swapping. ``direction`` is treated
            as the source direction and this is the replacement direction.
        swap_scale: Optional only for swapping; defaults to a full swap.

    Returns:
        A cloned hidden-state tensor with only the selected token rows edited.
        The input tensor is never modified in place.
    """

    if hidden_states.ndim != 3:
        raise ValueError(
            "hidden_states must have shape [batch, sequence, d_model]"
        )
    positions = _normalize_token_positions(
        token_positions,
        sequence_length=hidden_states.shape[1],
    )

    if kind == "steer":
        if coefficient is None:
            raise ValueError("steering requires coefficient")
        if strength is not None or target_direction is not None or swap_scale is not None:
            raise ValueError("steering accepts only coefficient")
        edit = lambda selected: steer_along_direction(
            selected,
            direction,
            coefficient=coefficient,
        )
    elif kind == "ablate":
        if coefficient is not None or target_direction is not None or swap_scale is not None:
            raise ValueError("ablation accepts only strength")
        edit = lambda selected: ablate_direction(
            selected,
            direction,
            strength=1.0 if strength is None else strength,
        )
    elif kind == "swap":
        if coefficient is not None or strength is not None:
            raise ValueError("coordinate swapping does not accept coefficient or strength")
        if target_direction is None:
            raise ValueError("coordinate swapping requires target_direction")
        edit = lambda selected: swap_direction_coordinates(
            selected,
            direction,
            target_direction,
            scale=1.0 if swap_scale is None else swap_scale,
        )
    else:
        raise ValueError(f"unsupported intervention kind: {kind!r}")

    edited_hidden_states = hidden_states.clone()
    selected = hidden_states[:, positions, :]
    edited_hidden_states[:, positions, :] = edit(selected)
    return edited_hidden_states


def _replace_hidden_states(output: object, hidden_states: torch.Tensor) -> object:
    """Replace the hidden-state tensor while preserving a block's output type."""

    if torch.is_tensor(output):
        return hidden_states
    if isinstance(output, tuple) and output and torch.is_tensor(output[0]):
        return (hidden_states, *output[1:])
    if isinstance(output, list) and output and torch.is_tensor(output[0]):
        return [hidden_states, *output[1:]]
    raise TypeError(
        "layer output must be a tensor or a nonempty tuple/list whose first "
        "element is the hidden-state tensor"
    )


class LayerIntervention:
    """Temporarily intervene on one transformer block's residual output.

    The context manager registers a forward hook on ``blocks[layer_index]``.
    Every forward pass made inside the context edits the requested token rows;
    leaving the context removes the hook, including when an exception occurs.

    This class deliberately accepts the already-constructed layer direction.
    Loading the correct Jacobian and selecting an unembedding row are runner
    responsibilities and therefore remain independently testable.
    """

    def __init__(
        self,
        blocks: Sequence[nn.Module],
        *,
        layer_index: int,
        token_positions: Sequence[int] | None,
        direction: torch.Tensor,
        kind: InterventionKind,
        coefficient: float | None = None,
        strength: float | None = None,
        target_direction: torch.Tensor | None = None,
        swap_scale: float | None = None,
    ) -> None:
        if isinstance(layer_index, bool) or not isinstance(layer_index, int):
            raise TypeError("layer_index must be an integer")
        if not 0 <= layer_index < len(blocks):
            raise IndexError(
                f"layer_index {layer_index} is outside {len(blocks)} blocks"
            )
        if token_positions is not None:
            token_positions = tuple(token_positions)

        # Validate the operation-specific scalar arguments immediately rather
        # than waiting until a potentially expensive model forward pass.
        probe = torch.zeros(1, 1, direction.shape[-1], dtype=torch.float32)
        intervene_on_token_positions(
            probe,
            direction,
            token_positions=(0,),
            kind=kind,
            coefficient=coefficient,
            strength=strength,
            target_direction=target_direction,
            swap_scale=swap_scale,
        )

        self._block = blocks[layer_index]
        self.layer_index = layer_index
        self.token_positions = token_positions
        self.direction = direction.detach().clone()
        self.kind = kind
        self.coefficient = coefficient
        self.strength = strength
        self.target_direction = (
            None if target_direction is None else target_direction.detach().clone()
        )
        self.swap_scale = swap_scale
        self._handle: torch.utils.hooks.RemovableHandle | None = None

    def _hook(self, module: nn.Module, inputs: object, output: object) -> object:
        hidden_states = output if torch.is_tensor(output) else output[0]
        edited = intervene_on_token_positions(
            hidden_states,
            self.direction,
            token_positions=self.token_positions,
            kind=self.kind,
            coefficient=self.coefficient,
            strength=self.strength,
            target_direction=self.target_direction,
            swap_scale=self.swap_scale,
        )
        return _replace_hidden_states(output, edited)

    def __enter__(self) -> LayerIntervention:
        if self._handle is not None:
            raise RuntimeError("this LayerIntervention is already active")
        self._handle = self._block.register_forward_hook(self._hook)
        return self

    def __exit__(self, *exc: object) -> None:
        if self._handle is not None:
            self._handle.remove()
            self._handle = None
