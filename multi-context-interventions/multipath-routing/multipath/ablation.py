"""Pure tensor operations for Stage-04 subspace ablation.

No model loading, hooks, or file I/O. A subspace is given by row directions
``[k, d_model]``; it is orthonormalised once and then removed from a residual
vector either by zeroing its component (zero ablation) or by replacing that
component with the component of a reference mean (mean ablation).
"""
from __future__ import annotations

from collections.abc import Sequence
import zlib

import torch


ABLATION_TYPES = ("zero", "mean")


def orthonormal_basis(directions: torch.Tensor, *, tolerance: float = 1e-6) -> torch.Tensor:
    """Return ``Q`` with orthonormal columns spanning the given row directions.

    ``directions`` is ``[k, d_model]``. Rows that are (numerically) linearly
    dependent on earlier rows are dropped, so ``Q`` is ``[d_model, rank]``.
    """

    if directions.ndim != 2 or directions.shape[0] == 0 or not directions.is_floating_point():
        raise ValueError("directions must be a non-empty floating [k, d_model] tensor")
    if not torch.isfinite(directions).all():
        raise ValueError("directions must be finite")
    u, s, _ = torch.linalg.svd(directions.float().T, full_matrices=False)
    keep = s > tolerance * s.max()
    if not bool(keep.any()):
        raise ValueError("directions span a zero subspace")
    return u[:, keep]


def ablate(hidden: torch.Tensor, basis: torch.Tensor, mean: torch.Tensor | None) -> torch.Tensor:
    """Remove the ``basis`` component of ``hidden`` ([d_model]).

    Zero ablation (``mean is None``): ``h - Q Q^T h``.
    Mean ablation: ``h - Q Q^T (h - mean)``; the subspace component becomes the
    mean's component and everything orthogonal to the subspace is unchanged.
    """

    if hidden.ndim != 1 or basis.ndim != 2 or basis.shape[0] != hidden.shape[0]:
        raise ValueError("hidden must be [d_model] and basis [d_model, rank]")
    work = hidden.float()
    q = basis.to(device=work.device, dtype=torch.float32)
    delta = work if mean is None else work - mean.to(device=work.device, dtype=torch.float32)
    return (work - q @ (q.T @ delta)).to(hidden.dtype)


def projection_fraction(direction: torch.Tensor, basis: torch.Tensor) -> float:
    """Norm of a unit direction's projection onto ``span(basis)`` (0 = orthogonal, 1 = inside)."""

    unit = direction.float() / direction.float().norm()
    return float((basis.float().T @ unit).norm().item())


def matched_random_tokens(
    reference_ids: Sequence[int],
    candidate_mask: torch.Tensor,
    *,
    excluded: set[int],
    window: int,
    seed_key: str,
) -> list[int]:
    """Draw one random candidate token near each reference token ID.

    BPE IDs are roughly ordered by merge frequency, so a token within ``window``
    IDs of the reference serves as a frequency-matched control. Draws are
    deterministic in ``seed_key`` and never repeat or hit ``excluded``.
    """

    if window <= 0 or candidate_mask.ndim != 1:
        raise ValueError("window must be positive and candidate_mask one-dimensional")
    generator = torch.Generator().manual_seed(zlib.crc32(seed_key.encode("utf-8")))
    chosen: list[int] = []
    size = candidate_mask.shape[0]
    for reference in reference_ids:
        low, high = max(0, int(reference) - window), min(size, int(reference) + window + 1)
        pool = [i for i in torch.nonzero(candidate_mask[low:high]).flatten().add(low).tolist()
                if i not in excluded and i not in chosen]
        if not pool:
            raise ValueError(f"no matched random candidate near token {reference}")
        chosen.append(pool[int(torch.randint(len(pool), (1,), generator=generator).item())])
    return chosen
