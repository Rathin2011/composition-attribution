"""Screen stage-one OLMo 3 on landmark-country-capital composition.

Prompt construction, context sampling, generation, and exact-match scoring are
adapted from Khandelwal and Pavlick's MIT-licensed ``composing-functions``
repository at commit f12cef400ff946ab09cee988817daea939436698.

This screening block evaluates only the standalone composition x -> g(f(x)).
The two primitive mappings and logit-lens analysis are intentionally out of
scope until the number of correct compositions is known.
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
TASK_NAME = "landmark-country-capital"
EXPECTED_DATASET_SIZE = 1_385
DEFAULT_SEED = 0
DEFAULT_ICL_EXAMPLES = 10
DEFAULT_NUM_QUERIES = EXPECTED_DATASET_SIZE
MAX_NEW_TOKENS = 20
STOP_SEQUENCE = "\n\n"
PROJECT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = (
    PROJECT_DIR / "results" / "olmo3_stage1_landmark_country_capital.json"
)
DEFAULT_CORRECT_OUTPUT = (
    PROJECT_DIR
    / "results"
    / "olmo3_stage1_landmark_country_capital.correct.jsonl"
)

Node = Literal["x", "Fx", "GFx"]


@dataclass(frozen=True)
class Example:
    x: str
    Fx: str
    GFx: str

    def get(self, node: Node, *, leading_space: bool = False) -> str:
        value = getattr(self, node)
        return f" {value}" if leading_space else value

    def overlaps(self, other: "Example") -> bool:
        return bool(set(asdict(self).values()) & set(asdict(other).values()))


@dataclass(frozen=True)
class InContextQuery:
    context: tuple[Example, ...]
    query: Example

    def composition_prompt(self) -> str:
        text = "".join(
            f"Q: {example.x}\nA: {example.GFx}\n\n" for example in self.context
        )
        return f"{text}Q: {self.query.x}\nA:"


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
        Example(x=row["x"], Fx=row["Fx"], GFx=row["GFx"])
        for row in dataset
        if row["task"] == TASK_NAME
    ]
    if len(examples) != EXPECTED_DATASET_SIZE:
        raise RuntimeError(
            f"Expected {EXPECTED_DATASET_SIZE} {TASK_NAME} examples, got {len(examples)}"
        )
    if any(not example.x or not example.Fx or not example.GFx for example in examples):
        raise RuntimeError(f"{TASK_NAME} contains a missing required node")
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
    """Mirror the authors' seeded, rejection-sampled context construction."""

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
    model_inputs = tokenizer(
        [prompt], return_tensors="pt", return_token_type_ids=False
    )
    input_device = model.get_input_embeddings().weight.device
    model_inputs = {name: tensor.to(input_device) for name, tensor in model_inputs.items()}
    generated_tokens = model.generate(
        **model_inputs,
        tokenizer=tokenizer,
        do_sample=False,
        max_new_tokens=MAX_NEW_TOKENS,
        stop_strings=STOP_SEQUENCE,
        pad_token_id=(tokenizer.pad_token_id or tokenizer.eos_token_id),
    )
    generated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    continuation = generated_text[len(prompt) :]
    return continuation.split(STOP_SEQUENCE, maxsplit=1)[0]


def evaluate_compositions(model, tokenizer, queries: list[InContextQuery]) -> dict:
    predictions = []
    for query in queries:
        prompt = query.composition_prompt()
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


def correct_query_records(
    queries: list[InContextQuery],
    composition_results: dict,
    dataset_indices: dict[Example, int],
) -> list[dict]:
    records = []
    for evaluation_index, prediction in enumerate(composition_results["predictions"]):
        if prediction["pred"] != prediction["label"]:
            continue
        query = queries[evaluation_index]
        records.append(
            {
                "evaluation_index": evaluation_index,
                "dataset_index": dataset_indices[query.query],
                "context": [asdict(example) for example in query.context],
                "query": asdict(query.query),
                "prediction": prediction,
            }
        )
    return records


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records)
    )


def summarize(composition_results: dict) -> dict:
    predictions = composition_results["predictions"]
    correct = sum(item["pred"] == item["label"] for item in predictions)
    return {
        "x_GFx": composition_results["accuracy"],
        "num_queries": len(predictions),
        "num_composition_correct": correct,
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

    composition_results = evaluate_compositions(model, tokenizer, queries)
    correct_records = correct_query_records(
        queries,
        composition_results,
        dataset_indices=dataset_indices,
    )
    output = {
        "metadata": {
            "model": MODEL_ID,
            "stage_one_revision": STAGE_ONE_REVISION,
            "model_commit": STAGE_ONE_COMMIT,
            "dataset": DATASET_ID,
            "dataset_commit": DATASET_COMMIT,
            "task": TASK_NAME,
            "reference_code_commit": REFERENCE_CODE_COMMIT,
            "seed": args.seed,
            "icl_examples": args.icl_examples,
            "evaluated_mapping": "x_GFx",
            "max_new_tokens": MAX_NEW_TOKENS,
            "stop_sequence": STOP_SEQUENCE,
        },
        "summary": summarize(composition_results),
        "results": {"x_GFx": composition_results},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    write_jsonl(args.correct_output, correct_records)
    print(json.dumps(output["summary"], indent=2))
    print(f"Wrote {args.output}")
    print(f"Wrote {len(correct_records)} correct composition queries to {args.correct_output}")


if __name__ == "__main__":
    main()
