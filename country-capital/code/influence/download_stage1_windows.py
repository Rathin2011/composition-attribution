"""Download and inspect one sampled OLMo 3 stage-one token window."""

from __future__ import annotations

import argparse
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import re
import time
from typing import Any
from urllib.request import Request, urlopen

import numpy as np

from sample_stage1_windows import DEFAULT_HESSIAN_OUTPUT, DEFAULT_RANKING_OUTPUT
from stage1_data import ANALYSIS_WINDOW_LENGTH, TOKEN_BYTES


CONTENT_RANGE_PATTERN = re.compile(r"bytes (\d+)-(\d+)/(\d+|\*)")
EXPECTED_WINDOW_BYTES = ANALYSIS_WINDOW_LENGTH * TOKEN_BYTES
COUNTRY_CAPITAL_DIR = Path(__file__).resolve().parents[2]
INFLUENCE_RESULTS_DIR = COUNTRY_CAPITAL_DIR / "results" / "influence"
DEFAULT_MAX_WORKERS = 32
DEFAULT_RETRIES = 3
DEFAULT_PROGRESS_INTERVAL = 500


@dataclass(frozen=True)
class CohortConfig:
    """Fixed input and output contract for one sampled cohort."""

    name: str
    samples_path: Path
    expected_count: int
    tokens_path: Path
    summary_path: Path


COHORTS = {
    "hessian": CohortConfig(
        name="hessian",
        samples_path=DEFAULT_HESSIAN_OUTPUT,
        expected_count=10_000,
        tokens_path=INFLUENCE_RESULTS_DIR / "hessian_tokens.npy",
        summary_path=INFLUENCE_RESULTS_DIR / "hessian_download_summary.json",
    ),
    "ranking": CohortConfig(
        name="ranking",
        samples_path=DEFAULT_RANKING_OUTPUT,
        expected_count=100_000,
        tokens_path=INFLUENCE_RESULTS_DIR / "ranking_tokens.npy",
        summary_path=INFLUENCE_RESULTS_DIR / "ranking_download_summary.json",
    ),
}


def load_first_window(path: str | Path) -> dict[str, object]:
    """Read and validate the first sampled-window record from a JSONL file."""

    input_path = Path(path)
    with input_path.open(encoding="utf-8") as file_handle:
        first_line = file_handle.readline()
    if not first_line:
        raise ValueError(f"sample file is empty: {input_path}")

    record = json.loads(first_line)
    required_fields = {"url", "source", "manifest_index", "byte_start", "byte_end"}
    missing = required_fields - record.keys()
    if missing:
        raise ValueError(f"sample record is missing fields: {sorted(missing)}")

    byte_start = record["byte_start"]
    byte_end = record["byte_end"]
    if not isinstance(byte_start, int) or not isinstance(byte_end, int):
        raise ValueError("sample byte offsets must be integers")
    if byte_end - byte_start != EXPECTED_WINDOW_BYTES:
        raise ValueError(
            f"sample byte range must contain {EXPECTED_WINDOW_BYTES} bytes"
        )
    return record


def fetch_byte_range(
    url: str,
    byte_start: int,
    byte_end: int,
    *,
    timeout: float = 60.0,
    opener: Callable[..., Any] = urlopen,
) -> bytes:
    """Download one exclusive-end byte range and verify the HTTP response."""

    if byte_start < 0 or byte_end <= byte_start:
        raise ValueError("invalid byte range")
    inclusive_end = byte_end - 1
    request = Request(
        url,
        headers={
            "Range": f"bytes={byte_start}-{inclusive_end}",
            "User-Agent": "olmo3-influence-reproduction/1.0",
        },
    )

    with opener(request, timeout=timeout) as response:
        status = getattr(response, "status", response.getcode())
        content_range = response.headers.get("Content-Range")
        raw_bytes = response.read()

    if status != 206:
        raise ValueError(
            f"server returned HTTP {status}, not partial-content status 206"
        )
    if content_range is None:
        raise ValueError("partial response is missing Content-Range")
    match = CONTENT_RANGE_PATTERN.fullmatch(content_range.strip())
    if match is None:
        raise ValueError(f"invalid Content-Range header: {content_range!r}")
    returned_start, returned_end = (int(value) for value in match.group(1, 2))
    if returned_start != byte_start or returned_end != inclusive_end:
        raise ValueError(
            "server returned the wrong byte range: "
            f"expected {byte_start}-{inclusive_end}, "
            f"got {returned_start}-{returned_end}"
        )
    if len(raw_bytes) != byte_end - byte_start:
        raise ValueError(
            f"server returned {len(raw_bytes)} bytes; expected {byte_end - byte_start}"
        )
    return raw_bytes


