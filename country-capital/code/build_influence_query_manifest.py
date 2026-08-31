"""Export the existing 32 strict landmark composition-shortcut pairs to JSONL."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


TASK_NAME = "landmark_country_capital"
COMPOSITION_GROUP = "composition"
SHORTCUT_GROUP = "shortcut"
SOURCE_COMPOSITION_GROUP = "compositional"
SOURCE_SHORTCUT_GROUP = "shortcut_candidate"
EXPECTED_PAIRS = 32
EXPECTED_QUERIES = 64
EXPECTED_CONTEXT_EXAMPLES = 10

PROJECT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_DIR / "results"
DEFAULT_COMPOSITIONAL_INPUT = (
    RESULTS_DIR / "olmo3_stage1_landmark_country_capital.compositional.jsonl"
)
DEFAULT_SHORTCUT_INPUT = (
    RESULTS_DIR / "olmo3_stage1_landmark_country_capital.shortcut_candidates.jsonl"
)
DEFAULT_MATCHED_REPORT = RESULTS_DIR / "markdown/matched_compositional_shortcut_pairs.md"
DEFAULT_OUTPUT = RESULTS_DIR / "influence/strict_matched_queries.jsonl"
DEFAULT_SUMMARY_OUTPUT = RESULTS_DIR / "influence/strict_matched_queries_summary.json"

QUERY_LINE = re.compile(r"^- \*\*(Compositional|Shortcut) query (\d+) — Context:")


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_frozen_pairs(path: Path) -> list[tuple[int, int]]:
    """Read the ordered evaluation indices shown in the reviewed Markdown report."""

    selected = []
    for line in path.read_text().splitlines():
        match = QUERY_LINE.match(line)
        if match:
            selected.append((match.group(1), int(match.group(2))))

    if len(selected) != EXPECTED_QUERIES:
        raise ValueError(
            f"expected {EXPECTED_QUERIES} selected queries in {path}, found {len(selected)}"
        )

    pairs = []
    for offset in range(0, len(selected), 2):
        composition, shortcut = selected[offset : offset + 2]
        if composition[0] != "Compositional" or shortcut[0] != "Shortcut":
            raise ValueError(
                f"Markdown pair {offset // 2} is not ordered compositional then shortcut"
            )
        pairs.append((composition[1], shortcut[1]))

    if len(pairs) != EXPECTED_PAIRS:
        raise ValueError(f"expected {EXPECTED_PAIRS} Markdown pairs, found {len(pairs)}")
    if len({index for pair in pairs for index in pair}) != EXPECTED_QUERIES:
        raise ValueError("Markdown report reuses an evaluation index")
    return pairs


def index_records(records: list[dict], *, expected_group: str) -> dict[int, dict]:
    indexed = {}
    for record in records:
        evaluation_index = record.get("evaluation_index")
        if not isinstance(evaluation_index, int):
            raise ValueError("source record lacks an integer evaluation_index")
        if evaluation_index in indexed:
            raise ValueError(f"duplicate evaluation index {evaluation_index}")
        if record.get("classification", {}).get("group") != expected_group:
            raise ValueError(
                f"evaluation {evaluation_index} is not labeled {expected_group}"
            )
        indexed[evaluation_index] = record
    return indexed


def validate_source_record(record: dict, *, source_group: str) -> None:
    evaluation_index = record["evaluation_index"]
    prediction = record.get("prediction", {})
    query = record.get("query", {})
    classification = record.get("classification", {})

    if prediction.get("pred") != prediction.get("label"):
        raise ValueError(f"evaluation {evaluation_index} was not answered correctly")
    if prediction.get("label", "").strip() != query.get("GFx"):
        raise ValueError(f"evaluation {evaluation_index} label is not the correct capital")
    if len(record.get("context", [])) != EXPECTED_CONTEXT_EXAMPLES:
        raise ValueError(
            f"evaluation {evaluation_index} does not have {EXPECTED_CONTEXT_EXAMPLES} examples"
        )
    expected_suffix = f"Q: {query.get('x')}\nA:"
    if not prediction.get("prompt", "").endswith(expected_suffix):
        raise ValueError(f"evaluation {evaluation_index} prompt has the wrong final query")

    peak_rr = classification.get("peak_reciprocal_rank")
    composition_threshold = classification.get("composition_rr_threshold")
    shortcut_threshold = classification.get("shortcut_rr_threshold")
    if not all(isinstance(value, (int, float)) for value in (
        peak_rr,
        composition_threshold,
        shortcut_threshold,
    )):
        raise ValueError(f"evaluation {evaluation_index} lacks numeric RR thresholds")
    if source_group == SOURCE_COMPOSITION_GROUP and peak_rr < composition_threshold:
        raise ValueError(f"evaluation {evaluation_index} is below the composition threshold")
    if source_group == SOURCE_SHORTCUT_GROUP and peak_rr > shortcut_threshold:
        raise ValueError(f"evaluation {evaluation_index} is above the shortcut threshold")


def manifest_record(
    source: dict,
    *,
    query_index: int,
    pair_index: int,
    group: str,
) -> dict:
    classification = source["classification"]
    query = source["query"]
    prediction = source["prediction"]
    return {
        "task": TASK_NAME,
        "query_index": query_index,
        "pair_index": pair_index,
        "group": group,
        "evaluation_index": source["evaluation_index"],
        "dataset_index": source["dataset_index"],
        "model": source["model"],
        "stage_one_revision": source["stage_one_revision"],
        "model_commit": source["model_commit"],
        "landmark": query["x"],
        "country": query["Fx"],
        "capital": query["GFx"],
        "context": source["context"],
        "prompt": prediction["prompt"],
        "completion": prediction["label"],
        "model_prediction": prediction["pred"],
        "intermediate_node": classification["intermediate"],
        "intermediate_peak_reciprocal_rank": classification["peak_reciprocal_rank"],
        "intermediate_best_vocabulary_rank": classification["best_vocabulary_rank"],
        "intermediate_peak_layers": classification["peak_layers"],
        "composition_rr_threshold": classification["composition_rr_threshold"],
        "shortcut_rr_threshold": classification["shortcut_rr_threshold"],
    }


def build_manifest(
    compositional_records: list[dict],
    shortcut_records: list[dict],
    frozen_pairs: list[tuple[int, int]],
) -> list[dict]:
    compositional = index_records(
        compositional_records, expected_group=SOURCE_COMPOSITION_GROUP
    )
    shortcuts = index_records(shortcut_records, expected_group=SOURCE_SHORTCUT_GROUP)
    output = []
    for pair_index, (composition_index, shortcut_index) in enumerate(frozen_pairs):
        if composition_index not in compositional:
            raise ValueError(
                f"Markdown compositional query {composition_index} is absent from its JSONL"
            )
        if shortcut_index not in shortcuts:
            raise ValueError(
                f"Markdown shortcut query {shortcut_index} is absent from its JSONL"
            )
        composition = compositional[composition_index]
        shortcut = shortcuts[shortcut_index]
        validate_source_record(composition, source_group=SOURCE_COMPOSITION_GROUP)
        validate_source_record(shortcut, source_group=SOURCE_SHORTCUT_GROUP)
        composition_key = (composition["query"]["Fx"], composition["query"]["GFx"])
        shortcut_key = (shortcut["query"]["Fx"], shortcut["query"]["GFx"])
        if composition_key != shortcut_key:
            raise ValueError(
                f"pair {pair_index} does not share country and capital: "
                f"{composition_key} != {shortcut_key}"
            )
        output.append(
            manifest_record(
                composition,
                query_index=len(output),
                pair_index=pair_index,
                group=COMPOSITION_GROUP,
            )
        )
        output.append(
            manifest_record(
                shortcut,
                query_index=len(output),
                pair_index=pair_index,
                group=SHORTCUT_GROUP,
            )
        )
    return output


def validate_manifest(records: list[dict]) -> dict:
    if len(records) != EXPECTED_QUERIES:
        raise ValueError(f"expected {EXPECTED_QUERIES} manifest queries, found {len(records)}")
    if [record["query_index"] for record in records] != list(range(EXPECTED_QUERIES)):
        raise ValueError("manifest query indices are not contiguous")
    if len({record["evaluation_index"] for record in records}) != EXPECTED_QUERIES:
        raise ValueError("manifest evaluation indices are not unique")

    group_counts = Counter(record["group"] for record in records)
    expected_counts = Counter({COMPOSITION_GROUP: EXPECTED_PAIRS, SHORTCUT_GROUP: EXPECTED_PAIRS})
    if group_counts != expected_counts:
        raise ValueError(f"unexpected manifest group counts: {dict(group_counts)}")

    pair_country_counts = Counter()
    for pair_index in range(EXPECTED_PAIRS):
        pair = [record for record in records if record["pair_index"] == pair_index]
        if len(pair) != 2 or {record["group"] for record in pair} != {
            COMPOSITION_GROUP,
            SHORTCUT_GROUP,
        }:
            raise ValueError(f"manifest pair {pair_index} does not contain both groups")
        keys = {(record["country"], record["capital"]) for record in pair}
        if len(keys) != 1:
            raise ValueError(f"manifest pair {pair_index} is not fact matched")
        pair_country_counts[pair[0]["country"]] += 1

    return {
        "task": TASK_NAME,
        "queries": len(records),
        "matched_pairs": EXPECTED_PAIRS,
        "group_counts": dict(sorted(group_counts.items())),
        "matched_pairs_per_country": dict(sorted(pair_country_counts.items())),
        "selection": "frozen evaluation indices from reviewed Markdown report",
    }


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records)
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compositional-input", type=Path, default=DEFAULT_COMPOSITIONAL_INPUT)
    parser.add_argument("--shortcut-input", type=Path, default=DEFAULT_SHORTCUT_INPUT)
    parser.add_argument("--matched-report", type=Path, default=DEFAULT_MATCHED_REPORT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    frozen_pairs = read_frozen_pairs(args.matched_report)
    records = build_manifest(
        read_jsonl(args.compositional_input),
        read_jsonl(args.shortcut_input),
        frozen_pairs,
    )
    summary = validate_manifest(records)
    write_jsonl(args.output, records)
    summary.update(
        {
            "inputs": {
                "compositional": str(args.compositional_input),
                "shortcut": str(args.shortcut_input),
                "matched_report": str(args.matched_report),
            },
            "input_sha256": {
                "compositional": sha256_file(args.compositional_input),
                "shortcut": sha256_file(args.shortcut_input),
                "matched_report": sha256_file(args.matched_report),
            },
            "output": str(args.output),
            "output_sha256": sha256_file(args.output),
        }
    )
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
