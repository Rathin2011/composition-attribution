"""Download and inspect one sampled OLMo 3 stage-one token window."""

from __future__ import annotations

import argparse
from collections.abc import Callable, Sequence
import json
from pathlib import Path
import re
from typing import Any
from urllib.request import Request, urlopen

import numpy as np

from sample_stage1_windows import DEFAULT_HESSIAN_OUTPUT
from stage1_data import ANALYSIS_WINDOW_LENGTH, TOKEN_BYTES


CONTENT_RANGE_PATTERN = re.compile(r"bytes (\d+)-(\d+)/(\d+|\*)")
EXPECTED_WINDOW_BYTES = ANALYSIS_WINDOW_LENGTH * TOKEN_BYTES


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


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download and inspect the first sampled Hessian window."
    )
    parser.add_argument("--samples", type=Path, default=DEFAULT_HESSIAN_OUTPUT)
    parser.add_argument("--timeout", type=float, default=60.0)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    inspect_first_download(args.samples, timeout=args.timeout)


if __name__ == "__main__":
    main()