def bytes_to_token_ids(raw_bytes: bytes) -> np.ndarray:
    """Decode little-endian uint32 bytes into an independent token-ID array."""

    if len(raw_bytes) != EXPECTED_WINDOW_BYTES:
        raise ValueError(
            f"token window has {len(raw_bytes)} bytes; expected {EXPECTED_WINDOW_BYTES}"
        )
    token_ids = np.frombuffer(raw_bytes, dtype="<u4").copy()
    if token_ids.shape != (ANALYSIS_WINDOW_LENGTH,):
        raise ValueError(f"decoded token array has unexpected shape {token_ids.shape}")
    return token_ids


def inspect_first_download(
    samples_path: str | Path = DEFAULT_HESSIAN_OUTPUT,
    *,
    timeout: float = 60.0,
    range_fetcher: Callable[..., bytes] = fetch_byte_range,
) -> np.ndarray:
    """Download one sampled window and print enough information to inspect it."""

    record = load_first_window(samples_path)
    byte_start = int(record["byte_start"])
    byte_end = int(record["byte_end"])
    print(f"Source: {record['source']}")
    print(f"Shard index: {record['manifest_index']}")
    print(f"Shard URL: {record['url']}")
    print(f"Requesting bytes: [{byte_start}, {byte_end})")

    raw_bytes = range_fetcher(
        str(record["url"]),
        byte_start,
        byte_end,
        timeout=timeout,
    )
    token_ids = bytes_to_token_ids(raw_bytes)
    print(f"Bytes received: {len(raw_bytes):,}")
    print(f"Token IDs received: {len(token_ids):,}")
    print(f"First 20 token IDs: {token_ids[:20].tolist()}")
    return token_ids


def load_cohort_records(config: CohortConfig) -> list[dict[str, object]]:
    """Load and fail closed on a cohort's order, count, and byte ranges."""

    records: list[dict[str, object]] = []
    seen_window_ids: set[int] = set()
    with config.samples_path.open(encoding="utf-8") as file_handle:
        for line_number, line in enumerate(file_handle, start=1):
            record = json.loads(line)
            sample_index = record.get("sample_index")
            if sample_index != len(records):
                raise ValueError(
                    f"line {line_number} has sample_index {sample_index}; "
                    f"expected {len(records)}"
                )
            if record.get("cohort") != config.name:
                raise ValueError(
                    f"line {line_number} belongs to cohort {record.get('cohort')!r}, "
                    f"not {config.name!r}"
                )
            validated = load_first_window_from_record(record, line_number=line_number)
            global_window_id = validated.get("global_window_id")
            if not isinstance(global_window_id, int):
                raise ValueError(f"line {line_number} has an invalid global_window_id")
            if global_window_id in seen_window_ids:
                raise ValueError(f"line {line_number} duplicates a global window ID")
            seen_window_ids.add(global_window_id)
            records.append(validated)

    if len(records) != config.expected_count:
        raise ValueError(
            f"{config.name} cohort contains {len(records):,} records; "
            f"expected {config.expected_count:,}"
        )
    return records


