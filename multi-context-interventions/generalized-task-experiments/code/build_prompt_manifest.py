"""Build reproducible multi-context prompts for any registered paper task.

This is the first executable stage of the generalized experiment pipeline. It
loads one task from the pinned Khandelwal--Pavlick dataset and writes one JSONL
record per query-context instance. It does not load OLMo, evaluate correctness,
calculate either lens, or run interventions.

The sampling method matches the verified earlier implementation: the task rows
are shuffled with ``seed`` and each context variant owns one continuous random
stream that advances across queries.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any, Iterable, Mapping

from tasks import DATASET_COMMIT, DATASET_ID, TASKS, TaskExample, TaskSpec, get_task_spec


REFERENCE_CODE_COMMIT = "f12cef400ff946ab09cee988817daea939436698"
DEFAULT_CONTEXTS_PER_QUERY = 10
DEFAULT_ICL_EXAMPLES = 10
DEFAULT_SEED = 0
PROJECT_DIR = Path(__file__).resolve().parent.parent


def parse_args() -> argparse.Namespace:
    """Parse one task and its prompt-sampling settings."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, choices=sorted(TASKS))
    parser.add_argument("--all-queries", action="store_true")
    parser.add_argument("--query-index", action="append", type=int, default=[])
    parser.add_argument(
        "--contexts-per-query", type=int, default=DEFAULT_CONTEXTS_PER_QUERY
    )
    parser.add_argument("--icl-examples", type=int, default=DEFAULT_ICL_EXAMPLES)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--summary-output", type=Path)
    return parser.parse_args()


def load_dataset_rows() -> Iterable[Mapping[str, Any]]:
    """Load the full pinned Khandelwal--Pavlick dataset."""

    from datasets import load_dataset

    return load_dataset(DATASET_ID, split="train", revision=DATASET_COMMIT)


def load_examples(spec: TaskSpec) -> list[TaskExample]:
    """Load and validate all rows for one registered task."""

    return spec.select_examples(load_dataset_rows())


def select_query_indices(
    num_examples: int,
    *,
    query_indices: Iterable[int],
    all_queries: bool,
) -> list[int]:
    """Resolve the requested task-local query indices."""

    selected = list(dict.fromkeys(query_indices))
    if all_queries:
        if selected:
            raise ValueError("--all-queries cannot be combined with --query-index")
        return list(range(num_examples))
    if not selected:
        raise ValueError("use --all-queries or provide at least one --query-index")
    for index in selected:
        if not 0 <= index < num_examples:
            raise ValueError(f"query index {index} is outside [0, {num_examples})")
    return selected


def sample_context(
    query: TaskExample,
    candidates: list[TaskExample],
    *,
    icl_examples: int,
    rng: random.Random,
) -> list[TaskExample]:
    """Sample distinct demonstrations with no x/Fx/GFx query overlap."""

    if icl_examples <= 0:
        raise ValueError("icl_examples must be positive")
    context = []
    attempts = 0
    max_attempts = max(1_000, 100 * len(candidates))
    while len(context) < icl_examples:
        attempts += 1
        if attempts > max_attempts:
            raise RuntimeError("could not sample enough non-overlapping examples")
        candidate = rng.choice(candidates)
        if (
            candidate != query
            and candidate not in context
            and not candidate.overlaps(query)
        ):
            context.append(candidate)
    return context


def build_prompt_manifest(
    spec: TaskSpec,
    examples: list[TaskExample],
    query_indices: list[int],
    *,
    contexts_per_query: int = DEFAULT_CONTEXTS_PER_QUERY,
    icl_examples: int = DEFAULT_ICL_EXAMPLES,
    seed: int = DEFAULT_SEED,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Create reproducible query-context records for one task."""

    if contexts_per_query <= 0:
        raise ValueError("contexts_per_query must be positive")
    candidates = examples.copy()
    random.Random(seed).shuffle(candidates)
    context_rngs = [
        random.Random(seed + variant) for variant in range(contexts_per_query)
    ]
    records = []
    for query_index in query_indices:
        if not 0 <= query_index < len(examples):
            raise ValueError(f"query index {query_index} is outside [0, {len(examples)})")
        query = examples[query_index]
        for variant, rng in enumerate(context_rngs):
            context = sample_context(
                query, candidates, icl_examples=icl_examples, rng=rng
            )
            records.append(
                {
                    "prompt_instance_id": (
                        f"{spec.dataset_task}__query_{query_index:05d}"
                        f"_context_{variant:02d}"
                    ),
                    "task": spec.dataset_task,
                    "query_index": query_index,
                    "context_variant": variant,
                    "query": query.as_dict(),
                    "context": [example.as_dict() for example in context],
                    "prompt": spec.render_prompt(context, query),
                }
            )
    summary = {
        "dataset": DATASET_ID,
        "dataset_commit": DATASET_COMMIT,
        "reference_code_commit": REFERENCE_CODE_COMMIT,
        "task": spec.dataset_task,
        "base_seed": seed,
        "sampling_method": "continuous_rng_stream_per_context_variant",
        "contexts_per_query": contexts_per_query,
        "num_queries": len(query_indices),
        "num_prompt_instances": len(records),
        "query_indices": query_indices,
    }
    return records, summary


def write_jsonl(path: Path, records: Iterable[Mapping[str, Any]]) -> None:
    """Write records as one JSON object per line."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    args = parse_args()
    spec = get_task_spec(args.task)
    examples = load_examples(spec)
    query_indices = select_query_indices(
        len(examples), query_indices=args.query_index, all_queries=args.all_queries
    )
    records, summary = build_prompt_manifest(
        spec,
        examples,
        query_indices,
        contexts_per_query=args.contexts_per_query,
        icl_examples=args.icl_examples,
        seed=args.seed,
    )
    result_directory = PROJECT_DIR / "results" / spec.dataset_task
    output = args.output or result_directory / "prompt_manifest.jsonl"
    summary_output = args.summary_output or result_directory / "prompt_manifest_summary.json"
    write_jsonl(output, records)
    summary_output.parent.mkdir(parents=True, exist_ok=True)
    summary_output.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))
    print(f"Wrote {output}")
    print(f"Wrote {summary_output}")


if __name__ == "__main__":
    main()
