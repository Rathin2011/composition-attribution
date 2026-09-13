"""Two-block eigendecomposition used by Ruis et al. for their 7B model."""

from __future__ import annotations

from typing import Any

import torch


def block_diagonal_eigh(
    matrix: torch.Tensor, *, blocks: int = 2
) -> tuple[torch.Tensor, torch.Tensor]:
    """Discard cross-block entries and eigendecompose each diagonal block."""

    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("matrix must be square")
    if not 1 <= blocks <= matrix.shape[0]:
        raise ValueError("blocks must be between one and the matrix dimension")

    boundaries = [matrix.shape[0] * index // blocks for index in range(blocks + 1)]
    eigenvalues: list[torch.Tensor] = []
    eigenvectors: list[torch.Tensor] = []
    for start, end in zip(boundaries[:-1], boundaries[1:]):
        values, vectors = torch.linalg.eigh(matrix[start:end, start:end])
        eigenvalues.append(values.clamp_min(0))
        eigenvectors.append(vectors)
    return torch.cat(eigenvalues), torch.block_diag(*eigenvectors)


def install_two_block_eigendecomposition() -> None:
    """Replace Kronfluence's full eigendecomposition for this pinned process."""

    from tqdm import tqdm

    import kronfluence.computer.factor_computer as factor_computer
    import kronfluence.factor.eigen as eigen_module
    from kronfluence.module.utils import get_tracked_module_names
    from kronfluence.utils.constants import (
        ACTIVATION_COVARIANCE_MATRIX_NAME,
        ACTIVATION_EIGENVALUES_NAME,
        ACTIVATION_EIGENVECTORS_NAME,
        EIGENDECOMPOSITION_FACTOR_NAMES,
        GRADIENT_COVARIANCE_MATRIX_NAME,
        GRADIENT_EIGENVALUES_NAME,
        GRADIENT_EIGENVECTORS_NAME,
        NUM_ACTIVATION_COVARIANCE_PROCESSED,
        NUM_GRADIENT_COVARIANCE_PROCESSED,
    )
    from kronfluence.utils.logger import TQDM_BAR_FORMAT

    @torch.no_grad()
    def perform_eigendecomposition(
        covariance_factors: dict[str, dict[str, torch.Tensor]],
        model: torch.nn.Module,
        state: Any,
        factor_args: FactorArgumentsLike,
        disable_tqdm: bool = False,
    ) -> dict[str, dict[str, torch.Tensor]]:
        output = {name: {} for name in EIGENDECOMPOSITION_FACTOR_NAMES}
        module_names = get_tracked_module_names(model=model)
        factor_specs = (
            (
                ACTIVATION_COVARIANCE_MATRIX_NAME,
                NUM_ACTIVATION_COVARIANCE_PROCESSED,
                ACTIVATION_EIGENVECTORS_NAME,
                ACTIVATION_EIGENVALUES_NAME,
            ),
            (
                GRADIENT_COVARIANCE_MATRIX_NAME,
                NUM_GRADIENT_COVARIANCE_PROCESSED,
                GRADIENT_EIGENVECTORS_NAME,
                GRADIENT_EIGENVALUES_NAME,
            ),
        )
        with tqdm(
            total=len(module_names),
            desc="Performing two-block eigendecomposition",
            bar_format=TQDM_BAR_FORMAT,
            disable=not state.is_main_process or disable_tqdm,
        ) as progress:
            for module_name in module_names:
                for covariance_name, count_name, vectors_name, values_name in factor_specs:
                    source = covariance_factors[covariance_name][module_name]
                    original_dtype = source.dtype
                    matrix = source.to(
                        device=state.device,
                        dtype=factor_args.eigendecomposition_dtype,
                    )
                    matrix.div_(
                        covariance_factors[count_name][module_name].to(
                            device=state.device
                        )
                    )
                    matrix = (matrix + matrix.t()).mul_(0.5)
                    values, vectors = block_diagonal_eigh(matrix, blocks=2)
                    output[values_name][module_name] = values.to(
                        dtype=original_dtype, device="cpu"
                    ).contiguous()
                    output[vectors_name][module_name] = vectors.to(
                        dtype=original_dtype, device="cpu"
                    ).contiguous()
                    del matrix, values, vectors
                progress.update(1)
        return output

    eigen_module.perform_eigendecomposition = perform_eigendecomposition
    factor_computer.perform_eigendecomposition = perform_eigendecomposition


class FactorArgumentsLike:
    """Structural type used only to document the patched callback argument."""

    eigendecomposition_dtype: torch.dtype