def load_first_window_from_record(
    record: dict[str, object], *, line_number: int | None = None
) -> dict[str, object]:
    """Validate fields shared by single-window and bulk downloads."""

    location = f"line {line_number}" if line_number is not None else "sample record"
    required_fields = {"url", "source", "manifest_index", "byte_start", "byte_end"}
    missing = required_fields - record.keys()
    if missing:
        raise ValueError(f"{location} is missing fields: {sorted(missing)}")
    byte_start = record["byte_start"]
    byte_end = record["byte_end"]
    if not isinstance(byte_start, int) or not isinstance(byte_end, int):
        raise ValueError(f"{location} byte offsets must be integers")
    if byte_end - byte_start != EXPECTED_WINDOW_BYTES:
        raise ValueError(
            f"{location} byte range must contain {EXPECTED_WINDOW_BYTES} bytes"
        )
    return record


def fetch_window_with_retries(
    record: dict[str, object],
    *,
    timeout: float,
    attempts: int,
    range_fetcher: Callable[..., bytes] = fetch_byte_range,
    sleeper: Callable[[float], None] = time.sleep,
) -> np.ndarray:
    """Download and decode one record, retrying transient network failures."""

    if attempts <= 0:
        raise ValueError("attempts must be positive")
    for attempt in range(1, attempts + 1):
        try:
            raw_bytes = range_fetcher(
                str(record["url"]),
                int(record["byte_start"]),
                int(record["byte_end"]),
                timeout=timeout,
            )
            return bytes_to_token_ids(raw_bytes)
        except (OSError, TimeoutError):
            if attempt == attempts:
                raise
            sleeper(float(attempt))
    raise AssertionError("retry loop terminated unexpectedly")


def progress_paths(tokens_path: Path) -> tuple[Path, Path]:
    """Return cohort-specific partial-token and completion-bitmap paths."""

    partial_tokens = tokens_path.with_name(
        f".{tokens_path.stem}.partial{tokens_path.suffix}"
    )
    completion_bitmap = tokens_path.with_name(
        f".{tokens_path.stem}.done{tokens_path.suffix}"
    )
    return partial_tokens, completion_bitmap


def open_progress_arrays(
    config: CohortConfig,
) -> tuple[np.memmap, np.memmap, bool]:
    """Create or reopen a cohort's resumable token array and completion bitmap."""

    config.tokens_path.parent.mkdir(parents=True, exist_ok=True)
    partial_tokens, completion_bitmap = progress_paths(config.tokens_path)
    if config.tokens_path.exists():
        raise FileExistsError(
            f"completed output already exists for {config.name}: {config.tokens_path}"
        )
    if partial_tokens.exists() != completion_bitmap.exists():
        raise ValueError(
            f"incomplete resume state for {config.name}; expected both partial files"
        )

    resumed = partial_tokens.exists()
    if resumed:
        tokens = np.load(partial_tokens, mmap_mode="r+")
        done = np.load(completion_bitmap, mmap_mode="r+")
    else:
        tokens = np.lib.format.open_memmap(
            partial_tokens,
            mode="w+",
            dtype="<u4",
            shape=(config.expected_count, ANALYSIS_WINDOW_LENGTH),
        )
        done = np.lib.format.open_memmap(
            completion_bitmap,
            mode="w+",
            dtype=np.bool_,
            shape=(config.expected_count,),
        )
        done[:] = False
        done.flush()

    expected_shape = (config.expected_count, ANALYSIS_WINDOW_LENGTH)
    if tokens.shape != expected_shape or tokens.dtype != np.dtype("<u4"):
        raise ValueError(
            f"invalid partial token array for {config.name}: "
            f"shape={tokens.shape}, dtype={tokens.dtype}"
        )
    if done.shape != (config.expected_count,) or done.dtype != np.dtype(np.bool_):
        raise ValueError(
            f"invalid completion bitmap for {config.name}: "
            f"shape={done.shape}, dtype={done.dtype}"
        )
    return tokens, done, resumed


def sha256_file(path: Path) -> str:
    """Hash a file without loading it all into memory."""

    digest = sha256()
    with path.open("rb") as file_handle:
        while block := file_handle.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def save_summary(payload: dict[str, object], path: Path) -> None:
    """Atomically save one cohort's download summary."""

    temporary_path = path.with_name(f".{path.name}.tmp")
    temporary_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary_path.replace(path)


