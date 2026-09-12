"""Uniformly select disjoint 512-token windows from the stage-one inventory.

This module records shard locations and byte ranges only. It does not download
the selected token contents.
"""

from __future__ import annotations

import argparse
from bisect import bisect_right
from collections.abc import Iterable, Sequence
import json
from pathlib import Path
import random
import sys

from stage1_data import (
    ANALYSIS_WINDOW_LENGTH,
    MANIFEST_SHA256,
    TOKEN_BYTES,
    TRAIN_SEQUENCE_LENGTH,
    WINDOWS_PER_TRAIN_SEQUENCE,
)


COUNTRY_CAPITAL_DIR = Path(__file__).resolve().parents[2]
INFLUENCE_RESULTS_DIR = COUNTRY_CAPITAL_DIR / "results" / "influence"
DEFAULT_INVENTORY = INFLUENCE_RESULTS_DIR / "stage1_inventory.json"
DEFAULT_HESSIAN_OUTPUT = INFLUENCE_RESULTS_DIR / "hessian_windows.jsonl"
DEFAULT_RANKING_OUTPUT = INFLUENCE_RESULTS_DIR / "ranking_windows.jsonl"
DEFAULT_SUMMARY_OUTPUT = INFLUENCE_RESULTS_DIR / "sampling_summary.json"

DEFAULT_HESSIAN_COUNT = 10_000
DEFAULT_RANKING_COUNT = 100_000
DEFAULT_SEED = 0
DEFAULT_PREVIEW_COUNT = 5


def load_and_validate_inventory(path: str | Path) -> dict[str, object]:
    """Load the inventory and check all offsets needed by the sampler."""

    inventory_path = Path(path)
    payload = json.loads(inventory_path.read_text(encoding="utf-8"))
    if payload.get("manifest_sha256") != MANIFEST_SHA256:
        raise ValueError("inventory manifest hash does not match the pinned manifest")
    if payload.get("token_bytes") != TOKEN_BYTES:
        raise ValueError("inventory token width does not match the stage-one recipe")
    if payload.get("train_sequence_length") != TRAIN_SEQUENCE_LENGTH:
        raise ValueError("inventory sequence length does not match the stage-one recipe")

    shards = payload.get("shards")
    if not isinstance(shards, list) or not shards:
        raise ValueError("inventory contains no shards")
    if payload.get("total_shards") != len(shards):
        raise ValueError("inventory total_shards does not match its shard records")

    expected_start = 0
    for index, shard in enumerate(shards):
        if not isinstance(shard, dict):
            raise ValueError(f"inventory shard {index} is not an object")
        if shard.get("manifest_index") != index:
            raise ValueError(f"inventory shard {index} has the wrong manifest index")
        if shard.get("sequence_start") != expected_start:
            raise ValueError(f"inventory shard {index} has a non-contiguous start offset")
        sequence_end = shard.get("sequence_end")
        complete_sequences = shard.get("complete_train_sequences")
        if not isinstance(sequence_end, int) or not isinstance(complete_sequences, int):
            raise ValueError(f"inventory shard {index} has invalid sequence counts")
        if sequence_end - expected_start != complete_sequences:
            raise ValueError(f"inventory shard {index} has inconsistent sequence offsets")
        expected_start = sequence_end

    if payload.get("total_complete_train_sequences") != expected_start:
        raise ValueError("inventory total sequence count does not match its final offset")
    return payload


def select_disjoint_window_ids(
    total_windows: int,
    hessian_count: int,
    ranking_count: int,
    *,
    seed: int,
) -> tuple[list[int], list[int]]:
    """Select both cohorts uniformly without replacement using one RNG draw."""

    if total_windows <= 0:
        raise ValueError("total_windows must be positive")
    if hessian_count < 0 or ranking_count < 0:
        raise ValueError("sample counts cannot be negative")
    requested = hessian_count + ranking_count
    if requested > total_windows:
        raise ValueError("requested more unique windows than the inventory contains")

    selected = random.Random(seed).sample(range(total_windows), requested)
    return selected[:hessian_count], selected[hessian_count:]


