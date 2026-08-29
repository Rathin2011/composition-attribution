"""Evaluate stage-one OLMo 3 on Khandelwal--Pavlick antonym--Spanish.

Prompt construction, context sampling, mapping, generation, and scoring are
adapted from the authors' MIT-licensed ``composing-functions`` repository at
commit f12cef400ff946ab09cee988817daea939436698.
"""

from __future__ import annotations

import argparse
import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import mean
from typing import Literal

from load_olmo3_stage1 import MODEL_ID, STAGE_ONE_COMMIT, STAGE_ONE_REVISION

REFERENCE_CODE_COMMIT = "f12cef400ff946ab09cee988817daea939436698"
DATASET_ID = "apoorvkh/composing-functions"
DATASET_COMMIT = "5b7b70743ff849eae3875dc0c22d5443066b33e9"
TASK_NAME = "antonym-spanish"
EXPECTED_DATASET_SIZE = 2_398
DEFAULT_SEED = 0
DEFAULT_ICL_EXAMPLES = 10
DEFAULT_NUM_QUERIES = EXPECTED_DATASET_SIZE
MAX_NEW_TOKENS = 20
STOP_SEQUENCE = "\n\n"
PROJECT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = PROJECT_DIR / "results" / "olmo3_stage1_antonym_spanish_all.json"
DEFAULT_CORRECT_OUTPUT = (
    PROJECT_DIR / "results" / "olmo3_stage1_antonym_spanish_all.correct.jsonl"
)

Node = Literal["x", "Fx", "Gx", "GFx", "FGx"]


@dataclass(frozen=True)
class Example:
    x: str
    Fx: str
    Gx: str
    GFx: str
    FGx: str

    def get(self, node: Node, *, leading_space: bool = False) -> str:
        value = getattr(self, node)
        return f" {value}" if leading_space else value

    def overlaps(self, other: "Example") -> bool:
        return bool(set(asdict(self).values()) & set(asdict(other).values()))


@dataclass(frozen=True)
class InContextQuery:
    context: tuple[Example, ...]
    query: Example

    def prompt(self, query_type: Node, pred_type: Node) -> str:
        text = "".join(
            f"Q: {example.get(query_type)}\nA: {example.get(pred_type)}\n\n"
            for example in self.context
        )
        return f"{text}Q: {self.query.get(query_type)}\nA:"


@dataclass(frozen=True)
class Prediction:
    prompt: str
    pred: str
    label: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--num-queries", type=int, default=DEFAULT_NUM_QUERIES)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--icl-examples", type=int, default=DEFAULT_ICL_EXAMPLES)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
    )
    parser.add_argument(
        "--correct-output",
        type=Path,
        default=DEFAULT_CORRECT_OUTPUT,
    )
    return parser.parse_args()


def load_examples() -> list[Example]:
    from datasets import load_dataset

    dataset = load_dataset(
        DATASET_ID,
        split="train",
        revision=DATASET_COMMIT,
    )
    examples = [
        Example(
            x=row["x"],
            Fx=row["Fx"],
            Gx=row["Gx"],
            GFx=row["GFx"],
            FGx=row["FGx"],
        )
        for row in dataset
        if row["task"] == TASK_NAME
    ]
    if len(examples) != EXPECTED_DATASET_SIZE:
        raise RuntimeError(
            f"Expected {EXPECTED_DATASET_SIZE} {TASK_NAME} examples, got {len(examples)}"
        )
    return examples


def shuffle_examples(
    examples: list[Example],
    *,
    seed: int = DEFAULT_SEED,
) -> list[Example]:
    """Mirror the authors' seeded dataset shuffle before context sampling."""
    shuffled = examples.copy()
    random.Random(seed).shuffle(shuffled)
    return shuffled


def generate_in_context_queries(
    examples: list[Example],
    *,
    icl_examples: int = DEFAULT_ICL_EXAMPLES,
    seed: int = DEFAULT_SEED,
) -> list[InContextQuery]:
    """Mirror the authors' seed-0, rejection-sampled context construction."""
    rng = random.Random(seed)
    queries = []
    for query in examples:
        context: list[Example] = []
        while len(context) < icl_examples:
            example = rng.choice(examples)
            if example not in context and example != query and not example.overlaps(query):
                context.append(example)
        queries.append(InContextQuery(context=tuple(context), query=query))
    return queries


def sample_queries(
    queries: list[InContextQuery],
    *,
    num_queries: int,
    seed: int = DEFAULT_SEED,
) -> list[InContextQuery]:
    if not 1 <= num_queries <= len(queries):
        raise ValueError(f"num_queries must be between 1 and {len(queries)}")
    return random.Random(seed).sample(queries, num_queries)


