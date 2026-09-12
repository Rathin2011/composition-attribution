"""Download and verify the pinned OLMo 3 stage-one data manifest."""

from __future__ import annotations

import argparse
from collections.abc import Callable, Sequence
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen

from stage1_data import (
    EXPECTED_SHARD_COUNT,
    MANIFEST_FILENAME,
    MANIFEST_SHA256,
    MANIFEST_URL,
    parse_manifest_text,
)


COUNTRY_CAPITAL_DIR = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = COUNTRY_CAPITAL_DIR / "results" / "influence" / MANIFEST_FILENAME


def fetch_bytes(url: str, timeout: float) -> bytes:
    """Fetch one URL without modifying the response bytes."""

    request = Request(url, headers={"User-Agent": "olmo3-influence-reproduction/1.0"})
    with urlopen(request, timeout=timeout) as response:
        return response.read()


def verify_manifest_bytes(
    raw_bytes: bytes,
    *,
    expected_sha256: str = MANIFEST_SHA256,
    expected_shard_count: int = EXPECTED_SHARD_COUNT,
) -> int:
    """Verify the manifest's exact hash, encoding, syntax, and shard count."""

    actual_sha256 = sha256(raw_bytes).hexdigest()
    if actual_sha256 != expected_sha256:
        raise ValueError(
            f"manifest SHA-256 mismatch: expected {expected_sha256}, "
            f"got {actual_sha256}"
        )

    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("manifest is not valid UTF-8") from error

    entries = parse_manifest_text(text)
    if len(entries) != expected_shard_count:
        raise ValueError(
            f"manifest shard-count mismatch: expected {expected_shard_count}, "
            f"got {len(entries)}"
        )
    return len(entries)


def download_manifest(
    output: str | Path = DEFAULT_OUTPUT,
    *,
    timeout: float = 60.0,
    verbose: bool = True,
    fetcher: Callable[[str, float], bytes] = fetch_bytes,
    expected_sha256: str = MANIFEST_SHA256,
    expected_shard_count: int = EXPECTED_SHARD_COUNT,
) -> Path:
    """Download, validate, and atomically save the official manifest."""

    output_path = Path(output)
    if verbose:
        print(f"Downloading manifest: {MANIFEST_URL}")

    raw_bytes = fetcher(MANIFEST_URL, timeout)
    shard_count = verify_manifest_bytes(
        raw_bytes,
        expected_sha256=expected_sha256,
        expected_shard_count=expected_shard_count,
    )
    if verbose:
        print(f"Verified SHA-256: {expected_sha256}")
        print(f"Verified shard count: {shard_count:,}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_name(f".{output_path.name}.tmp")
    temporary_path.write_bytes(raw_bytes)
    temporary_path.replace(output_path)

    if verbose:
        print(f"Saved manifest: {output_path}")
    return output_path


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download and verify the official OLMo 3 stage-one manifest."
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--quiet", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    download_manifest(args.output, timeout=args.timeout, verbose=not args.quiet)


if __name__ == "__main__":
    main()