def map_window_ids(
    window_ids: Iterable[int],
    shards: Sequence[dict[str, object]],
    *,
    cohort: str,
) -> list[dict[str, object]]:
    """Map global window IDs to exact shard token and byte ranges."""

    sequence_ends = [int(shard["sequence_end"]) for shard in shards]
    total_sequences = sequence_ends[-1]
    total_windows = total_sequences * WINDOWS_PER_TRAIN_SEQUENCE
    records: list[dict[str, object]] = []

    for sample_index, global_window_id in enumerate(window_ids):
        if not 0 <= global_window_id < total_windows:
            raise ValueError(f"window ID {global_window_id} is outside the inventory")

        global_sequence_index, window_slot = divmod(
            global_window_id, WINDOWS_PER_TRAIN_SEQUENCE
        )
        shard_index = bisect_right(sequence_ends, global_sequence_index)
        shard = shards[shard_index]
        local_sequence_index = global_sequence_index - int(shard["sequence_start"])
        token_start = (
            local_sequence_index * TRAIN_SEQUENCE_LENGTH
            + window_slot * ANALYSIS_WINDOW_LENGTH
        )
        token_end = token_start + ANALYSIS_WINDOW_LENGTH

        records.append(
            {
                "cohort": cohort,
                "sample_index": sample_index,
                "global_window_id": global_window_id,
                "global_sequence_index": global_sequence_index,
                "window_slot": window_slot,
                "manifest_index": shard_index,
                "source": shard["source"],
                "relative_path": shard["relative_path"],
                "url": shard["url"],
                "local_sequence_index": local_sequence_index,
                "token_start": token_start,
                "token_end": token_end,
                "byte_start": token_start * TOKEN_BYTES,
                "byte_end": token_end * TOKEN_BYTES,
            }
        )
    return records


def write_jsonl(records: Iterable[dict[str, object]], output: str | Path) -> Path:
    """Atomically write records as one JSON object per line."""

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_name(f".{output_path.name}.tmp")
    with temporary_path.open("w", encoding="utf-8") as file_handle:
        for record in records:
            file_handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    temporary_path.replace(output_path)
    return output_path


def write_json(payload: dict[str, object], output: str | Path) -> Path:
    """Atomically write a human-readable JSON object."""

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_name(f".{output_path.name}.tmp")
    temporary_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary_path.replace(output_path)
    return output_path


def print_sample_preview(
    cohort: str,
    records: Sequence[dict[str, object]],
    *,
    limit: int,
) -> None:
    """Print a concise mapping preview for manual inspection."""

    if limit < 0:
        raise ValueError("preview limit cannot be negative")
    shown = min(limit, len(records))
    print(f"{cohort.capitalize()} preview ({shown} windows):")
    for record in records[:shown]:
        print(
            f"  sample={record['sample_index']} "
            f"window={record['global_window_id']} "
            f"source={record['source']} "
            f"shard={record['manifest_index']} "
            f"sequence={record['global_sequence_index']} "
            f"local_sequence={record['local_sequence_index']} "
            f"slot={record['window_slot']} "
            f"tokens=[{record['token_start']},{record['token_end']}) "
            f"bytes=[{record['byte_start']},{record['byte_end']})"
        )