def download_cohort(
    config: CohortConfig,
    *,
    timeout: float = 60.0,
    max_workers: int = DEFAULT_MAX_WORKERS,
    retries: int = DEFAULT_RETRIES,
    progress_interval: int = DEFAULT_PROGRESS_INTERVAL,
    range_fetcher: Callable[..., bytes] = fetch_byte_range,
) -> dict[str, object]:
    """Download one complete cohort into a resumable, ordered uint32 array."""

    if max_workers <= 0:
        raise ValueError("max_workers must be positive")
    if progress_interval <= 0:
        raise ValueError("progress_interval must be positive")

    records = load_cohort_records(config)
    tokens, done, resumed = open_progress_arrays(config)
    initial_completed = int(np.count_nonzero(done))
    print(
        f"{'Resuming' if resumed else 'Starting'} {config.name} download: "
        f"{initial_completed:,}/{config.expected_count:,} already complete"
    )
    pending_indices = np.flatnonzero(~done).tolist()
    batch_size = max_workers * 4
    completed = initial_completed

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for batch_start in range(0, len(pending_indices), batch_size):
            batch_indices = pending_indices[batch_start : batch_start + batch_size]
            futures: dict[Future[np.ndarray], int] = {
                executor.submit(
                    fetch_window_with_retries,
                    records[index],
                    timeout=timeout,
                    attempts=retries,
                    range_fetcher=range_fetcher,
                ): index
                for index in batch_indices
            }
            try:
                for future in as_completed(futures):
                    index = futures[future]
                    tokens[index] = future.result()
                    done[index] = True
                    completed += 1
                    if completed % progress_interval == 0 or completed == config.expected_count:
                        print(
                            f"Downloaded {completed:,}/{config.expected_count:,} "
                            f"{config.name} windows"
                        )
            finally:
                tokens.flush()
                done.flush()

    if not bool(np.all(done)):
        raise RuntimeError(f"{config.name} download ended with incomplete rows")
    tokens.flush()
    done.flush()
    partial_tokens, completion_bitmap = progress_paths(config.tokens_path)
    del tokens
    del done
    partial_tokens.replace(config.tokens_path)
    completion_bitmap.unlink()

    completed_tokens = np.load(config.tokens_path, mmap_mode="r")
    if completed_tokens.shape != (
        config.expected_count,
        ANALYSIS_WINDOW_LENGTH,
    ) or completed_tokens.dtype != np.dtype("<u4"):
        raise ValueError("completed token array failed shape or dtype validation")
    print(f"First 20 token IDs from row 0: {completed_tokens[0, :20].tolist()}")
    print(f"First 20 token IDs from final row: {completed_tokens[-1, :20].tolist()}")
    del completed_tokens

    summary: dict[str, object] = {
        "schema_version": 1,
        "cohort": config.name,
        "samples_path": str(config.samples_path.resolve()),
        "samples_sha256": sha256_file(config.samples_path),
        "tokens_path": str(config.tokens_path.resolve()),
        "tokens_sha256": sha256_file(config.tokens_path),
        "shape": [config.expected_count, ANALYSIS_WINDOW_LENGTH],
        "dtype": "uint32-little-endian",
        "records": config.expected_count,
        "bytes_per_window": EXPECTED_WINDOW_BYTES,
        "resumed": resumed,
    }
    save_summary(summary, config.summary_path)
    print(f"Saved tokens: {config.tokens_path}")
    print(f"Saved summary: {config.summary_path}")
    return summary


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download one selected stage-one window cohort."
    )
    parser.add_argument("--cohort", choices=sorted(COHORTS), required=True)
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--max-workers", type=int, default=DEFAULT_MAX_WORKERS)
    parser.add_argument("--retries", type=int, default=DEFAULT_RETRIES)
    parser.add_argument(
        "--first-only",
        action="store_true",
        help="Download and print only the first selected window.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    config = COHORTS[args.cohort]
    if args.first_only:
        inspect_first_download(config.samples_path, timeout=args.timeout)
    else:
        download_cohort(
            config,
            timeout=args.timeout,
            max_workers=args.max_workers,
            retries=args.retries,
        )


if __name__ == "__main__":
    main()
