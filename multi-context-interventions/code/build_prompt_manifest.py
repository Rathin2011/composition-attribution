"""Create reproducible multi-context prompts for landmark queries.

The prompt format, overlap rule, seeded shuffle, and context sampling mirror the
verified Khandelwal--Pavlick evaluation port.  This file adds only one new
dimension: each selected query receives multiple independently sampled
contexts rather than a single context.

This block does not load OLMo, calculate lens scores, or run interventions.
"""

from __future__ import annotations

import argparse
import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


DATASET_ID = "apoorvkh/composing-functions"
DATASET_COMMIT = "5b7b70743ff849eae3875dc0c22d5443066b33e9"
TASK_NAME = "landmark-country-capital"
EXPECTED_DATASET_SIZE = 1_385
REFERENCE_CODE_COMMIT = "f12cef400ff946ab09cee988817daea939436698"
DEFAULT_CONTEXTS_PER_QUERY = 10
DEFAULT_ICL_EXAMPLES = 10
DEFAULT_SEED = 0

PROJECT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = PROJECT_DIR / "results" / "prompt_manifest.jsonl"
DEFAULT_SUMMARY = PROJECT_DIR / "results" / "prompt_manifest_summary.json"


@dataclass(frozen=True)
class Example:
    """One landmark-country-capital dataset row."""

    x: str
    Fx: str
    GFx: str

    def overlaps(self, other: "Example") -> bool:
        """Whether any task value is shared with another row."""

        return bool(set(asdict(self).values()) & set(asdict(other).values()))


@dataclass(frozen=True)
class InContextQuery:
    """One query paired with one ordered set of demonstrations."""

    context: tuple[Example, ...]
    query: Example

    def composition_prompt(self) -> str:
        """Render the authors' Q/A prompt for landmark-to-capital composition."""

        demonstrations = "".join(
            f"Q: {example.x}\nA: {example.GFx}\n\n" for example in self.context
        )
        return f"{demonstrations}Q: {self.query.x}\nA:"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--landmark",
        action="append",
        default=[],
        help="Exact landmark value to include; may be supplied more than once.",
    )
    parser.add_argument(
        "--query-index",
        action="append",
        type=int,
        default=[],
        help="Zero-based task-local dataset index; may be supplied more than once.",
    )
    parser.add_argument(
        "--all-queries",
        action="store_true",
        help="Generate contexts for all landmark-country-capital dataset rows.",
    )
    parser.add_argument(
        "--contexts-per-query", type=int, default=DEFAULT_CONTEXTS_PER_QUERY
    )
    parser.add_argument("--icl-examples", type=int, default=DEFAULT_ICL_EXAMPLES)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY)
    return parser.parse_args()


def load_examples() -> list[Example]:
    """Load the pinned paper dataset and select the landmark task."""

    from datasets import load_dataset

    dataset = load_dataset(DATASET_ID, split="train", revision=DATASET_COMMIT)
    examples = [
        Example(x=row["x"], Fx=row["Fx"], GFx=row["GFx"])
        for row in dataset
        if row["task"] == TASK_NAME
    ]
    if len(examples) != EXPECTED_DATASET_SIZE:
        raise RuntimeError(
            f"Expected {EXPECTED_DATASET_SIZE} {TASK_NAME} rows, got {len(examples)}"
        )
    return examples


def select_query_indices(
    examples: list[Example],
    *,
    landmarks: Iterable[str],
    query_indices: Iterable[int],
    all_queries: bool = False,
) -> list[int]:
    """Resolve requested landmarks and indices to unique task-local indices."""

    landmarks = list(landmarks)
    query_indices = list(query_indices)
    if all_queries:
        if landmarks or query_indices:
            raise ValueError("--all-queries cannot be combined with individual queries")
        return list(range(len(examples)))

    selected = []
    for index in query_indices:
        if not 0 <= index < len(examples):
            raise ValueError(f"query index {index} is outside [0, {len(examples)})")
        selected.append(index)

    index_by_landmark: dict[str, int] = {}
    for index, example in enumerate(examples):
        if example.x in index_by_landmark:
            raise ValueError(f"duplicate landmark in dataset: {example.x!r}")
        index_by_landmark[example.x] = index
    for landmark in landmarks:
        if landmark not in index_by_landmark:
            raise ValueError(f"unknown landmark: {landmark!r}")
        selected.append(index_by_landmark[landmark])

    selected = list(dict.fromkeys(selected))
    if not selected:
        raise ValueError("select at least one query with --landmark or --query-index")
    return selected