def generate_continuation(model, tokenizer, prompt: str) -> str:
    """Mirror the authors' greedy Transformers generation and string handling."""
    model_inputs = tokenizer([prompt], return_tensors="pt").to(model.device)
    generated_tokens = model.generate(
        **model_inputs,
        tokenizer=tokenizer,
        max_new_tokens=MAX_NEW_TOKENS,
        stop_strings=STOP_SEQUENCE,
        pad_token_id=(tokenizer.pad_token_id or tokenizer.eos_token_id),
    )
    generated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    continuation = generated_text[len(prompt) :]
    return continuation.split(STOP_SEQUENCE, maxsplit=1)[0]


def evaluate_compositions(model, tokenizer, queries: list[InContextQuery]) -> dict:
    """Evaluate only the direct English-word to Spanish-antonym mapping."""
    predictions = []
    for query in queries:
        prompt = query.prompt("x", "GFx")
        predictions.append(
            Prediction(
                prompt=prompt,
                pred=generate_continuation(model, tokenizer, prompt),
                label=query.query.get("GFx", leading_space=True),
            )
        )
    return {
        "accuracy": mean(pred.pred == pred.label for pred in predictions),
        "predictions": [asdict(pred) for pred in predictions],
    }


def composition_correct_indices(results: dict[str, dict]) -> list[int]:
    """Indices where the direct x -> GFx prediction exactly matches GFx."""
    return [
        index
        for index, prediction in enumerate(results["x_GFx"]["predictions"])
        if prediction["pred"] == prediction["label"]
    ]


def correct_query_records(
    queries: list[InContextQuery],
    results: dict[str, dict],
    dataset_indices: dict[Example, int],
) -> list[dict]:
    records = []
    for evaluation_index in composition_correct_indices(results):
        in_context_query = queries[evaluation_index]
        records.append(
            {
                "evaluation_index": evaluation_index,
                "dataset_index": dataset_indices[in_context_query.query],
                "context": [asdict(example) for example in in_context_query.context],
                "query": asdict(in_context_query.query),
                "prediction": results["x_GFx"]["predictions"][evaluation_index],
            }
        )
    return records


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records)
    )


def summarize(results: dict[str, dict]) -> dict:
    composition_correct = {
        index
        for index, prediction in enumerate(results["x_GFx"]["predictions"])
        if prediction["pred"] == prediction["label"]
    }
    total = len(results["x_GFx"]["predictions"])
    return {
        "x_GFx": results["x_GFx"]["accuracy"],
        "num_queries": total,
        "num_composition_correct": len(composition_correct),
    }


def main() -> None:
    args = parse_args()

    from transformers import AutoModelForCausalLM, AutoTokenizer

    unshuffled_examples = load_examples()
    dataset_indices = {
        example: index for index, example in enumerate(unshuffled_examples)
    }
    examples = shuffle_examples(unshuffled_examples, seed=args.seed)
    all_queries = generate_in_context_queries(
        examples,
        icl_examples=args.icl_examples,
        seed=args.seed,
    )
    queries = sample_queries(all_queries, num_queries=args.num_queries, seed=args.seed)

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID,
        revision=STAGE_ONE_COMMIT,
        padding_side="left",
    )
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        revision=STAGE_ONE_COMMIT,
        device_map="auto",
        dtype="auto",
    )
    model.eval()

    results = {"x_GFx": evaluate_compositions(model, tokenizer, queries)}
    correct_records = correct_query_records(
        queries,
        results,
        dataset_indices=dataset_indices,
    )
    output = {
        "metadata": {
            "model": MODEL_ID,
            "stage_one_revision": STAGE_ONE_REVISION,
            "model_commit": STAGE_ONE_COMMIT,
            "dataset": DATASET_ID,
            "dataset_commit": DATASET_COMMIT,
            "reference_code_commit": REFERENCE_CODE_COMMIT,
            "task": TASK_NAME,
            "seed": args.seed,
            "icl_examples": args.icl_examples,
            "evaluated_mapping": "x_GFx",
            "max_new_tokens": MAX_NEW_TOKENS,
            "stop_sequence": STOP_SEQUENCE,
        },
        "summary": summarize(results),
        "results": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    write_jsonl(args.correct_output, correct_records)
    print(json.dumps(output["summary"], indent=2))
    print(f"Wrote {args.output}")
    print(f"Wrote {len(correct_records)} correct composition queries to {args.correct_output}")


if __name__ == "__main__":
    main()
