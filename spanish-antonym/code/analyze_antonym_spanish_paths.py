"""Classify correct antonym-Spanish compositions using OLMo 3 logit lens."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any, Literal

import torch

from composition_evidence import (
    COMPOSITION_RR_THRESHOLD,
    SHORTCUT_RR_THRESHOLD,
    classify_reciprocal_rank,
)
from load_olmo3_stage1 import MODEL_ID, STAGE_ONE_COMMIT, STAGE_ONE_REVISION
from olmo3_logit_lens import REFERENCE_CODE_COMMIT, capture_residual_stream, target_token_ranks


NODES = ("x", "Fx", "Gx", "GFx")
INTERMEDIATE_NODES = ("Fx", "Gx")
EXPECTED_CORRECT = 687
EXPECTED_ELIGIBLE = 519
STRONG_RR_THRESHOLD = COMPOSITION_RR_THRESHOLD

PROJECT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_DIR / "results"
DEFAULT_INPUT = RESULTS_DIR / "olmo3_stage1_antonym_spanish_all.correct.jsonl"
DEFAULT_FX_OUTPUT = RESULTS_DIR / "olmo3_stage1_antonym_spanish_path_fx.jsonl"
DEFAULT_GX_OUTPUT = RESULTS_DIR / "olmo3_stage1_antonym_spanish_path_gx.jsonl"

PathName = Literal["antonym_then_translate", "translate_then_antonym"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--fx-output", type=Path, default=DEFAULT_FX_OUTPUT)
    parser.add_argument("--gx-output", type=Path, default=DEFAULT_GX_OUTPUT)
    parser.add_argument("--expected-correct", type=int, default=EXPECTED_CORRECT)
    parser.add_argument("--expected-eligible", type=int, default=EXPECTED_ELIGIBLE)
    parser.add_argument("--max-records", type=int)
    parser.add_argument("--chunk-size", type=int, default=32)
    return parser.parse_args()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records))


def node_token_info(tokenizer: Any, query: dict) -> dict[str, dict]:
    """Tokenize variables exactly as the paper does for lexical tasks."""

    info = {}
    for node in NODES:
        token_ids = tokenizer.encode(" " + query[node], add_special_tokens=False)
        if not token_ids:
            raise ValueError(f"{node} has no tokens")
        info[node] = {
            "value": query[node],
            "first_token_id": token_ids[0],
            "first_token": tokenizer.decode(token_ids[0]),
            "token_ids": token_ids,
        }
    return info


def passes_paper_token_filter(token_info: dict[str, dict]) -> bool:
    """Apply the authors' first-token overlap exclusions."""

    first_tokens = [token_info[node]["first_token_id"] for node in NODES]
    if len(first_tokens) != len(set(first_tokens)):
        return False

    non_x_first_tokens = {
        token_info[node]["first_token_id"] for node in NODES if node != "x"
    }
    return not bool(non_x_first_tokens & set(token_info["x"]["token_ids"]))


def select_paper_eligible(records: list[dict], tokenizer: Any) -> list[tuple[dict, dict[str, dict]]]:
    selected = []
    for record in records:
        token_info = node_token_info(tokenizer, record["query"])
        if passes_paper_token_filter(token_info):
            selected.append((record, token_info))
    return selected


def first_query_token_index(tokenizer: Any, prompt: str, x: str) -> int:
    """Mirror the reference code's right-to-left query-token boundary."""

    query_characters = len(f"{x}\nA:")
    prompt_tokens = tokenizer.encode(prompt, add_special_tokens=False)
    for token_index in range(len(prompt_tokens) - 1, -1, -1):
        query_characters -= len(tokenizer.decode(prompt_tokens[token_index]))
        if query_characters <= 0:
            return token_index
    raise ValueError("could not locate query tokens in prompt")


def summarize_node_evidence(
    ranks: torch.Tensor,
    token_info: dict[str, dict],
    *,
    prompt_position_offset: int,
) -> dict[str, dict]:
    """Summarize per-layer and peak evidence for every tracked variable."""

    if ranks.ndim != 3 or ranks.shape[2] != len(NODES):
        raise ValueError("ranks must have shape [positions, layers, four nodes]")

    reciprocal_ranks = 1.0 / ranks.float()
    evidence = {}
    for node_index, node in enumerate(NODES):
        node_rr = reciprocal_ranks[:, :, node_index]
        layerwise_max = node_rr.max(dim=0).values
        max_rr = layerwise_max.max()
        peak_locations = (node_rr == max_rr).nonzero(as_tuple=False)
        peak_layers = sorted({location[1].item() for location in peak_locations})
        evidence[node] = {
            **token_info[node],
            "peak_reciprocal_rank": max_rr.item(),
            "best_vocabulary_rank": int(round(1.0 / max_rr.item())),
            "strong_presence": max_rr.item() >= STRONG_RR_THRESHOLD,
            "peak_layers": peak_layers,
            "first_peak_layer": peak_layers[0],
            "peak_locations": [
                {
                    "query_position": location[0].item(),
                    "prompt_position": prompt_position_offset + location[0].item(),
                    "layer": location[1].item(),
                }
                for location in peak_locations
            ],
            "layerwise_max_reciprocal_rank": layerwise_max.tolist(),
            "mean_layerwise_max_reciprocal_rank": mean(layerwise_max.tolist()),
        }
    return evidence


