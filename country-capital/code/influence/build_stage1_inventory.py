"""Build a size-and-offset inventory for the OLMo 3 stage-one shards.

Only HTTP metadata are requested. This module never downloads token contents.
"""

from __future__ import annotations

import argparse
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from collections.abc import Callable, Sequence
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import time
from typing import Any
from urllib.request import Request, urlopen

from stage1_data import (
    GLOBAL_BATCH_SEQUENCES,
    MANIFEST_FILENAME,
    MANIFEST_SHA256,
    STAGE_ONE_STEP,
    TOKEN_BYTES,
    TRAIN_SEQUENCE_LENGTH,
    ManifestEntry,
    load_official_manifest,
)


COUNTRY_CAPITAL_DIR = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = COUNTRY_CAPITAL_DIR / "results" / "influence" / MANIFEST_FILENAME
DEFAULT_OUTPUT = COUNTRY_CAPITAL_DIR / "results" / "influence" / "stage1_inventory.json"
DEFAULT_MAX_WORKERS = 16
DEFAULT_RETRIES = 3


@dataclass(frozen=True)
class ShardInspection:
    """Size information derived for one tokenized shard."""

    source: str
    relative_path: str
    url: str
    byte_size: int
    token_count: int
    complete_train_sequences: int
    trailing_tokens: int


def get_remote_file_size(
    url: str,
    timeout: float = 60.0,
    *,
    opener: Callable[..., Any] = urlopen,
) -> int:
    """Return a remote shard's byte size using an HTTP HEAD request."""

    request = Request(
        url,
        method="HEAD",
        headers={"User-Agent": "olmo3-influence-reproduction/1.0"},
    )
    with opener(request, timeout=timeout) as response:
        content_length = response.headers.get("Content-Length")

    if content_length is None:
        raise ValueError(f"server did not provide Content-Length for {url}")
    try:
        byte_size = int(content_length)
    except ValueError as error:
        raise ValueError(f"invalid Content-Length {content_length!r} for {url}") from error
    if byte_size <= 0:
        raise ValueError(f"non-positive Content-Length {byte_size} for {url}")
    return byte_size


def summarize_shard(entry: ManifestEntry, byte_size: int) -> ShardInspection:
    """Convert a shard's byte size into OLMo training-sequence counts."""

    if byte_size <= 0:
        raise ValueError("shard byte size must be positive")
    if byte_size % TOKEN_BYTES != 0:
        raise ValueError(
            f"shard byte size {byte_size} is not divisible by {TOKEN_BYTES} bytes/token"
        )

    token_count = byte_size // TOKEN_BYTES
    complete_sequences, trailing_tokens = divmod(token_count, TRAIN_SEQUENCE_LENGTH)
    return ShardInspection(
        source=entry.source,
        relative_path=entry.relative_path,
        url=entry.url,
        byte_size=byte_size,
        token_count=token_count,
        complete_train_sequences=complete_sequences,
        trailing_tokens=trailing_tokens,
    )


def inspect_first_shard(
    manifest_path: str | Path = DEFAULT_MANIFEST,
    *,
    timeout: float = 60.0,
    size_getter: Callable[[str, float], int] = get_remote_file_size,
) -> ShardInspection:
    """Load the verified manifest and inspect only its first shard."""

    entries = load_official_manifest(manifest_path)
    first_entry = entries[0]
    print(f"Inspecting first shard: {first_entry.url}")

    byte_size = size_getter(first_entry.url, timeout)
    inspection = summarize_shard(first_entry, byte_size)
    print(f"Source: {inspection.source}")
    print(f"Bytes: {inspection.byte_size:,}")
    print(f"Tokens: {inspection.token_count:,}")
    print(f"Complete 8,192-token sequences: {inspection.complete_train_sequences:,}")
    print(f"Trailing tokens ignored by OLMo: {inspection.trailing_tokens:,}")
    return inspection


def get_file_size_with_retries(
    url: str,
    timeout: float,
    attempts: int,
    *,
    size_getter: Callable[[str, float], int] = get_remote_file_size,
    sleeper: Callable[[float], None] = time.sleep,
) -> int:
    """Retry transient network failures while retrieving one shard size."""

    if attempts <= 0:
        raise ValueError("attempts must be positive")

    for attempt in range(1, attempts + 1):
        try:
            return size_getter(url, timeout)
        except (OSError, TimeoutError):
            if attempt == attempts:
                raise
            sleeper(float(attempt))
    raise AssertionError("retry loop terminated unexpectedly")


