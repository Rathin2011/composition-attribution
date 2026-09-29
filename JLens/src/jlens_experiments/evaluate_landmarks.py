"""Compare J-Lens and logit-lens country evidence on landmark queries.

Inputs
------
* The saved, correctly answered landmark-query JSONL files already classified
  as compositional or shortcut candidates by the original 32-layer logit lens.
* A fitted :class:`jlens.JacobianLens`.
* The pinned OLMo 3 stage-one checkpoint.

For every query, this program measures every token in the country name at
every layer available in the fitted J-Lens.  It takes each token's best rank
across the landmark's query-token positions.  The first-token measurement is
still exposed as ``j_lens`` so existing analysis remains compatible; the full
sequence is exposed as ``country_token_evidence`` for diagnosing whether
generic first tokens in multi-token country names create false negatives.
The program also assigns each complete country name a length-normalized score
(the mean logit of all its tokens) and ranks the correct country against every
country label occurring in the evaluated dataset.

Outputs
-------
* ``per_query.jsonl``: one record per query with layerwise ranks and peak
  evidence under both readouts.
* ``summary.json``: group-level evidence bands and improvement counts.

This is a readout comparison, not a causal intervention and not a replacement
for the original all-layer classification.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import statistics
import sys
from typing import Any, Iterable, Sequence

from .compatibility import MODEL_COMMIT, MODEL_ID, MODEL_REVISION, VENDORED_JLENS


PROJECT_ROOT = Path(__file__).resolve().parents[2]
COUNTRY_RESULTS = Path(
    "/projectnb/buinlp/rathin/composition-experiments/country-capital/results"
)
DEFAULT_GROUP_FILES = {
    "compositional": COUNTRY_RESULTS
    / "olmo3_stage1_landmark_country_capital.compositional.jsonl",
    "shortcut_candidate": COUNTRY_RESULTS
    / "olmo3_stage1_landmark_country_capital.shortcut_candidates.jsonl",
}
DEFAULT_LENS = (
    PROJECT_ROOT / "results" / "fit_1000" / "merged" / "jacobian_lens.pt"
)
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "results" / "landmark_evaluation"
EXPECTED_COUNTS = {"compositional": 370, "shortcut_candidate": 105}
COMPOSITION_RR_THRESHOLD = 0.5
SHORTCUT_RR_THRESHOLD = 0.2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compositional", type=Path, default=DEFAULT_GROUP_FILES["compositional"])
    parser.add_argument("--shortcut", type=Path, default=DEFAULT_GROUP_FILES["shortcut_candidate"])
    parser.add_argument("--lens", type=Path, default=DEFAULT_LENS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-seq-len", type=int, default=512)
    parser.add_argument("--progress-every", type=int, default=10)
    parser.add_argument(
        "--allow-download",
        action="store_true",
        help="Allow Hugging Face downloads instead of requiring cached files.",
    )
    return parser.parse_args()


def read_group(path: Path, expected_group: str, expected_count: int | None) -> list[dict[str, Any]]:
    """Load one saved query group and validate its identity and core fields."""
    records: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            record = json.loads(line)
            if record.get("model_commit") != MODEL_COMMIT:
                raise ValueError(f"wrong model commit at {path}:{line_number}")
            if record.get("classification", {}).get("group") != expected_group:
                raise ValueError(f"wrong group at {path}:{line_number}")
            if not isinstance(record.get("prediction", {}).get("prompt"), str):
                raise ValueError(f"missing prompt at {path}:{line_number}")
            if not isinstance(record.get("query", {}).get("Fx"), str):
                raise ValueError(f"missing country at {path}:{line_number}")
            country_evidence = record.get("node_evidence", {}).get("Fx", {})
            token_id = country_evidence.get("first_token_id")
            if not isinstance(token_id, int) or isinstance(token_id, bool):
                raise ValueError(f"invalid country token at {path}:{line_number}")
            token_ids = country_evidence.get("token_ids")
            if (
                not isinstance(token_ids, list)
                or not token_ids
                or any(not isinstance(item, int) or isinstance(item, bool) for item in token_ids)
                or token_ids[0] != token_id
            ):
                raise ValueError(f"invalid country token sequence at {path}:{line_number}")
            start = record.get("query_token_start")
            count = record.get("num_query_positions")
            if not isinstance(start, int) or not isinstance(count, int) or start < 0 or count < 1:
                raise ValueError(f"invalid query positions at {path}:{line_number}")
            records.append(record)
    if expected_count is not None and len(records) != expected_count:
        raise ValueError(f"expected {expected_count} {expected_group} records, found {len(records)}")
    return records


def target_ranks(logits: Any, token_id: int) -> list[int]:
    """Return one-based target rank at every position, using shared-best ties."""
    if logits.ndim != 2:
        raise ValueError("logits must have shape [positions, vocabulary]")
    if not 0 <= token_id < logits.shape[1]:
        raise ValueError("token_id is outside the vocabulary")
    target = logits[:, token_id].unsqueeze(1)
    return (1 + (logits > target).sum(dim=1)).to("cpu").tolist()


def country_entity_target_ranks(
    logits: Any,
    candidate_token_ids: Sequence[Sequence[int]],
    target_index: int,
) -> list[int]:
    """Rank one complete country label against all candidate country labels.

    A country's score is the mean logit of all tokens in its stored token
    sequence.  Averaging prevents longer country names from receiving a
    systematic scale advantage or penalty solely because of token count.
    """
    if logits.ndim != 2:
        raise ValueError("logits must have shape [positions, vocabulary]")
    if not candidate_token_ids or not 0 <= target_index < len(candidate_token_ids):
        raise ValueError("target country must index a nonempty candidate set")
    if any(not token_ids for token_ids in candidate_token_ids):
        raise ValueError("every candidate country needs at least one token")
    vocabulary_size = logits.shape[1]
    if any(
        token_id < 0 or token_id >= vocabulary_size
        for token_ids in candidate_token_ids
        for token_id in token_ids
    ):
        raise ValueError("country token is outside the vocabulary")

    def entity_score(token_ids: Sequence[int]) -> Any:
        return logits[:, list(token_ids)].mean(dim=1)

    target_score = entity_score(candidate_token_ids[target_index])
    ranks: Any = 1
    for index, token_ids in enumerate(candidate_token_ids):
        if index != target_index:
            ranks = ranks + (entity_score(token_ids) > target_score)
    if isinstance(ranks, int):
        return [ranks] * logits.shape[0]
    return ranks.to("cpu").tolist()


def evidence_band(peak_reciprocal_rank: float) -> str:
    """Apply the same RR bands used by the saved logit-lens experiment."""
    if peak_reciprocal_rank >= COMPOSITION_RR_THRESHOLD:
        return "compositional"
    if peak_reciprocal_rank <= SHORTCUT_RR_THRESHOLD:
        return "shortcut_candidate"
    return "ambiguous"


def summarize_readout(layer_ranks: dict[int, list[int]]) -> dict[str, Any]:
    """Summarize positionwise ranks into the best evidence over layers."""
    if not layer_ranks or any(not ranks for ranks in layer_ranks.values()):
        raise ValueError("every layer needs at least one position rank")
    layerwise = []
    for layer in sorted(layer_ranks):
        best_rank = min(layer_ranks[layer])
        layerwise.append(
            {
                "layer": layer,
                "position_ranks": layer_ranks[layer],
                "best_rank": best_rank,
                "reciprocal_rank": 1.0 / best_rank,
            }
        )
    overall_best = min(item["best_rank"] for item in layerwise)
    peak_layers = [item["layer"] for item in layerwise if item["best_rank"] == overall_best]
    peak_rr = 1.0 / overall_best
    return {
        "best_rank": overall_best,
        "peak_reciprocal_rank": peak_rr,
        "peak_layers": peak_layers,
        "evidence_band": evidence_band(peak_rr),
        "layers": layerwise,
    }


def measure_country_tokens(
    logits_by_layer: dict[int, Any],
    token_ids: Sequence[int],
    token_texts: Sequence[str],
) -> list[dict[str, Any]]:
    """Measure J-Lens evidence separately for every token in a country name."""
    if not logits_by_layer:
        raise ValueError("at least one layer of logits is required")
    if not token_ids or len(token_ids) != len(token_texts):
        raise ValueError("country token IDs and texts must have equal nonzero length")
    return [
        {
            "token_index": index,
            "token_id": token_id,
            "token": token_text,
            "j_lens": summarize_readout(
                {
                    layer: target_ranks(logits, token_id)
                    for layer, logits in logits_by_layer.items()
                }
            ),
        }
        for index, (token_id, token_text) in enumerate(zip(token_ids, token_texts, strict=True))
    ]


def country_candidates(records: Iterable[dict[str, Any]]) -> dict[str, tuple[int, ...]]:
    """Build a deterministic country-label vocabulary from saved query rows."""
    candidates: dict[str, tuple[int, ...]] = {}
    for record in records:
        country = record["query"]["Fx"]
        token_ids = tuple(record["node_evidence"]["Fx"]["token_ids"])
        previous = candidates.setdefault(country, token_ids)
        if previous != token_ids:
            raise ValueError(f"country has inconsistent tokenization: {country}")
    return dict(sorted(candidates.items()))


def stored_logit_lens(record: dict[str, Any], layers: Sequence[int]) -> dict[str, Any]:
    """Extract the original logit-lens country evidence at fitted layers."""
    reciprocal_ranks = record["node_evidence"]["Fx"]["layerwise_max_reciprocal_rank"]
    if max(layers) >= len(reciprocal_ranks):
        raise ValueError("saved logit-lens evidence lacks a fitted layer")
    ranks = {
        layer: [int(round(1.0 / float(reciprocal_ranks[layer])))] for layer in layers
    }
    return summarize_readout(ranks)


def aggregate(rows: Sequence[dict[str, Any]], group: str) -> dict[str, Any]:
    """Aggregate paired J-Lens/logit-lens measurements for one query group."""
    selected = [row for row in rows if row["original_group"] == group]
    if not selected:
        raise ValueError(f"no rows for group {group}")
    original_ranks = [row["logit_lens_fitted_layers"]["best_rank"] for row in selected]
    jlens_ranks = [row["j_lens"]["best_rank"] for row in selected]
    bands = Counter(row["j_lens"]["evidence_band"] for row in selected)
    return {
        "num_queries": len(selected),
        "j_lens_evidence_bands": {
            key: bands.get(key, 0)
            for key in ("compositional", "ambiguous", "shortcut_candidate")
        },
        "j_lens_better_rank": sum(j < old for j, old in zip(jlens_ranks, original_ranks, strict=True)),
        "same_rank": sum(j == old for j, old in zip(jlens_ranks, original_ranks, strict=True)),
        "j_lens_worse_rank": sum(j > old for j, old in zip(jlens_ranks, original_ranks, strict=True)),
        "median_logit_lens_rank_fitted_layers": statistics.median(original_ranks),
        "median_j_lens_rank": statistics.median(jlens_ranks),
        "mean_logit_lens_peak_rr_fitted_layers": statistics.mean(1.0 / rank for rank in original_ranks),
        "mean_j_lens_peak_rr": statistics.mean(1.0 / rank for rank in jlens_ranks),
    }


def atomic_write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    """Write JSONL atomically so an interrupted run cannot look complete."""
    temporary = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    try:
        with temporary.open("w", encoding="utf-8") as handle:
            for record in records:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _import_runtime() -> tuple[Any, Any, Any, Any]:
    if not (VENDORED_JLENS / "jlens" / "__init__.py").is_file():
        raise FileNotFoundError(f"missing official J-Lens checkout: {VENDORED_JLENS}")
    sys.path.insert(0, str(VENDORED_JLENS))
    import jlens
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    return jlens, torch, AutoModelForCausalLM, AutoTokenizer


def run(args: argparse.Namespace) -> dict[str, Any]:
    """Load the model and fitted lens, evaluate both groups, and save results."""
    if args.max_seq_len < 1 or args.progress_every < 1:
        raise ValueError("length and progress settings must be positive")
    output_dir = args.output_dir
    rows_path = output_dir / "per_query.jsonl"
    summary_path = output_dir / "summary.json"
    if rows_path.exists() or summary_path.exists():
        raise FileExistsError("completed landmark J-Lens output already exists")

    grouped = {
        "compositional": read_group(
            args.compositional, "compositional", EXPECTED_COUNTS["compositional"]
        ),
        "shortcut_candidate": read_group(
            args.shortcut, "shortcut_candidate", EXPECTED_COUNTS["shortcut_candidate"]
        ),
    }
    identities = [
        (record["evaluation_index"], record["dataset_index"])
        for records in grouped.values()
        for record in records
    ]
    if len(identities) != len(set(identities)):
        raise ValueError("query identities overlap within or across input groups")
    candidate_map = country_candidates(
        record for records in grouped.values() for record in records
    )
    candidate_names = list(candidate_map)
    candidate_token_ids = list(candidate_map.values())
    candidate_indices = {country: index for index, country in enumerate(candidate_names)}

    jlens, torch, model_class, tokenizer_class = _import_runtime()
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
    # force_bos=False preserves the exact tokenization used to create the saved
    # query positions in the original landmark analysis.
    adapter = jlens.from_hf(model, tokenizer, compile=False, force_bos=False)
    layers = lens.source_layers
    lens.jacobians = {
        layer: matrix.to(adapter.input_device) for layer, matrix in lens.jacobians.items()
    }

    rows: list[dict[str, Any]] = []
    total = sum(len(records) for records in grouped.values())
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
                use_jacobian=True,
            )
            if positions[-1] >= input_ids.shape[1]:
                raise ValueError(
                    f"saved query span exceeds prompt for evaluation_index={record['evaluation_index']}"
                )
            country_token_ids = record["node_evidence"]["Fx"]["token_ids"]
            country_token_evidence = measure_country_tokens(
                logits_by_layer,
                country_token_ids,
                [
                    tokenizer.decode([token_id], clean_up_tokenization_spaces=False)
                    for token_id in country_token_ids
                ],
            )
            country_token_id = country_token_ids[0]
            jlens_measurement = country_token_evidence[0]["j_lens"]
            country_entity_measurement = summarize_readout(
                {
                    layer: country_entity_target_ranks(
                        logits_by_layer[layer],
                        candidate_token_ids,
                        candidate_indices[record["query"]["Fx"]],
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
                    "country_first_token_id": country_token_id,
                    "country_first_token": record["node_evidence"]["Fx"]["first_token"],
                    "country_token_count": len(country_token_ids),
                    "country_token_evidence": country_token_evidence,
                    "j_lens_last_country_token": country_token_evidence[-1]["j_lens"],
                    "j_lens_country_entity": country_entity_measurement,
                    "query_token_start": start,
                    "num_query_positions": len(positions),
                    "original_logit_lens_all_layers": {
                        "best_rank": record["classification"]["best_vocabulary_rank"],
                        "peak_reciprocal_rank": record["classification"]["peak_reciprocal_rank"],
                        "peak_layers": record["classification"]["peak_layers"],
                    },
                    "logit_lens_fitted_layers": stored_logit_lens(record, layers),
                    "j_lens": jlens_measurement,
                }
            )
            if len(rows) % args.progress_every == 0 or len(rows) == total:
                print(f"evaluated {len(rows)}/{total}", flush=True)

    output_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_jsonl(rows_path, rows)
    summary = {
        "status": "complete",
        "scope": (
            "six fitted layers; original groups unchanged; all country tokens and "
            "length-normalized country entities measured"
        ),
        "model": MODEL_ID,
        "stage_one_revision": MODEL_REVISION,
        "model_commit": MODEL_COMMIT,
        "lens": str(args.lens),
        "source_layers": layers,
        "thresholds": {
            "compositional_rr": COMPOSITION_RR_THRESHOLD,
            "shortcut_rr": SHORTCUT_RR_THRESHOLD,
        },
        "total_queries": len(rows),
        "country_entity_candidates": candidate_names,
        "groups": {
            group: aggregate(rows, group)
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
