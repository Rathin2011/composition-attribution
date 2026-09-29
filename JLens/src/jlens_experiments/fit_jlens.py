"""Fit an OLMo 3 stage-one Jacobian lens from a fixed prompt manifest.

The Jacobian calculation, averaging, checkpointing, and serialization are
delegated unchanged to the authors' ``jlens.fit`` implementation. This runner
validates and selects one non-overlapping manifest shard, loads the pinned
OLMo 3 checkpoint and official adapter, fits the requested source layers, and
saves the lens plus provenance.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Sequence

from .compatibility import (
    JLENS_COMMIT,
    MODEL_COMMIT,
    MODEL_ID,
    MODEL_REVISION,
    VENDORED_JLENS,
    package_version,
    validate_adapter,
)
from .manifest import persist_prompt_records, read_prompt_records, select_prompt_shard


DEFAULT_LAYERS = (12, 16, 18, 20, 22, 24)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt-manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--num-shards", type=int, default=1)
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--max-seq-len", type=int, default=128)
    parser.add_argument("--layers", type=int, nargs="+", default=DEFAULT_LAYERS)
    parser.add_argument("--target-layer", type=int, default=31)
    parser.add_argument("--dim-batch", type=int, default=8)
    parser.add_argument("--checkpoint-every", type=int, default=10)
    parser.add_argument(
        "--allow-download",
        action="store_true",
        help="Allow Hugging Face downloads instead of requiring cached files.",
    )
    return parser.parse_args()


def validate_fit_settings(
    *, source_layers: Sequence[int], target_layer: int, dim_batch: int
) -> list[int]:
    """Validate settings before loading the 7B model."""

    layers = sorted(set(source_layers))
    if not layers:
        raise ValueError("at least one source layer is required")
    if layers[0] < 0 or layers[-1] >= target_layer:
        raise ValueError("source layers must be non-negative and below target_layer")
    if target_layer != 31:
        raise ValueError("the OLMo 3 target layer must be 31")
    if dim_batch < 1:
        raise ValueError("dim_batch must be positive")
    return layers


def _import_runtime() -> tuple[Any, Any, Any, Any]:
    """Import the official J-Lens package and model dependencies lazily."""

    if not (VENDORED_JLENS / "jlens" / "__init__.py").is_file():
        raise FileNotFoundError(f"missing official J-Lens checkout: {VENDORED_JLENS}")
    sys.path.insert(0, str(VENDORED_JLENS))
    import jlens
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    return jlens, torch, AutoModelForCausalLM, AutoTokenizer


def run(args: argparse.Namespace) -> dict[str, Any]:
    """Fit one fixed-manifest shard and save its lens and provenance."""

    layers = validate_fit_settings(
        source_layers=args.layers,
        target_layer=args.target_layer,
        dim_batch=args.dim_batch,
    )
    if args.max_seq_len < 18:
        raise ValueError("max_seq_len must be at least 18")
    if args.checkpoint_every < 1:
        raise ValueError("checkpoint_every must be positive")

    output_dir = args.output_dir
    lens_path = output_dir / "jacobian_lens.pt"
    checkpoint_path = output_dir / "fit_checkpoint.pt"
    prompts_path = output_dir / "prompts.jsonl"
    summary_path = output_dir / "summary.json"
    if lens_path.exists() or summary_path.exists():
        raise FileExistsError("completed fitting output already exists")

    all_prompt_records = read_prompt_records(args.prompt_manifest)
    prompt_records = select_prompt_shard(
        all_prompt_records,
        num_shards=args.num_shards,
        shard_index=args.shard_index,
    )
    persist_prompt_records(prompts_path, prompt_records)
    prompts = [record["text"] for record in prompt_records]

    jlens, torch, model_class, tokenizer_class = _import_runtime()
    jlens.configure_logging()
    tokenizer = tokenizer_class.from_pretrained(
        MODEL_ID,
        revision=MODEL_COMMIT,
        local_files_only=not args.allow_download,
    )
    model = model_class.from_pretrained(
        MODEL_ID,
        revision=MODEL_COMMIT,
        dtype=torch.bfloat16,
        device_map="auto",
        local_files_only=not args.allow_download,
    )
    adapter = jlens.from_hf(model, tokenizer, compile=False)
    adapter_report = validate_adapter(adapter)

    lens = jlens.fit(
        adapter,
        prompts=prompts,
        source_layers=layers,
        target_layer=args.target_layer,
        dim_batch=args.dim_batch,
        max_seq_len=args.max_seq_len,
        checkpoint_path=str(checkpoint_path),
        checkpoint_every=args.checkpoint_every,
        resume=True,
    )
    lens.save(str(lens_path))

    summary = {
        "status": "complete",
        "model": MODEL_ID,
        "stage_one_revision": MODEL_REVISION,
        "model_commit": MODEL_COMMIT,
        "jlens_commit": JLENS_COMMIT,
        "versions": {
            "python": sys.version.split()[0],
            "torch": package_version("torch"),
            "transformers": package_version("transformers"),
        },
        "input": {
            "mode": "fixed_manifest",
            "prompt_manifest": str(args.prompt_manifest),
            "manifest_prompts": len(all_prompt_records),
            "num_shards": args.num_shards,
            "shard_index": args.shard_index,
            "selected_sample_indices": [
                record["sample_index"] for record in prompt_records
            ],
        },
        "fit": {
            "requested_prompts": len(prompt_records),
            "successful_prompts": lens.n_prompts,
            "source_layers": lens.source_layers,
            "target_layer": args.target_layer,
            "hidden_size": lens.d_model,
            "prompt_tokens": len(prompt_records[0]["token_ids"]),
            "max_seq_len": args.max_seq_len,
            "dim_batch": args.dim_batch,
            "checkpoint_every": args.checkpoint_every,
        },
        "adapter": adapter_report,
        "outputs": {
            "lens": str(lens_path),
            "checkpoint": str(checkpoint_path),
            "prompts": str(prompts_path),
        },
    }
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return summary


def main() -> None:
    run(parse_args())


if __name__ == "__main__":
    main()