def inspect_all_shards(
    entries: Sequence[ManifestEntry],
    *,
    timeout: float,
    max_workers: int,
    retries: int,
    size_getter: Callable[[str, float], int] = get_remote_file_size,
    verbose: bool = True,
) -> list[ShardInspection]:
    """Inspect all shards concurrently while preserving manifest order."""

    if not entries:
        raise ValueError("cannot inspect an empty manifest")
    if max_workers <= 0:
        raise ValueError("max_workers must be positive")

    inspections: list[ShardInspection | None] = [None] * len(entries)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures: dict[Future[int], int] = {
            executor.submit(
                get_file_size_with_retries,
                entry.url,
                timeout,
                retries,
                size_getter=size_getter,
            ): index
            for index, entry in enumerate(entries)
        }

        for completed, future in enumerate(as_completed(futures), start=1):
            index = futures[future]
            inspections[index] = summarize_shard(entries[index], future.result())
            if verbose and (completed == 1 or completed % 25 == 0 or completed == len(entries)):
                print(f"Inspected {completed:,}/{len(entries):,} shards")

    if any(inspection is None for inspection in inspections):
        raise RuntimeError("one or more shard inspections are missing")
    return [inspection for inspection in inspections if inspection is not None]


def build_inventory_payload(
    inspections: Sequence[ShardInspection],
    *,
    expected_stage_one_steps: int = STAGE_ONE_STEP,
) -> dict[str, object]:
    """Add global offsets and validate the complete stage-one dataset size."""

    shards: list[dict[str, object]] = []
    next_sequence_offset = 0
    total_tokens = 0
    total_trailing_tokens = 0

    for manifest_index, inspection in enumerate(inspections):
        sequence_start = next_sequence_offset
        sequence_end = sequence_start + inspection.complete_train_sequences
        shard = {
            "manifest_index": manifest_index,
            **asdict(inspection),
            "sequence_start": sequence_start,
            "sequence_end": sequence_end,
        }
        shards.append(shard)
        next_sequence_offset = sequence_end
        total_tokens += inspection.token_count
        total_trailing_tokens += inspection.trailing_tokens

    complete_batches, final_batch_remainder = divmod(
        next_sequence_offset, GLOBAL_BATCH_SEQUENCES
    )
    if complete_batches != expected_stage_one_steps:
        raise ValueError(
            "inventory does not match the stage-one checkpoint: "
            f"expected {expected_stage_one_steps:,} complete batches, "
            f"found {complete_batches:,}"
        )

    return {
        "schema_version": 1,
        "manifest_sha256": MANIFEST_SHA256,
        "token_bytes": TOKEN_BYTES,
        "train_sequence_length": TRAIN_SEQUENCE_LENGTH,
        "global_batch_sequences": GLOBAL_BATCH_SEQUENCES,
        "stage_one_step": expected_stage_one_steps,
        "stage_one_instances_seen": expected_stage_one_steps
        * GLOBAL_BATCH_SEQUENCES,
        "total_shards": len(shards),
        "total_tokens_in_shards": total_tokens,
        "total_complete_train_sequences": next_sequence_offset,
        "total_trailing_tokens_ignored_within_shards": total_trailing_tokens,
        "final_incomplete_batch_sequences": final_batch_remainder,
        "shards": shards,
    }


def save_inventory(payload: dict[str, object], output: str | Path) -> Path:
    """Atomically save a deterministic, human-readable JSON inventory."""

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_name(f".{output_path.name}.tmp")
    temporary_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary_path.replace(output_path)
    return output_path


def build_inventory(
    manifest_path: str | Path = DEFAULT_MANIFEST,
    output: str | Path = DEFAULT_OUTPUT,
    *,
    timeout: float = 60.0,
    max_workers: int = DEFAULT_MAX_WORKERS,
    retries: int = DEFAULT_RETRIES,
) -> dict[str, object]:
    """Inspect every manifest shard, validate totals, and save the inventory."""

    entries = load_official_manifest(manifest_path)
    print(f"Loaded verified manifest with {len(entries):,} shards")
    inspections = inspect_all_shards(
        entries,
        timeout=timeout,
        max_workers=max_workers,
        retries=retries,
    )
    payload = build_inventory_payload(inspections)
    output_path = save_inventory(payload, output)
    print(
        "Complete 8,192-token sequences: "
        f"{payload['total_complete_train_sequences']:,}"
    )
    print(f"Complete training batches: {payload['stage_one_step']:,}")
    print(
        "Sequences omitted from the final incomplete batch: "
        f"{payload['final_incomplete_batch_sequences']:,}"
    )
    print(f"Saved inventory: {output_path}")
    return payload


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the stage-one shard inventory.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--max-workers", type=int, default=DEFAULT_MAX_WORKERS)
    parser.add_argument("--retries", type=int, default=DEFAULT_RETRIES)
    parser.add_argument(
        "--first-only",
        action="store_true",
        help="Inspect the first shard without creating an inventory.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    if args.first_only:
        inspect_first_shard(args.manifest, timeout=args.timeout)
    else:
        build_inventory(
            args.manifest,
            args.output,
            timeout=args.timeout,
            max_workers=args.max_workers,
            retries=args.retries,
        )


if __name__ == "__main__":
    main()
