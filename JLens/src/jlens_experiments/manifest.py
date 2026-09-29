"""Create, persist, read, and shard immutable J-Lens prompt manifests."""

from __future__ import annotations

import json
from pathlib import Path
import random
from typing import Any, Sequence

import numpy as np


DEFAULT_TOKEN_WINDOWS = Path(
    "/projectnb/buinlp/rathin/composition-experiments/country-capital/"
    "results/influence/hessian_tokens.npy"
)
DEFAULT_WINDOW_METADATA = Path(
    "/projectnb/buinlp/rathin/composition-experiments/country-capital/"
    "results/influence/hessian_windows.jsonl"
)


def read_metadata(path: Path) -> dict[int, dict[str, Any]]:
    """Index JSONL window provenance by its unique sample index."""

    records: dict[int, dict[str, Any]] = {}
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            record = json.loads(line)
            sample_index = record.get("sample_index")
            if not isinstance(sample_index, int) or isinstance(sample_index, bool):
                raise ValueError(f"invalid sample_index on metadata line {line_number}")
            if sample_index in records:
                raise ValueError(f"duplicate metadata sample_index {sample_index}")
            records[sample_index] = record
    return records


def select_prompt_indices(
    *, num_windows: int, num_prompts: int, seed: int
) -> list[int]:
    """Select unique source windows reproducibly without replacement."""

    if num_windows < 1:
        raise ValueError("the token-window array is empty")
    if not 1 <= num_prompts <= num_windows:
        raise ValueError("num_prompts must be between 1 and num_windows")
    return random.Random(seed).sample(range(num_windows), k=num_prompts)


def prepare_prompt_records(
    token_windows: np.ndarray,
    metadata: dict[int, dict[str, Any]],
    tokenizer: Any,
    *,
    num_prompts: int,
    prompt_tokens: int,
    seed: int,
) -> list[dict[str, Any]]:
    """Select, decode, and attach provenance to fitting prompts."""

    if token_windows.ndim != 2:
        raise ValueError("token windows must have shape [windows, tokens]")
    if not 1 <= prompt_tokens <= token_windows.shape[1]:
        raise ValueError("prompt_tokens is outside the stored window length")
    if set(metadata) != set(range(token_windows.shape[0])):
        raise ValueError("metadata indices do not match the token-window rows")

    selected = select_prompt_indices(
        num_windows=token_windows.shape[0],
        num_prompts=num_prompts,
        seed=seed,
    )
    records: list[dict[str, Any]] = []
    for selection_index, sample_index in enumerate(selected):
        token_ids = token_windows[sample_index, :prompt_tokens].astype(
            np.int64, copy=False
        )
        text = tokenizer.decode(
            token_ids.tolist(),
            skip_special_tokens=False,
            clean_up_tokenization_spaces=False,
        )
        if not text.strip():
            raise ValueError(f"sample {sample_index} decoded to empty text")
        source = metadata[sample_index]
        records.append(
            {
                "selection_index": selection_index,
                "sample_index": sample_index,
                "global_window_id": source.get("global_window_id"),
                "global_sequence_index": source.get("global_sequence_index"),
                "manifest_index": source.get("manifest_index"),
                "source": source.get("source"),
                "relative_path": source.get("relative_path"),
                "source_token_count": prompt_tokens,
                "token_ids": token_ids.tolist(),
                "text": text,
            }
        )
    return records


def persist_prompt_records(path: Path, records: Sequence[dict[str, Any]]) -> None:
    """Write exact prompt inputs once, or verify an existing resume artifact."""

    contents = "".join(
        json.dumps(record, ensure_ascii=False) + "\n" for record in records
    )
    if path.exists():
        if path.read_text(encoding="utf-8") != contents:
            raise ValueError(f"existing prompt artifact differs: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")


def read_prompt_records(path: Path) -> list[dict[str, Any]]:
    """Read and validate an immutable, ordered fitting-prompt manifest."""

    records: list[dict[str, Any]] = []
    seen_samples: set[int] = set()
    first_selection_index: int | None = None
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            record = json.loads(line)
            selection_index = record.get("selection_index")
            if not isinstance(selection_index, int) or isinstance(selection_index, bool):
                raise ValueError(
                    f"invalid selection_index on manifest line {line_number}"
                )
            if first_selection_index is None:
                first_selection_index = selection_index
            if selection_index != first_selection_index + len(records):
                raise ValueError(
                    f"non-contiguous selection_index on manifest line {line_number}"
                )
            sample_index = record.get("sample_index")
            if not isinstance(sample_index, int) or isinstance(sample_index, bool):
                raise ValueError(f"invalid sample_index on manifest line {line_number}")
            if sample_index in seen_samples:
                raise ValueError(f"duplicate sample_index {sample_index} in manifest")
            token_ids = record.get("token_ids")
            if not isinstance(token_ids, list) or not token_ids or not all(
                isinstance(token_id, int) and not isinstance(token_id, bool)
                for token_id in token_ids
            ):
                raise ValueError(f"invalid token_ids on manifest line {line_number}")
            if record.get("source_token_count") != len(token_ids):
                raise ValueError(f"token count mismatch on manifest line {line_number}")
            if not isinstance(record.get("text"), str) or not record["text"].strip():
                raise ValueError(f"invalid text on manifest line {line_number}")
            seen_samples.add(sample_index)
            records.append(record)
    if not records:
        raise ValueError("prompt manifest is empty")
    return records


def select_prompt_shard(
    records: Sequence[dict[str, Any]], *, num_shards: int, shard_index: int
) -> list[dict[str, Any]]:
    """Return one equal contiguous shard from a fixed ordered manifest."""

    if num_shards < 1:
        raise ValueError("num_shards must be positive")
    if not 0 <= shard_index < num_shards:
        raise ValueError("shard_index must be between zero and num_shards - 1")
    if len(records) % num_shards:
        raise ValueError("manifest size must be divisible by num_shards")
    shard_size = len(records) // num_shards
    start = shard_index * shard_size
    return list(records[start : start + shard_size])
