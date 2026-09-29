"""Check whether the official Jacobian Lens adapter supports OLMo 3 stage one.

This is deliberately a compatibility smoke test, not a lens-fitting job. It:

1. loads the immutable OLMo 3 stage-one checkpoint in bfloat16;
2. wraps it with the authors' unmodified ``jlens.from_hf`` adapter;
3. verifies the expected 32-layer, 4096-dimensional residual-stream layout;
4. compares one normal Hugging Face forward pass with the adapter's
   residual-to-unembedding path; and
5. writes a small JSON report.

No Jacobian matrices or task-query results are produced by this module.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import json
from pathlib import Path
import sys
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
VENDORED_JLENS = PROJECT_ROOT / "vendor" / "jacobian-lens"
DEFAULT_REPORT = PROJECT_ROOT / "results" / "compatibility" / "olmo3_stage1.json"

MODEL_ID = "allenai/Olmo-3-1025-7B"
MODEL_REVISION = "stage1-step1413814"
MODEL_COMMIT = "373bad25002f1624757a73235c5ca844c6375c25"
JLENS_COMMIT = "581d398613e5602a5af361e1c34d3a92ea82ba8e"
EXPECTED_LAYERS = 32
EXPECTED_HIDDEN_SIZE = 4096
DEFAULT_PROMPT = "The capital of France is"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument(
        "--allow-download",
        action="store_true",
        help="Allow Hugging Face downloads instead of requiring cached files.",
    )
    return parser.parse_args()


def package_version(name: str) -> str:
    """Return an installed distribution version or ``not-installed``."""
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return "not-installed"


def validate_adapter(adapter: Any) -> dict[str, Any]:
    """Validate the model-independent structural contract needed by J-lens."""
    if adapter.n_layers != EXPECTED_LAYERS:
        raise ValueError(
            f"expected {EXPECTED_LAYERS} layers, found {adapter.n_layers}"
        )
    if adapter.d_model != EXPECTED_HIDDEN_SIZE:
        raise ValueError(
            f"expected hidden size {EXPECTED_HIDDEN_SIZE}, found {adapter.d_model}"
        )
    if len(adapter.layers) != EXPECTED_LAYERS:
        raise ValueError(
            f"adapter exposes {len(adapter.layers)} blocks, expected {EXPECTED_LAYERS}"
        )
    return {
        "adapter_type": type(adapter).__name__,
        "layout": {
            "path": adapter.layout.path,
            "layers": adapter.layout.layers,
            "norm": adapter.layout.norm,
            "embed": adapter.layout.embed,
            "lm_head": adapter.layout.lm_head,
        },
        "num_layers": adapter.n_layers,
        "hidden_size": adapter.d_model,
        "input_device": str(adapter.input_device),
    }


def compare_logits(hf_logits: Any, adapter_logits: Any) -> dict[str, Any]:
    """Confirm that the adapter's norm/unembedding reproduces HF logits."""
    import torch

    if hf_logits.shape != adapter_logits.shape:
        raise ValueError(
            f"logit shape mismatch: HF={hf_logits.shape}, adapter={adapter_logits.shape}"
        )
    hf_float = hf_logits.float()
    adapter_float = adapter_logits.to(hf_logits.device).float()
    difference = (hf_float - adapter_float).abs()
    matches = torch.allclose(hf_float, adapter_float, rtol=1e-3, atol=1e-3)
    same_top_token = bool(
        torch.equal(hf_float[:, -1].argmax(-1), adapter_float[:, -1].argmax(-1))
    )
    if not matches or not same_top_token:
        raise ValueError(
            "the J-lens residual-to-logit path does not reproduce Hugging Face logits"
        )
    return {
        "shape": list(hf_logits.shape),
        "max_absolute_difference": float(difference.max().item()),
        "mean_absolute_difference": float(difference.mean().item()),
        "allclose_rtol": 1e-3,
        "allclose_atol": 1e-3,
        "same_final_top_token": same_top_token,
    }


def _import_runtime() -> tuple[Any, Any, Any, Any]:
    """Import the vendored authors' package and model dependencies lazily."""
    if not (VENDORED_JLENS / "jlens" / "__init__.py").is_file():
        raise FileNotFoundError(
            f"official J-lens checkout is missing from {VENDORED_JLENS}"
        )
    sys.path.insert(0, str(VENDORED_JLENS))
    import jlens
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    return jlens, torch, AutoModelForCausalLM, AutoTokenizer


def run_smoke_test(
    *, prompt: str, report_path: Path, local_files_only: bool
) -> dict[str, Any]:
    """Run the real checkpoint compatibility test and save its JSON report."""
    jlens, torch, model_class, tokenizer_class = _import_runtime()

    tokenizer = tokenizer_class.from_pretrained(
        MODEL_ID,
        revision=MODEL_COMMIT,
        local_files_only=local_files_only,
    )
    model = model_class.from_pretrained(
        MODEL_ID,
        revision=MODEL_COMMIT,
        dtype=torch.bfloat16,
        device_map="auto",
        local_files_only=local_files_only,
    )
    adapter = jlens.from_hf(model, tokenizer, compile=False)
    adapter_report = validate_adapter(adapter)

    input_ids = adapter.encode(prompt, max_length=128)
    with torch.inference_mode():
        hf_logits = model(input_ids=input_ids, use_cache=False).logits
        # J-lens reads a block's residual output and then applies the model's
        # final norm and unembedding.  The bare HF model's last_hidden_state is
        # already final-normalized, so using it here would normalize twice.
        final_block = adapter.n_layers - 1
        with jlens.ActivationRecorder(adapter.layers, at=[final_block]) as recorder:
            adapter.forward(input_ids)
        residual = recorder.activations[final_block]
        adapter_logits = adapter.unembed(residual)
    logit_report = compare_logits(hf_logits, adapter_logits)

    final_token_id = int(hf_logits[0, -1].argmax().item())
    report = {
        "status": "compatible",
        "model": MODEL_ID,
        "stage_one_revision": MODEL_REVISION,
        "model_commit": MODEL_COMMIT,
        "dtype": "bfloat16",
        "jlens_commit": JLENS_COMMIT,
        "versions": {
            "python": sys.version.split()[0],
            "torch": package_version("torch"),
            "transformers": package_version("transformers"),
            "accelerate": package_version("accelerate"),
        },
        "prompt": prompt,
        "num_prompt_tokens": int(input_ids.shape[1]),
        "bos_token_id": tokenizer.bos_token_id,
        "first_input_token_id": int(input_ids[0, 0].item()),
        "final_top_token_id": final_token_id,
        "final_top_token": tokenizer.decode([final_token_id]),
        "adapter": adapter_report,
        "logit_comparison": logit_report,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return report


def main() -> None:
    args = parse_args()
    run_smoke_test(
        prompt=args.prompt,
        report_path=args.report,
        local_files_only=not args.allow_download,
    )


if __name__ == "__main__":
    main()