def sample_windows(
    inventory_path: str | Path = DEFAULT_INVENTORY,
    *,
    hessian_count: int = DEFAULT_HESSIAN_COUNT,
    ranking_count: int = DEFAULT_RANKING_COUNT,
    seed: int = DEFAULT_SEED,
    hessian_output: str | Path = DEFAULT_HESSIAN_OUTPUT,
    ranking_output: str | Path = DEFAULT_RANKING_OUTPUT,
    summary_output: str | Path = DEFAULT_SUMMARY_OUTPUT,
    preview_count: int = DEFAULT_PREVIEW_COUNT,
) -> dict[str, object]:
    """Select, validate, map, and save the two pilot cohorts."""

    inventory = load_and_validate_inventory(inventory_path)
    shards = inventory["shards"]
    total_sequences = int(inventory["total_complete_train_sequences"])
    total_windows = total_sequences * WINDOWS_PER_TRAIN_SEQUENCE
    print(f"Available aligned 512-token windows: {total_windows:,}")
    print(
        f"Selecting {hessian_count:,} Hessian and {ranking_count:,} ranking "
        f"windows with seed {seed}"
    )

    hessian_ids, ranking_ids = select_disjoint_window_ids(
        total_windows,
        hessian_count,
        ranking_count,
        seed=seed,
    )
    hessian_id_set = set(hessian_ids)
    ranking_id_set = set(ranking_ids)
    overlap_count = len(hessian_id_set & ranking_id_set)
    if len(hessian_id_set) != hessian_count:
        raise AssertionError("Hessian sample contains duplicate window IDs")
    if len(ranking_id_set) != ranking_count:
        raise AssertionError("ranking sample contains duplicate window IDs")
    if overlap_count:
        raise AssertionError("Hessian and ranking samples overlap")

    print(f"Unique Hessian windows: {len(hessian_id_set):,}/{hessian_count:,}")
    print(f"Unique ranking windows: {len(ranking_id_set):,}/{ranking_count:,}")
    print(f"Overlap between cohorts: {overlap_count}")
    if hessian_ids:
        print(f"Hessian global-window range: {min(hessian_ids):,}–{max(hessian_ids):,}")
    if ranking_ids:
        print(f"Ranking global-window range: {min(ranking_ids):,}–{max(ranking_ids):,}")

    hessian_records = map_window_ids(hessian_ids, shards, cohort="hessian")
    ranking_records = map_window_ids(ranking_ids, shards, cohort="ranking")
    print_sample_preview("hessian", hessian_records, limit=preview_count)
    print_sample_preview("ranking", ranking_records, limit=preview_count)
    hessian_path = write_jsonl(hessian_records, hessian_output)
    ranking_path = write_jsonl(ranking_records, ranking_output)

    summary: dict[str, object] = {
        "schema_version": 1,
        "inventory_path": str(Path(inventory_path).resolve()),
        "manifest_sha256": MANIFEST_SHA256,
        "sampling_algorithm": "python random.Random.sample over range",
        "python_version": sys.version.split()[0],
        "seed": seed,
        "train_sequence_length": TRAIN_SEQUENCE_LENGTH,
        "window_length": ANALYSIS_WINDOW_LENGTH,
        "windows_per_train_sequence": WINDOWS_PER_TRAIN_SEQUENCE,
        "total_complete_train_sequences": total_sequences,
        "total_candidate_windows": total_windows,
        "hessian_count": len(hessian_records),
        "ranking_count": len(ranking_records),
        "hessian_unique_count": len(hessian_id_set),
        "ranking_unique_count": len(ranking_id_set),
        "overlap_count": overlap_count,
        "sets_are_disjoint": True,
        "hessian_output": str(hessian_path.resolve()),
        "ranking_output": str(ranking_path.resolve()),
    }
    summary_path = write_json(summary, summary_output)
    print(f"Saved Hessian selections: {hessian_path}")
    print(f"Saved ranking selections: {ranking_path}")
    print(f"Saved sampling summary: {summary_path}")
    return summary


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sample disjoint Hessian and ranking windows from stage one."
    )
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--hessian-count", type=int, default=DEFAULT_HESSIAN_COUNT)
    parser.add_argument("--ranking-count", type=int, default=DEFAULT_RANKING_COUNT)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--hessian-output", type=Path, default=DEFAULT_HESSIAN_OUTPUT)
    parser.add_argument("--ranking-output", type=Path, default=DEFAULT_RANKING_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--preview-count", type=int, default=DEFAULT_PREVIEW_COUNT)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    sample_windows(
        args.inventory,
        hessian_count=args.hessian_count,
        ranking_count=args.ranking_count,
        seed=args.seed,
        hessian_output=args.hessian_output,
        ranking_output=args.ranking_output,
        summary_output=args.summary_output,
        preview_count=args.preview_count,
    )


if __name__ == "__main__":
    main()
