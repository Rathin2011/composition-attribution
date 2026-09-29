"""Validate and merge ten disjoint OLMo 3 J-Lens fit shards.

The numerical merge is delegated unchanged to the authors'
``JacobianLens.merge`` method, which computes an ``n_prompts``-weighted mean.
This wrapper establishes that the ten inputs cover the immutable 1,000-prompt
manifest exactly once and agree on every fitting setting before merging them.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
from typing import Any, Sequence

from .compatibility import JLENS_COMMIT, MODEL_COMMIT, MODEL_ID, MODEL_REVISION, VENDORED_JLENS
from .manifest import read_prompt_records


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FIT_ROOT = PROJECT_ROOT / "results" / "fit_1000"
DEFAULT_MANIFEST = DEFAULT_FIT_ROOT / "prompt_manifest.jsonl"
DEFAULT_SHARDS = DEFAULT_FIT_ROOT / "shards"
DEFAULT_OUTPUT_DIR = DEFAULT_FIT_ROOT / "merged"
EXPECTED_LAYERS = [12, 16, 18, 20, 22, 24]
EXPECTED_SHARDS = 10
EXPECTED_PROMPTS_PER_SHARD = 100
EXPECTED_HIDDEN_SIZE = 4096
EXPECTED_TARGET_LAYER = 31


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--shards-dir", type=Path, default=DEFAULT_SHARDS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def sha256(path: Path) -> str:
    """Return the hexadecimal SHA-256 digest of one file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def validate_shard_summary(
    summary: dict[str, Any],
    *,
    shard_index: int,
    expected_records: Sequence[dict[str, Any]],
    manifest_path: Path,
) -> None:
    """Validate one shard's identity, prompt membership, and fit settings."""
    expected_indices = [record["sample_index"] for record in expected_records]
    input_report = summary.get("input", {})
    fit = summary.get("fit", {})
    checks = {
        "status": summary.get("status") == "complete",
        "model": summary.get("model") == MODEL_ID,
        "model_commit": summary.get("model_commit") == MODEL_COMMIT,
        "jlens_commit": summary.get("jlens_commit") == JLENS_COMMIT,
        "input_mode": input_report.get("mode") == "fixed_manifest",
        "manifest": Path(input_report.get("prompt_manifest", "")) == manifest_path,
        "manifest_size": input_report.get("manifest_prompts")
        == EXPECTED_SHARDS * EXPECTED_PROMPTS_PER_SHARD,
        "num_shards": input_report.get("num_shards") == EXPECTED_SHARDS,
        "shard_index": input_report.get("shard_index") == shard_index,
        "sample_indices": input_report.get("selected_sample_indices") == expected_indices,
        "requested_prompts": fit.get("requested_prompts") == len(expected_records),
        "successful_prompts": fit.get("successful_prompts") == len(expected_records),
        "source_layers": fit.get("source_layers") == EXPECTED_LAYERS,
        "target_layer": fit.get("target_layer") == EXPECTED_TARGET_LAYER,
        "hidden_size": fit.get("hidden_size") == EXPECTED_HIDDEN_SIZE,
        "max_seq_len": fit.get("max_seq_len") == 128,
        "dim_batch": fit.get("dim_batch") == 8,
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise ValueError(f"shard {shard_index:02d} failed validation: {failed}")


def run(args: argparse.Namespace) -> dict[str, Any]:
    """Validate shard coverage, invoke the official merge, and save provenance."""
    lens_path = args.output_dir / "jacobian_lens.pt"
    summary_path = args.output_dir / "summary.json"
    if lens_path.exists() or summary_path.exists():
        raise FileExistsError("completed merged J-Lens output already exists")

    manifest_records = read_prompt_records(args.manifest)
    expected_total = EXPECTED_SHARDS * EXPECTED_PROMPTS_PER_SHARD
    if len(manifest_records) != expected_total:
        raise ValueError(f"expected {expected_total} manifest prompts")

    shard_paths: list[Path] = []
    shard_reports: list[dict[str, Any]] = []
    covered_samples: list[int] = []
    for shard_index in range(EXPECTED_SHARDS):
        shard_dir = args.shards_dir / f"shard_{shard_index:02d}"
        shard_summary_path = shard_dir / "summary.json"
        shard_prompts_path = shard_dir / "prompts.jsonl"
        shard_lens_path = shard_dir / "jacobian_lens.pt"
        for required in (shard_summary_path, shard_prompts_path, shard_lens_path):
            if not required.is_file():
                raise FileNotFoundError(f"missing shard artifact: {required}")

        start = shard_index * EXPECTED_PROMPTS_PER_SHARD
        expected_records = manifest_records[start : start + EXPECTED_PROMPTS_PER_SHARD]
        actual_records = read_prompt_records(shard_prompts_path)
        if actual_records != expected_records:
            raise ValueError(f"shard {shard_index:02d} prompts differ from manifest slice")
        summary = json.loads(shard_summary_path.read_text(encoding="utf-8"))
        validate_shard_summary(
            summary,
            shard_index=shard_index,
            expected_records=expected_records,
            manifest_path=args.manifest,
        )
        covered_samples.extend(record["sample_index"] for record in actual_records)
        shard_paths.append(shard_lens_path)
        shard_reports.append(
            {
                "shard_index": shard_index,
                "num_prompts": len(actual_records),
                "lens": str(shard_lens_path),
                "lens_sha256": sha256(shard_lens_path),
            }
        )

    manifest_samples = [record["sample_index"] for record in manifest_records]
    if covered_samples != manifest_samples or len(set(covered_samples)) != expected_total:
        raise ValueError("shards do not cover the manifest exactly once")

    if not (VENDORED_JLENS / "jlens" / "__init__.py").is_file():
        raise FileNotFoundError(f"missing official J-Lens checkout: {VENDORED_JLENS}")
    sys.path.insert(0, str(VENDORED_JLENS))
    import jlens

    lenses = [jlens.JacobianLens.load(str(path)) for path in shard_paths]
    for shard_index, lens in enumerate(lenses):
        if (
            lens.n_prompts != EXPECTED_PROMPTS_PER_SHARD
            or lens.source_layers != EXPECTED_LAYERS
            or lens.d_model != EXPECTED_HIDDEN_SIZE
        ):
            raise ValueError(f"shard {shard_index:02d} lens metadata is inconsistent")

    merged = jlens.JacobianLens.merge(lenses)
    if (
        merged.n_prompts != expected_total
        or merged.source_layers != EXPECTED_LAYERS
        or merged.d_model != EXPECTED_HIDDEN_SIZE
    ):
        raise ValueError("merged lens metadata is inconsistent")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    temporary_lens = lens_path.with_name(f"{lens_path.name}.tmp.{os.getpid()}")
    try:
        merged.save(str(temporary_lens))
        os.replace(temporary_lens, lens_path)
    finally:
        temporary_lens.unlink(missing_ok=True)

    reloaded = jlens.JacobianLens.load(str(lens_path))
    if (
        reloaded.n_prompts != expected_total
        or reloaded.source_layers != EXPECTED_LAYERS
        or reloaded.d_model != EXPECTED_HIDDEN_SIZE
    ):
        raise ValueError("saved merged lens failed reload validation")

    summary = {
        "status": "complete",
        "operation": "official JacobianLens.merge n_prompts-weighted mean",
        "model": MODEL_ID,
        "stage_one_revision": MODEL_REVISION,
        "model_commit": MODEL_COMMIT,
        "jlens_commit": JLENS_COMMIT,
        "manifest": str(args.manifest),
        "manifest_sha256": sha256(args.manifest),
        "num_shards": len(lenses),
        "total_prompts": merged.n_prompts,
        "source_layers": merged.source_layers,
        "hidden_size": merged.d_model,
        "shards": shard_reports,
        "output": {
            "lens": str(lens_path),
            "lens_sha256": sha256(lens_path),
        },
    }
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return summary


def main() -> None:
    run(parse_args())


if __name__ == "__main__":
    main()
