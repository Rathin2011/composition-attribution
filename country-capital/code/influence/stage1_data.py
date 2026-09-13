"""Pinned OLMo 3 stage-one data specification.

This module defines and validates the training-data manifest. It intentionally
does not download shards or sample token windows; those are later blocks.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path


# OLMo-core release containing the official OLMo-3-1025-7B training scripts.
OLMO_CORE_COMMIT = "600d2fe2be2b49d9d83d3bab1656508e0b33cd35"
MODEL_ID = "allenai/Olmo-3-1025-7B"
MODEL_REVISION = "stage1-step1413814"
MODEL_COMMIT = "373bad25002f1624757a73235c5ca844c6375c25"

DATA_ROOT = "https://olmo-data.org"
TOKENIZER_PLACEHOLDER = "{TOKENIZER}"
TOKENIZER_DIRECTORY = "allenai/dolma3-tokenizer"

MANIFEST_FILENAME = "OLMo-mix-0625-official.txt"
MANIFEST_URL = (
    "https://raw.githubusercontent.com/allenai/OLMo-core/"
    f"{OLMO_CORE_COMMIT}/src/olmo_core/data/mixes/{MANIFEST_FILENAME}"
)
MANIFEST_SHA256 = "d770716a78fe0e9fa074c89f010574fd34ec0ee750cb79188120c62047c1a270"
EXPECTED_SHARD_COUNT = 1_016

# Values from the pinned official pretraining recipe.
TOKEN_DTYPE = "uint32"
TOKEN_BYTES = 4
TRAIN_SEQUENCE_LENGTH = 8_192
GLOBAL_BATCH_SEQUENCES = 512
LOADER_SEED = 34_521
STAGE_ONE_EPOCH = 1
STAGE_ONE_SHUFFLE_SEED = LOADER_SEED + STAGE_ONE_EPOCH
STAGE_ONE_STEP = 1_413_814
STAGE_ONE_INSTANCES_SEEN = STAGE_ONE_STEP * GLOBAL_BATCH_SEQUENCES

# Our influence-function example size. Each stage-one sequence contains exactly
# 16 non-overlapping candidate windows of this length.
ANALYSIS_WINDOW_LENGTH = 512
WINDOWS_PER_TRAIN_SEQUENCE = TRAIN_SEQUENCE_LENGTH // ANALYSIS_WINDOW_LENGTH


@dataclass(frozen=True)
class ManifestEntry:
    """One tokenized shard in AllenAI's official stage-one manifest."""

    source: str
    relative_path: str
    url: str


def validate_recipe() -> None:
    """Reject internally inconsistent constants before later sampling."""

    if TRAIN_SEQUENCE_LENGTH % ANALYSIS_WINDOW_LENGTH != 0:
        raise ValueError("analysis window must divide the training sequence length")
    if STAGE_ONE_SHUFFLE_SEED != LOADER_SEED + STAGE_ONE_EPOCH:
        raise ValueError("stage-one shuffle seed is inconsistent with OLMo-core")
    if STAGE_ONE_INSTANCES_SEEN != 723_872_768:
        raise ValueError("stage-one step and batch-size constants are inconsistent")


def manifest_digest(content: bytes) -> str:
    """Hash the exact file bytes without normalizing line endings."""

    return sha256(content).hexdigest()


def parse_manifest_text(text: str, *, data_root: str = DATA_ROOT) -> list[ManifestEntry]:
    """Parse OLMo-core's strict ``source,path`` manifest format."""

    root = data_root.rstrip("/")
    entries: list[ManifestEntry] = []
    seen_urls: set[str] = set()

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        fields = line.split(",")
        if len(fields) != 2:
            raise ValueError(
                f"manifest line {line_number} must contain exactly one comma"
            )
        source, path_template = (field.strip() for field in fields)
        if not source:
            raise ValueError(f"manifest line {line_number} has an empty source")
        if path_template.count(TOKENIZER_PLACEHOLDER) != 1:
            raise ValueError(
                f"manifest line {line_number} must contain exactly one "
                f"{TOKENIZER_PLACEHOLDER!r} placeholder"
            )

        relative_path = path_template.replace(
            TOKENIZER_PLACEHOLDER, TOKENIZER_DIRECTORY
        )
        if relative_path.startswith("/") or not relative_path.endswith(".npy"):
            raise ValueError(f"manifest line {line_number} has an invalid shard path")

        url = f"{root}/{relative_path}"
        if url in seen_urls:
            raise ValueError(f"manifest line {line_number} duplicates shard {url!r}")
        seen_urls.add(url)
        entries.append(ManifestEntry(source, relative_path, url))

    if not entries:
        raise ValueError("manifest contains no data shards")
    return entries


def load_official_manifest(path: str | Path) -> list[ManifestEntry]:
    """Load a local manifest copy and verify it against the pinned release."""

    raw_bytes = Path(path).read_bytes()
    digest = manifest_digest(raw_bytes)
    if digest != MANIFEST_SHA256:
        raise ValueError(
            f"manifest SHA-256 mismatch: expected {MANIFEST_SHA256}, got {digest}"
        )

    entries = parse_manifest_text(raw_bytes.decode("utf-8"))
    if len(entries) != EXPECTED_SHARD_COUNT:
        raise ValueError(
            f"manifest shard-count mismatch: expected {EXPECTED_SHARD_COUNT}, "
            f"got {len(entries)}"
        )
    return entries
