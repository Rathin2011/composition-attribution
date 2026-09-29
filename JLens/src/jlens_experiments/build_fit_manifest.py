"""Build the fixed 1,000-prompt manifest for distributed J-Lens fitting.

This CPU-only program deterministically selects unique rows from the already
downloaded uniform OLMo 3 stage-one token-window sample, decodes the first 128
tokens with the pinned tokenizer, and records both token IDs and provenance.
It does not load the language model or calculate Jacobians.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from .compatibility import MODEL_COMMIT, MODEL_ID, MODEL_REVISION
from .manifest import (
    DEFAULT_TOKEN_WINDOWS,
    DEFAULT_WINDOW_METADATA,
    prepare_prompt_records,
    persist_prompt_records,
    read_metadata,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = PROJECT_ROOT / "results" / "fit_1000" / "prompt_manifest.jsonl"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--token-windows", type=Path, default=DEFAULT_TOKEN_WINDOWS)
    parser.add_argument("--window-metadata", type=Path, default=DEFAULT_WINDOW_METADATA)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--num-prompts", type=int, default=1000)
    parser.add_argument("--prompt-tokens", type=int, default=128)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--allow-download",
        action="store_true",
        help="Allow a tokenizer download instead of requiring cached files.",
    )
    return parser.parse_args()


def run(args: argparse.Namespace) -> dict:
    """Create the immutable prompt JSONL and a checksum-bearing summary."""
    if args.num_prompts < 1 or args.prompt_tokens < 1:
        raise ValueError("prompt counts and lengths must be positive")
    summary_path = args.output.with_name("prompt_manifest_summary.json")
    if args.output.exists() or summary_path.exists():
        raise FileExistsError("fit manifest output already exists")

    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID,
        revision=MODEL_COMMIT,
        local_files_only=not args.allow_download,
    )
    token_windows = np.load(args.token_windows, mmap_mode="r")
    metadata = read_metadata(args.window_metadata)
    records = prepare_prompt_records(
        token_windows,
        metadata,
        tokenizer,
        num_prompts=args.num_prompts,
        prompt_tokens=args.prompt_tokens,
        seed=args.seed,
    )
    persist_prompt_records(args.output, records)
    digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
    summary = {
        "status": "complete",
        "model": MODEL_ID,
        "stage_one_revision": MODEL_REVISION,
        "model_commit": MODEL_COMMIT,
        "token_windows": str(args.token_windows),
        "window_metadata": str(args.window_metadata),
        "available_windows": int(token_windows.shape[0]),
        "stored_tokens_per_window": int(token_windows.shape[1]),
        "num_prompts": len(records),
        "prompt_tokens": args.prompt_tokens,
        "seed": args.seed,
        "unique_sample_indices": len({record["sample_index"] for record in records}),
        "manifest": str(args.output),
        "manifest_sha256": digest,
    }
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return summary


def main() -> None:
    run(parse_args())


if __name__ == "__main__":
    main()
