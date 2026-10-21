"""Write the exact result structure used by the generalized experiments.

This module does not calculate lens values or run interventions.  It receives
those calculated values and writes one task's result file with exactly these
five top-level fields::

    x, Fx, GFx, results_lenses, results_intervention

JSON has no set type, so the complete sets of possible ``x``, ``Fx``, and
``GFx`` values are represented as arrays with duplicates removed.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


TOP_LEVEL_FIELDS = (
    "x",
    "Fx",
    "GFx",
    "results_lenses",
    "results_intervention",
)

LENS_FIELDS = (
    "x",
    "Fx",
    "GFx",
    "icl_ctx",
    "llens_z",
    "jlens_z",
    "llens_rr",
    "jlens_rr",
    "llens_classification",
    "jlens_classification",
)

LENS_CLASSIFICATIONS = frozenset(
    {"compositional", "ambiguous", "shortcut_candidate"}
)

INTERVENTION_FIELDS = (
    "x",
    "Fx",
    "GFx",
    "icl_ctx",
    "intervention",
    "projection",
    "target",
    "z_max",
    "z_out_GFx",
    "z_out_Fx",
)


def _unique(values: Sequence[str], name: str) -> list[str]:
    """Return strings in first-occurrence order after validating them."""

    output = []
    seen = set()
    for value in values:
        if not isinstance(value, str) or not value:
            raise ValueError(f"{name} values must be non-empty strings")
        if value not in seen:
            output.append(value)
            seen.add(value)
    if not output:
        raise ValueError(f"{name} must contain at least one value")
    return output


def _matrix_shape(value: Any, name: str) -> tuple[int, int]:
    """Validate a rectangular numeric matrix and return ``(rows, columns)``."""

    if not isinstance(value, list) or not value:
        raise ValueError(f"{name} must be a non-empty matrix")
    if not all(isinstance(row, list) and row for row in value):
        raise ValueError(f"{name} rows must be non-empty arrays")
    columns = len(value[0])
    if any(len(row) != columns for row in value):
        raise ValueError(f"{name} must be rectangular")
    if any(not isinstance(item, (int, float)) for row in value for item in row):
        raise ValueError(f"{name} must contain only numbers")
    return len(value), columns


def _validate_lens_record(record: Mapping[str, Any], n_fx: int) -> dict[str, Any]:
    """Validate one per-prompt lens record and preserve only requested fields.

    ``llens_z`` and ``jlens_z`` must contain one row for every possible ``Fx``
    value.  Their columns are layers.  Each reciprocal-rank vector must have
    one value per corresponding layer.
    """

    if tuple(record) != LENS_FIELDS:
        raise ValueError(f"lens record fields must be exactly {LENS_FIELDS}")
    llens_rows, llens_layers = _matrix_shape(record["llens_z"], "llens_z")
    jlens_rows, jlens_layers = _matrix_shape(record["jlens_z"], "jlens_z")
    if llens_rows != n_fx or jlens_rows != n_fx:
        raise ValueError(f"lens z matrices must have n_Fx={n_fx} rows")
    if len(record["llens_rr"]) != llens_layers:
        raise ValueError("llens_rr must contain one value per Logit-Lens layer")
    if len(record["jlens_rr"]) != jlens_layers:
        raise ValueError("jlens_rr must contain one value per J-Lens layer")
    for lens_name in ("llens", "jlens"):
        classification = record[f"{lens_name}_classification"]
        if classification not in LENS_CLASSIFICATIONS:
            raise ValueError(
                f"{lens_name}_classification must be one of "
                f"{sorted(LENS_CLASSIFICATIONS)}"
            )
    return dict(record)


def _validate_intervention_record(
    record: Mapping[str, Any], n_fx: int, n_gfx: int
) -> dict[str, Any]:
    """Validate one intervention record and preserve only requested fields."""

    if tuple(record) != INTERVENTION_FIELDS:
        raise ValueError(
            f"intervention record fields must be exactly {INTERVENTION_FIELDS}"
        )
    if len(record["z_out_Fx"]) != n_fx:
        raise ValueError(f"z_out_Fx must contain n_Fx={n_fx} logits")
    if len(record["z_out_GFx"]) != n_gfx:
        raise ValueError(f"z_out_GFx must contain n_GFx={n_gfx} logits")
    return dict(record)


def write_results(
    output_path: Path,
    *,
    x: Sequence[str],
    Fx: Sequence[str],
    GFx: Sequence[str],
    results_lenses: Iterable[Mapping[str, Any]],
    results_intervention: Iterable[Mapping[str, Any]],
) -> None:
    """Validate and atomically write one task's complete result file.

    Inputs:
        All possible ``x``, ``Fx``, and ``GFx`` values for one task, followed
        by its calculated lens and intervention records.
    Output:
        An uncompressed JSON file containing exactly the requested structure.
    """

    x_values = _unique(x, "x")
    fx_values = _unique(Fx, "Fx")
    gfx_values = _unique(GFx, "GFx")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.with_name(f"{output_path.name}.tmp.{os.getpid()}")
    try:
        with temporary.open("w", encoding="utf-8") as handle:
            # Stream the potentially large per-prompt arrays instead of
            # retaining every matrix in memory. Field order is the declared
            # public result contract above.
            handle.write("{\"x\":")
            json.dump(x_values, handle, ensure_ascii=False, separators=(",", ":"))
            handle.write(",\"Fx\":")
            json.dump(fx_values, handle, ensure_ascii=False, separators=(",", ":"))
            handle.write(",\"GFx\":")
            json.dump(gfx_values, handle, ensure_ascii=False, separators=(",", ":"))
            handle.write(",\"results_lenses\":[")
            for index, record in enumerate(results_lenses):
                if index:
                    handle.write(",")
                json.dump(
                    _validate_lens_record(record, len(fx_values)),
                    handle,
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
            handle.write("],\"results_intervention\":[")
            for index, record in enumerate(results_intervention):
                if index:
                    handle.write(",")
                json.dump(
                    _validate_intervention_record(
                        record, len(fx_values), len(gfx_values)
                    ),
                    handle,
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
            handle.write("]}")
            handle.write("\n")
        os.replace(temporary, output_path)
    finally:
        temporary.unlink(missing_ok=True)
