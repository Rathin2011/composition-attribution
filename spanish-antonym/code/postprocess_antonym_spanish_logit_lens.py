"""Split Spanish-antonym logit-lens records into evidence groups and paths."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from composition_evidence import COMPOSITION_RR_THRESHOLD, SHORTCUT_RR_THRESHOLD


EXPECTED_CORRECT = 687
EXPECTED_ELIGIBLE = 519

PROJECT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_DIR / "results"
PREFIX = "olmo3_stage1_antonym_spanish"

DEFAULT_FX_INPUT = RESULTS_DIR / f"{PREFIX}_path_fx.jsonl"
DEFAULT_GX_INPUT = RESULTS_DIR / f"{PREFIX}_path_gx.jsonl"
DEFAULT_COMPOSITIONAL_OUTPUT = RESULTS_DIR / f"{PREFIX}.compositional.jsonl"
DEFAULT_AMBIGUOUS_OUTPUT = RESULTS_DIR / f"{PREFIX}.ambiguous.jsonl"
DEFAULT_SHORTCUT_OUTPUT = RESULTS_DIR / f"{PREFIX}.shortcut_candidates.jsonl"
DEFAULT_SUMMARY_OUTPUT = RESULTS_DIR / f"{PREFIX}.logit_lens_summary.json"
DEFAULT_COMPOSITIONAL_FX_OUTPUT = RESULTS_DIR / f"{PREFIX}.compositional_path_fx.jsonl"
DEFAULT_COMPOSITIONAL_GX_OUTPUT = RESULTS_DIR / f"{PREFIX}.compositional_path_gx.jsonl"

GROUPS = ("compositional", "ambiguous", "shortcut_candidate")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fx-input", type=Path, default=DEFAULT_FX_INPUT)
    parser.add_argument("--gx-input", type=Path, default=DEFAULT_GX_INPUT)
    parser.add_argument("--compositional-output", type=Path, default=DEFAULT_COMPOSITIONAL_OUTPUT)
    parser.add_argument("--ambiguous-output", type=Path, default=DEFAULT_AMBIGUOUS_OUTPUT)
    parser.add_argument("--shortcut-output", type=Path, default=DEFAULT_SHORTCUT_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    parser.add_argument("--compositional-fx-output", type=Path, default=DEFAULT_COMPOSITIONAL_FX_OUTPUT)
    parser.add_argument("--compositional-gx-output", type=Path, default=DEFAULT_COMPOSITIONAL_GX_OUTPUT)
    parser.add_argument("--expected-correct", type=int, default=EXPECTED_CORRECT)
    parser.add_argument("--expected-eligible", type=int, default=EXPECTED_ELIGIBLE)
    return parser.parse_args()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records))


def validate_path_records(records: list[dict], expected_intermediate: str) -> None:
    for record in records:
        classification = record.get("classification", {})
        if classification.get("selected_intermediate") != expected_intermediate:
            raise ValueError(
                f"Record {record.get('evaluation_index')} is in the {expected_intermediate} "
                "file but has a different selected intermediate"
            )
        if classification.get("group") not in GROUPS:
            raise ValueError(
                f"Record {record.get('evaluation_index')} has an unknown evidence group"
            )


def partition_records(
    fx_records: list[dict], gx_records: list[dict]
) -> tuple[list[dict], list[dict], list[dict], list[dict], list[dict]]:
    validate_path_records(fx_records, "Fx")
    validate_path_records(gx_records, "Gx")
    records = fx_records + gx_records

    evaluation_indices = [record.get("evaluation_index") for record in records]
    if None in evaluation_indices or len(evaluation_indices) != len(set(evaluation_indices)):
        raise ValueError("Path inputs contain missing or duplicate evaluation indices")

    compositional = [
        record for record in records if record["classification"]["group"] == "compositional"
    ]
    ambiguous = [
        record for record in records if record["classification"]["group"] == "ambiguous"
    ]
    shortcut = [
        record
        for record in records
        if record["classification"]["group"] == "shortcut_candidate"
    ]
    compositional_fx = [
        record for record in fx_records if record["classification"]["group"] == "compositional"
    ]
    compositional_gx = [
        record for record in gx_records if record["classification"]["group"] == "compositional"
    ]
    return compositional, ambiguous, shortcut, compositional_fx, compositional_gx


def build_summary(
    compositional: list[dict],
    ambiguous: list[dict],
    shortcut: list[dict],
    compositional_fx: list[dict],
    compositional_gx: list[dict],
    *,
    raw_correct: int,
    paper_token_eligible: int,
) -> dict:
    analyzed = len(compositional) + len(ambiguous) + len(shortcut)
    if raw_correct < paper_token_eligible:
        raise ValueError("Raw correct count cannot be smaller than eligible count")
    if analyzed != paper_token_eligible:
        raise ValueError(
            f"Expected {paper_token_eligible} eligible records, found {analyzed}"
        )
    if len(compositional_fx) + len(compositional_gx) != len(compositional):
        raise ValueError("Compositional path files do not partition compositional records")

    return {
        "raw_correct_compositions": raw_correct,
        "paper_token_eligible": paper_token_eligible,
        "paper_token_excluded": raw_correct - paper_token_eligible,
        "analyzed_records": analyzed,
        "composition_rr_threshold": COMPOSITION_RR_THRESHOLD,
        "shortcut_rr_threshold": SHORTCUT_RR_THRESHOLD,
        "num_compositional": len(compositional),
        "num_ambiguous": len(ambiguous),
        "num_shortcut_candidates": len(shortcut),
        "num_compositional_antonym_then_translate": len(compositional_fx),
        "num_compositional_translate_then_antonym": len(compositional_gx),
        "p_compositional_given_correct_eligible": (
            len(compositional) / analyzed if analyzed else None
        ),
    }


def main() -> None:
    args = parse_args()
    fx_records = read_jsonl(args.fx_input)
    gx_records = read_jsonl(args.gx_input)
    if len(fx_records) + len(gx_records) != args.expected_eligible:
        raise RuntimeError(
            f"Expected {args.expected_eligible} paper-filtered records, "
            f"got {len(fx_records) + len(gx_records)}"
        )

    compositional, ambiguous, shortcut, compositional_fx, compositional_gx = (
        partition_records(fx_records, gx_records)
    )
    summary = build_summary(
        compositional,
        ambiguous,
        shortcut,
        compositional_fx,
        compositional_gx,
        raw_correct=args.expected_correct,
        paper_token_eligible=args.expected_eligible,
    )

    write_jsonl(args.compositional_output, compositional)
    write_jsonl(args.ambiguous_output, ambiguous)
    write_jsonl(args.shortcut_output, shortcut)
    write_jsonl(args.compositional_fx_output, compositional_fx)
    write_jsonl(args.compositional_gx_output, compositional_gx)
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
