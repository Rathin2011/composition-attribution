"""Reproduce baseline answers and probabilities for saved compositional queries.

Input:
    The saved compositional-query JSONL, the pinned local OLMo 3 cache, and
    explicit output paths.
Output:
    One compact JSONL record per query and an incrementally updated JSON
    summary. No activations are edited in this experiment.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

from country_capital.config import (
    MODEL_COMMIT,
    MODEL_DTYPE,
    MODEL_ID,
    MODEL_REVISION,
)
from country_capital.data import load_compositional_queries, tokenize_queries
from country_capital.model import load_model_and_tokenizer
from country_capital.runner import MAX_NEW_TOKENS, run_query


def parse_args() -> argparse.Namespace:
    """Read explicit input, model-cache, and output paths from the command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--expected-queries", type=int, default=370)
    parser.add_argument("--max-new-tokens", type=int, default=MAX_NEW_TOKENS)
    return parser.parse_args()


def make_record(query: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    """Combine query identity with compact baseline probability measurements."""
    token_logprobs = result["completion_token_logprobs"]
    baseline = {
        "prediction": result["prediction"],
        "label": result["label"],
        "full_answer_correct": result["full_answer_correct"],
        "completion_logprob": result["completion_logprob"],
        "completion_probability": math.exp(result["completion_logprob"]),
        "completion_token_logprobs": token_logprobs,
        "completion_token_probabilities": [
            math.exp(value) for value in token_logprobs
        ],
        "greedy_next_token_id": result["greedy_next_token_id"],
        "correct_first_token_top1": result["correct_first_token_top1"],
        "generated_token_ids": result["generated_token_ids"],
    }
    return {
        "evaluation_index": query["evaluation_index"],
        "landmark": query["landmark"],
        "country": query["country"],
        "capital": query["capital"],
        "answer_token_count": len(query["answer_ids"]),
        "original_prediction": query["original_prediction"],
        "fresh_matches_saved_prediction": (
            result["prediction"] == query["original_prediction"]
        ),
        "baseline": baseline,
    }


def summarize(
    records: list[dict[str, Any]],
    *,
    expected_queries: int,
    input_path: Path,
    input_sha256: str,
) -> dict[str, Any]:
    """Return a compact, valid summary even while the run is incomplete."""
    completed = len(records)
    correct = sum(record["baseline"]["full_answer_correct"] for record in records)
    matching = sum(record["fresh_matches_saved_prediction"] for record in records)
    probabilities = [
        record["baseline"]["completion_probability"] for record in records
    ]
    logprobabilities = [
        record["baseline"]["completion_logprob"] for record in records
    ]
    return {
        "expected_queries": expected_queries,
        "completed_queries": completed,
        "complete": completed == expected_queries,
        "model": MODEL_ID,
        "model_commit": MODEL_COMMIT,
        "stage_one_revision": MODEL_REVISION,
        "dtype": MODEL_DTYPE,
        "input": str(input_path),
        "input_sha256": input_sha256,
        "fresh_baseline_correct": correct,
        "fresh_baseline_accuracy": correct / completed if completed else None,
        "fresh_matches_saved_prediction": matching,
        "multi_token_answers": sum(
            record["answer_token_count"] > 1 for record in records
        ),
        "mean_completion_logprob": (
            sum(logprobabilities) / completed if completed else None
        ),
        "mean_completion_probability": (
            sum(probabilities) / completed if completed else None
        ),
    }


def write_summary(path: Path, summary: dict[str, Any]) -> None:
    """Replace the current incomplete/complete summary."""
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")


def main() -> None:
    """Load the pinned model, run every unedited query, and checkpoint outputs."""
    args = parse_args()
    if args.expected_queries < 1:
        raise ValueError("expected-queries must be positive")
    if args.max_new_tokens < 1:
        raise ValueError("max-new-tokens must be positive")
    if args.output.resolve() == args.summary.resolve():
        raise ValueError("detailed output and summary paths must differ")
    for path in (args.output, args.summary):
        if path.exists():
            raise FileExistsError(f"refusing to overwrite existing output: {path}")
        path.parent.mkdir(parents=True, exist_ok=True)

    queries = load_compositional_queries(
        args.input, expected_count=args.expected_queries
    )
    input_sha256 = hashlib.sha256(args.input.read_bytes()).hexdigest()
    model, tokenizer = load_model_and_tokenizer(args.cache_dir)
    queries = tokenize_queries(queries, tokenizer)
    records: list[dict[str, Any]] = []

    write_summary(
        args.summary,
        summarize(
            records,
            expected_queries=args.expected_queries,
            input_path=args.input,
            input_sha256=input_sha256,
        ),
    )
    with args.output.open("x") as output_stream:
        for offset, query in enumerate(queries, start=1):
            result = run_query(
                model,
                tokenizer,
                query,
                activation_editor=None,
                max_new_tokens=args.max_new_tokens,
            )
            if result["editor_audit"]["editor_active"]:
                raise RuntimeError("baseline unexpectedly used an activation editor")

            record = make_record(query, result)
            output_stream.write(json.dumps(record, ensure_ascii=False) + "\n")
            output_stream.flush()
            records.append(record)
            write_summary(
                args.summary,
                summarize(
                    records,
                    expected_queries=args.expected_queries,
                    input_path=args.input,
                    input_sha256=input_sha256,
                ),
            )
            print(
                f"[{offset}/{len(queries)}] {query['landmark']}: "
                f"prediction={result['prediction']!r}, "
                f"correct={result['full_answer_correct']}, "
                f"logP={result['completion_logprob']:.6f}",
                flush=True,
            )

    print(
        f"Saved {len(records)} baseline records to {args.output}; "
        f"summary: {args.summary}",
        flush=True,
    )


if __name__ == "__main__":
    main()
