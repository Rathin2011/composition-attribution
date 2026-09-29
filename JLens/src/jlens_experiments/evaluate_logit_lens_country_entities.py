"""Evaluate complete-country evidence with an ordinary logit lens.

This is the direct comparison for the J-Lens country-entity diagnostic.  It
uses the same saved prompts, query-token positions, and six layers.  It reports
the earlier closed-country-set mean score plus stricter mean-token and
maximum-token ranks against every vocabulary token except the tokens
constituting the target country.  Intermediate residuals are normalized and
unembedded directly, without Jacobian transport into the final-layer basis.

Outputs
-------
* ``per_query.jsonl``: one complete-country logit-lens measurement per query.
* ``summary.json``: evidence-band counts for the two original query groups.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import statistics
from typing import Any, Sequence

from .compatibility import MODEL_COMMIT, MODEL_ID, MODEL_REVISION
from .evaluate_landmarks import (
    DEFAULT_GROUP_FILES,
    DEFAULT_LENS,
    EXPECTED_COUNTS,
    _import_runtime,
    atomic_write_jsonl,
    country_candidates,
    country_entity_target_ranks,
    read_group,
    summarize_readout,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "results" / "logit_lens_country_entities"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compositional", type=Path, default=DEFAULT_GROUP_FILES["compositional"])
    parser.add_argument("--shortcut", type=Path, default=DEFAULT_GROUP_FILES["shortcut_candidate"])
    parser.add_argument(
        "--lens",
        type=Path,
        default=DEFAULT_LENS,
        help="J-Lens checkpoint used only to select the identical six source layers.",
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-seq-len", type=int, default=512)
    parser.add_argument("--progress-every", type=int, default=10)
    parser.add_argument(
        "--allow-download",
        action="store_true",
        help="Allow Hugging Face downloads instead of requiring cached files.",
    )
    return parser.parse_args()


def full_vocabulary_entity_target_ranks(
    logits: Any,
    token_ids: Sequence[int],
    reduction: str = "mean",
) -> list[int]:
    """Rank a reduced entity-token score against all non-constituent tokens."""
    if logits.ndim != 2:
        raise ValueError("logits must have shape [positions, vocabulary]")
    if not token_ids:
        raise ValueError("country entity needs at least one token")
    vocabulary_size = logits.shape[1]
    if any(token_id < 0 or token_id >= vocabulary_size for token_id in token_ids):
        raise ValueError("country token is outside the vocabulary")
    if reduction not in {"mean", "max"}:
        raise ValueError("reduction must be 'mean' or 'max'")

    constituent_ids = sorted(set(token_ids))
    constituent_logits = logits[:, list(token_ids)]
    entity_score = (
        constituent_logits.mean(dim=1, keepdim=True)
        if reduction == "mean"
        else constituent_logits.max(dim=1, keepdim=True).values
    )
    outranks_entity = logits > entity_score
    outranks_entity[:, constituent_ids] = False
    return (1 + outranks_entity.sum(dim=1)).to("cpu").tolist()


def aggregate_entity(
    rows: Sequence[dict[str, Any]],
    group: str,
    measurement_key: str = "logit_lens_country_entity",
) -> dict[str, Any]:
    """Summarize country-entity ranks for one original query group."""
    selected = [row for row in rows if row["original_group"] == group]
    if not selected:
        raise ValueError(f"no rows for group {group}")
    ranks = [row[measurement_key]["best_rank"] for row in selected]
    bands = Counter(row[measurement_key]["evidence_band"] for row in selected)
    return {
        "num_queries": len(selected),
        "country_entity_evidence_bands": {
            key: bands.get(key, 0)
            for key in ("compositional", "ambiguous", "shortcut_candidate")
        },
        "median_country_entity_rank": statistics.median(ranks),
        "mean_country_entity_reciprocal_rank": statistics.mean(1.0 / rank for rank in ranks),
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    """Run ordinary logit lens and save complete-country evidence."""
    if args.max_seq_len < 1 or args.progress_every < 1:
        raise ValueError("length and progress settings must be positive")
    rows_path = args.output_dir / "per_query.jsonl"
    summary_path = args.output_dir / "summary.json"
    if rows_path.exists() or summary_path.exists():
        raise FileExistsError("completed logit-lens country-entity output already exists")

    grouped = {
        "compositional": read_group(
            args.compositional, "compositional", EXPECTED_COUNTS["compositional"]
        ),
        "shortcut_candidate": read_group(
            args.shortcut, "shortcut_candidate", EXPECTED_COUNTS["shortcut_candidate"]
        ),
    }
    all_records = [record for records in grouped.values() for record in records]
    identities = [(record["evaluation_index"], record["dataset_index"]) for record in all_records]
    if len(identities) != len(set(identities)):
        raise ValueError("query identities overlap within or across input groups")

    candidate_map = country_candidates(all_records)
    candidate_names = list(candidate_map)
    candidate_token_ids = list(candidate_map.values())
    candidate_indices = {country: index for index, country in enumerate(candidate_names)}

    jlens, torch, model_class, tokenizer_class = _import_runtime()
    # Loading the checkpoint fixes the comparison to exactly the same six
    # layers.  Its Jacobian matrices are never applied in this program.
    lens = jlens.JacobianLens.load(str(args.lens))
    tokenizer = tokenizer_class.from_pretrained(
        MODEL_ID, revision=MODEL_COMMIT, local_files_only=not args.allow_download
    )
    model = model_class.from_pretrained(
        MODEL_ID,
        revision=MODEL_COMMIT,
        dtype=torch.bfloat16,
        device_map="auto",
        local_files_only=not args.allow_download,
    )
    adapter = jlens.from_hf(model, tokenizer, compile=False, force_bos=False)
    layers = lens.source_layers

    rows: list[dict[str, Any]] = []
    total = len(all_records)
    for original_group, records in grouped.items():
        for record in records:
            start = record["query_token_start"]
            positions = list(range(start, start + record["num_query_positions"]))
            logits_by_layer, _, input_ids = lens.apply(
                adapter,
                record["prediction"]["prompt"],
                layers=layers,
                positions=positions,
                max_seq_len=args.max_seq_len,
                use_jacobian=False,
            )
            if positions[-1] >= input_ids.shape[1]:
                raise ValueError(
                    f"saved query span exceeds prompt for evaluation_index={record['evaluation_index']}"
                )
            target_index = candidate_indices[record["query"]["Fx"]]
            measurement = summarize_readout(
                {
                    layer: country_entity_target_ranks(
                        logits_by_layer[layer], candidate_token_ids, target_index
                    )
                    for layer in layers
                }
            )
            target_country_token_ids = record["node_evidence"]["Fx"]["token_ids"]
            full_vocabulary_measurement = summarize_readout(
                {
                    layer: full_vocabulary_entity_target_ranks(
                        logits_by_layer[layer], target_country_token_ids
                    )
                    for layer in layers
                }
            )
            full_vocabulary_max_measurement = summarize_readout(
                {
                    layer: full_vocabulary_entity_target_ranks(
                        logits_by_layer[layer],
                        target_country_token_ids,
                        reduction="max",
                    )
                    for layer in layers
                }
            )
            rows.append(
                {
                    "evaluation_index": record["evaluation_index"],
                    "dataset_index": record["dataset_index"],
                    "original_group": original_group,
                    "landmark": record["query"]["x"],
                    "country": record["query"]["Fx"],
                    "capital": record["query"]["GFx"],
                    "country_token_ids": target_country_token_ids,
                    "country_token_count": len(target_country_token_ids),
                    "query_token_start": start,
                    "num_query_positions": len(positions),
                    "logit_lens_country_entity": measurement,
                    "logit_lens_country_entity_full_vocabulary": (
                        full_vocabulary_measurement
                    ),
                    "logit_lens_country_entity_full_vocabulary_max": (
                        full_vocabulary_max_measurement
                    ),
                }
            )
            if len(rows) % args.progress_every == 0 or len(rows) == total:
                print(f"evaluated {len(rows)}/{total}", flush=True)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_jsonl(rows_path, rows)
    summary = {
        "status": "complete",
        "readout": "ordinary_logit_lens",
        "country_scores": {
            "closed_country_set": "mean constituent-token logit",
            "full_vocabulary": "mean and maximum constituent-token logits",
        },
        "comparison_sets": {
            "closed_country_set": "all country labels in the 475 evaluated queries",
            "full_vocabulary": (
                "all vocabulary tokens except the target country's constituent tokens"
            ),
        },
        "model": MODEL_ID,
        "stage_one_revision": MODEL_REVISION,
        "model_commit": MODEL_COMMIT,
        "source_layers": layers,
        "total_queries": len(rows),
        "country_entity_candidates": candidate_names,
        "groups": {
            group: {
                "closed_country_set": aggregate_entity(rows, group),
                "full_vocabulary": aggregate_entity(
                    rows,
                    group,
                    "logit_lens_country_entity_full_vocabulary",
                ),
                "full_vocabulary_max": aggregate_entity(
                    rows,
                    group,
                    "logit_lens_country_entity_full_vocabulary_max",
                ),
            }
            for group in ("compositional", "shortcut_candidate")
        },
        "outputs": {"per_query": str(rows_path)},
    }
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return summary


def main() -> None:
    run(parse_args())


if __name__ == "__main__":
    main()