def classify_path(evidence: dict[str, dict]) -> dict:
    """Choose the intermediate with stronger evidence using documented tie breaks."""

    fx = evidence["Fx"]
    gx = evidence["Gx"]
    fx_peak = fx["peak_reciprocal_rank"]
    gx_peak = gx["peak_reciprocal_rank"]
    tied_on_peak = fx_peak == gx_peak

    if fx_peak != gx_peak:
        selected = "Fx" if fx_peak > gx_peak else "Gx"
        tie_breaker = "peak_reciprocal_rank"
    elif fx["mean_layerwise_max_reciprocal_rank"] != gx["mean_layerwise_max_reciprocal_rank"]:
        selected = (
            "Fx"
            if fx["mean_layerwise_max_reciprocal_rank"]
            > gx["mean_layerwise_max_reciprocal_rank"]
            else "Gx"
        )
        tie_breaker = "mean_layerwise_max_reciprocal_rank"
    elif fx["first_peak_layer"] != gx["first_peak_layer"]:
        selected = "Fx" if fx["first_peak_layer"] < gx["first_peak_layer"] else "Gx"
        tie_breaker = "earlier_first_peak_layer"
    else:
        selected = "Fx"
        tie_breaker = "deterministic_fx_fallback"

    path: PathName = (
        "antonym_then_translate" if selected == "Fx" else "translate_then_antonym"
    )
    winner = evidence[selected]
    group = classify_reciprocal_rank(winner["peak_reciprocal_rank"])
    return {
        "group": group,
        "path": path,
        "selected_intermediate": selected,
        "path_peak_reciprocal_rank": winner["peak_reciprocal_rank"],
        "path_peak_layers": winner["peak_layers"],
        "strong_path_evidence": group == "compositional",
        "shortcut_candidate": group == "shortcut_candidate",
        "composition_rr_threshold": COMPOSITION_RR_THRESHOLD,
        "shortcut_rr_threshold": SHORTCUT_RR_THRESHOLD,
        "tied_on_peak_reciprocal_rank": tied_on_peak,
        "tie_breaker": tie_breaker,
    }


def analyze_record(
    model: Any,
    tokenizer: Any,
    record: dict,
    token_info: dict[str, dict],
    *,
    chunk_size: int,
) -> dict:
    prompt = record["prediction"]["prompt"]
    query_start = first_query_token_index(tokenizer, prompt, record["query"]["x"])
    model_inputs = tokenizer(
        [prompt],
        return_tensors="pt",
        return_token_type_ids=False,
    )
    input_device = model.get_input_embeddings().weight.device
    model_inputs = {name: tensor.to(input_device) for name, tensor in model_inputs.items()}

    residual_stream = capture_residual_stream(
        model,
        model_inputs,
        position_slice=slice(query_start, None),
    )
    ranks = target_token_ranks(
        model,
        residual_stream,
        [token_info[node]["first_token_id"] for node in NODES],
        chunk_size=chunk_size,
    )
    evidence = summarize_node_evidence(
        ranks,
        token_info,
        prompt_position_offset=query_start,
    )
    classification = classify_path(evidence)

    return {
        "model": MODEL_ID,
        "stage_one_revision": STAGE_ONE_REVISION,
        "model_commit": STAGE_ONE_COMMIT,
        "reference_code_commit": REFERENCE_CODE_COMMIT,
        "evaluation_index": record["evaluation_index"],
        "dataset_index": record["dataset_index"],
        "context": record["context"],
        "query": record["query"],
        "prediction": record["prediction"],
        "query_token_start": query_start,
        "num_query_positions": residual_stream.shape[0],
        "classification": classification,
        "node_evidence": evidence,
    }


def main() -> None:
    args = parse_args()
    if args.max_records is not None and args.max_records <= 0:
        raise ValueError("max_records must be positive")

    from transformers import AutoModelForCausalLM, AutoTokenizer

    records = read_jsonl(args.input)
    if len(records) != args.expected_correct:
        raise RuntimeError(
            f"Expected {args.expected_correct} correct records, got {len(records)}"
        )

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID,
        revision=STAGE_ONE_COMMIT,
        padding_side="left",
    )
    eligible = select_paper_eligible(records, tokenizer)
    if len(eligible) != args.expected_eligible:
        raise RuntimeError(
            f"Expected {args.expected_eligible} paper-filtered records, "
            f"got {len(eligible)}"
        )
    if args.max_records is not None:
        eligible = eligible[: args.max_records]

    print(f"Loaded {len(records)} correct compositions; analyzing {len(eligible)} paper-filtered examples")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        revision=STAGE_ONE_COMMIT,
        device_map="auto",
        dtype="auto",
    )
    model.eval()

    fx_records = []
    gx_records = []
    for index, (record, token_info) in enumerate(eligible, start=1):
        analyzed = analyze_record(
            model,
            tokenizer,
            record,
            token_info,
            chunk_size=args.chunk_size,
        )
        if analyzed["classification"]["selected_intermediate"] == "Fx":
            fx_records.append(analyzed)
        else:
            gx_records.append(analyzed)
        if index % 10 == 0 or index == len(eligible):
            print(f"Analyzed {index}/{len(eligible)}")

    if len(fx_records) + len(gx_records) != len(eligible):
        raise RuntimeError("path outputs do not partition the analyzed records")
    write_jsonl(args.fx_output, fx_records)
    write_jsonl(args.gx_output, gx_records)
    print(f"Wrote {len(fx_records)} antonym-then-translate records to {args.fx_output}")
    print(f"Wrote {len(gx_records)} translate-then-antonym records to {args.gx_output}")


if __name__ == "__main__":
    main()