def shuffled_examples(examples: list[Example], seed: int) -> list[Example]:
    """Apply the authors' deterministic shuffle before context sampling."""

    shuffled = examples.copy()
    random.Random(seed).shuffle(shuffled)
    return shuffled


def sample_context(
    query: Example,
    candidate_pool: list[Example],
    *,
    icl_examples: int,
    seed: int,
) -> tuple[Example, ...]:
    """Sample one valid ordered demonstration context for a query."""

    if icl_examples <= 0:
        raise ValueError("icl_examples must be positive")
    rng = random.Random(seed)
    context: list[Example] = []
    attempts = 0
    max_attempts = max(1_000, 100 * len(candidate_pool))
    while len(context) < icl_examples:
        attempts += 1
        if attempts > max_attempts:
            raise RuntimeError("could not sample enough non-overlapping examples")
        example = rng.choice(candidate_pool)
        if example not in context and example != query and not example.overlaps(query):
            context.append(example)
    return tuple(context)


def build_prompt_manifest(
    examples: list[Example],
    query_indices: list[int],
    *,
    contexts_per_query: int = DEFAULT_CONTEXTS_PER_QUERY,
    icl_examples: int = DEFAULT_ICL_EXAMPLES,
    seed: int = DEFAULT_SEED,
) -> tuple[list[dict], dict]:
    """Create multiple independently sampled prompt instances per query."""

    if contexts_per_query <= 0:
        raise ValueError("contexts_per_query must be positive")
    candidate_pool = shuffled_examples(examples, seed)
    records = []

    for query_index in query_indices:
        if not 0 <= query_index < len(examples):
            raise ValueError(f"query index {query_index} is outside [0, {len(examples)})")
        query = examples[query_index]
        for context_variant in range(contexts_per_query):
            context_seed = seed + context_variant
            context = sample_context(
                query,
                candidate_pool,
                icl_examples=icl_examples,
                seed=context_seed,
            )
            in_context_query = InContextQuery(context=context, query=query)
            records.append(
                {
                    "prompt_instance_id": (
                        f"query_{query_index:04d}_context_{context_variant:02d}"
                    ),
                    "task": TASK_NAME,
                    "query_index": query_index,
                    "context_variant": context_variant,
                    "context_seed": context_seed,
                    "icl_examples": icl_examples,
                    "query": asdict(query),
                    "context": [asdict(example) for example in context],
                    "prompt": in_context_query.composition_prompt(),
                }
            )

    summary = {
        "dataset": DATASET_ID,
        "dataset_commit": DATASET_COMMIT,
        "reference_code_commit": REFERENCE_CODE_COMMIT,
        "task": TASK_NAME,
        "base_seed": seed,
        "contexts_per_query": contexts_per_query,
        "icl_examples_per_context": icl_examples,
        "num_queries": len(query_indices),
        "num_prompt_instances": len(records),
        "query_indices": query_indices,
        "landmarks": [examples[index].x for index in query_indices],
    }
    return records, summary


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records)
    )


def main() -> None:
    args = parse_args()
    examples = load_examples()
    query_indices = select_query_indices(
        examples,
        landmarks=args.landmark,
        query_indices=args.query_index,
        all_queries=args.all_queries,
    )
    records, summary = build_prompt_manifest(
        examples,
        query_indices,
        contexts_per_query=args.contexts_per_query,
        icl_examples=args.icl_examples,
        seed=args.seed,
    )
    write_jsonl(args.output, records)
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print(f"Wrote {args.output}")
    print(f"Wrote {args.summary_output}")


if __name__ == "__main__":
    main()
