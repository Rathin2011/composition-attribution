"""Load and validate the pinned OLMo 3 stage-one checkpoint."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import torch

from .config import MODEL_COMMIT, MODEL_ID, MODEL_LAYERS


def resolve_cached_snapshot(cache_dir: Path) -> Path:
    """Resolve the pinned checkpoint locally without downloading anything."""
    from huggingface_hub import snapshot_download

    snapshot = Path(
        snapshot_download(
            MODEL_ID,
            revision=MODEL_COMMIT,
            cache_dir=cache_dir,
            local_files_only=True,
        )
    )
    if snapshot.name != MODEL_COMMIT:
        raise ValueError("cached snapshot is not the pinned stage-one commit")
    return snapshot


def validate_model(model: Any) -> None:
    """Reject a model that is not the expected 32-layer OLMo 3 architecture."""
    if model.config.model_type != "olmo3":
        raise ValueError("expected an OLMo 3 model")
    if len(model.model.layers) != MODEL_LAYERS:
        raise ValueError(f"expected {MODEL_LAYERS} decoder layers")


def load_model_and_tokenizer(cache_dir: Path) -> tuple[Any, Any]:
    """Load the pinned checkpoint offline in BF16 and switch it to eval mode."""
    from transformers import AutoModelForCausalLM, AutoTokenizer

    snapshot = resolve_cached_snapshot(cache_dir)
    tokenizer = AutoTokenizer.from_pretrained(snapshot, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        snapshot,
        local_files_only=True,
        device_map="auto",
        dtype=torch.bfloat16,
    )
    model.eval()
    validate_model(model)
    return model, tokenizer
