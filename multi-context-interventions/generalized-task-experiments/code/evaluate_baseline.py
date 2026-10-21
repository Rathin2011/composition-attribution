"""Evaluate OLMo 3 on a generalized task prompt manifest.

The implementation is shared by every registered task.  A run is selected by
``--task`` and its manifest; no task-specific model logic appears here.

For each query-context instance, this stage saves:

* the complete greedy continuation and exact-match correctness;
* the true Fx and GFx first-token logit, probability, and full-vocabulary rank;
* first-token logits for every possible Fx and GFx value in the task.

The task candidate order and every candidate's complete tokenizer encoding are
stored in the summary.  Consequently, later lens and intervention stages can
write matrices/vectors whose rows have one stable, auditable meaning.
"""

from __future__ import annotations

import argparse
import gzip
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping, Sequence

from tasks import TASKS, get_task_spec


MODEL_ID = "allenai/Olmo-3-1025-7B"
STAGE_ONE_REVISION = "stage1-step1413814"
STAGE_ONE_COMMIT = "373bad25002f1624757a73235c5ca844c6375c25"
MODEL_DTYPE = "bfloat16"
MAX_NEW_TOKENS = 20
STOP_SEQUENCE = "\n\n"
DEFAULT_TOP_KS = (1, 5, 10)
PROJECT_DIR = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class CandidateValues:
    """All unique task values in stable first-occurrence order."""

    task: str
    x: tuple[str, ...]
    Fx: tuple[str, ...]
    GFx: tuple[str, ...]


@dataclass
class RunningSummary:
    """Accumulate behavioral accuracy without retaining every result row."""

    top_ks: tuple[int, ...]
    evaluated: int = 0
    exact_correct: int = 0
    gfx_rank_sum: int = 0

    def __post_init__(self) -> None:
        self.top_k_correct = {value: 0 for value in self.top_ks}

    def add(self, result: Mapping[str, Any]) -> None:
        """Incorporate one evaluated prompt."""

        evaluation = result["evaluation"]
        target = evaluation["final_next_token_readout"]["target_GFx_first_token"]
        self.evaluated += 1
        self.exact_correct += int(evaluation["exact_match"])
        self.gfx_rank_sum += int(target["rank"])
        for value in self.top_ks:
            self.top_k_correct[value] += int(target["in_top_k"][str(value)])

    def as_dict(self) -> dict[str, Any]:
        """Return aggregate metrics in JSON-compatible form."""

        denominator = self.evaluated or 1
        return {
            "num_prompt_instances": self.evaluated,
            "num_exact_correct": self.exact_correct,
            "exact_accuracy": self.exact_correct / denominator,
            "GFx_first_token_top_k": {
                str(value): {
                    "correct": self.top_k_correct[value],
                    "accuracy": self.top_k_correct[value] / denominator,
                }
                for value in self.top_ks
            },
            "mean_GFx_first_token_rank": self.gfx_rank_sum / denominator,
        }


def parse_args() -> argparse.Namespace:
    """Parse a task-general full, shard, or smoke-test evaluation."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, choices=sorted(TASKS))
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--summary-output", type=Path)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--num-records", type=int)
    parser.add_argument("--top-k", type=int, action="append", default=[])
    parser.add_argument("--progress-every", type=int, default=10)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def validate_top_ks(values: Iterable[int]) -> tuple[int, ...]:
    """Return sorted unique positive top-k thresholds."""

    supplied = tuple(values)
    output = tuple(sorted(set(supplied or DEFAULT_TOP_KS)))
    if any(value <= 0 for value in output):
        raise ValueError("top-k values must be positive")
    return output


def read_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    """Yield nonempty JSON objects from a JSONL file."""

    found = False
    with open_text(path, "rt") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                raise ValueError(f"{path}:{line_number} is empty")
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number} is not an object")
            found = True
            yield value
    if not found:
        raise ValueError(f"{path} contains no records")


def open_text(path: Path, mode: str):
    """Open plain text or gzip text according to the filename suffix."""

    if "t" not in mode:
        raise ValueError("open_text requires an explicit text mode")
    if path.suffix == ".gz":
        return gzip.open(path, mode, encoding="utf-8")
    return path.open(mode, encoding="utf-8")


def candidate_values(path: Path, expected_task: str) -> CandidateValues:
    """Derive complete ordered x/Fx/GFx sets from the full task manifest."""

    output = {name: [] for name in ("x", "Fx", "GFx")}
    seen = {name: set() for name in output}
    for line_number, record in enumerate(read_jsonl(path), start=1):
        if record.get("task") != expected_task:
            raise ValueError(
                f"manifest row {line_number} has task {record.get('task')!r}, "
                f"expected {expected_task!r}"
            )
        query = record.get("query")
        if not isinstance(query, Mapping):
            raise ValueError(f"manifest row {line_number} lacks a query object")
        for name in output:
            value = query.get(name)
            if not isinstance(value, str) or not value:
                raise ValueError(f"manifest row {line_number} has invalid {name}")
            if value not in seen[name]:
                output[name].append(value)
                seen[name].add(value)
    return CandidateValues(
        task=expected_task,
        x=tuple(output["x"]),
        Fx=tuple(output["Fx"]),
        GFx=tuple(output["GFx"]),
    )


def read_manifest_slice(
    path: Path,
    expected_task: str,
    *,
    start_index: int,
    num_records: int | None,
) -> Iterator[dict[str, Any]]:
    """Yield a validated contiguous manifest slice for model evaluation."""

    if start_index < 0:
        raise ValueError("start-index must be non-negative")
    if num_records is not None and num_records <= 0:
        raise ValueError("num-records must be positive")
    yielded = 0
    for row_index, record in enumerate(read_jsonl(path)):
        if row_index < start_index:
            continue
        if num_records is not None and yielded >= num_records:
            break
        if record.get("task") != expected_task:
            raise ValueError(f"row {row_index} does not belong to {expected_task}")
        required = {"prompt_instance_id", "prompt", "query", "context"}
        if missing := required - record.keys():
            raise ValueError(f"row {row_index} is missing {sorted(missing)}")
        yield record
        yielded += 1


def batched(records: Iterable[Any], batch_size: int) -> Iterator[list[Any]]:
    """Group a stream into bounded model batches."""

    if batch_size <= 0:
        raise ValueError("batch-size must be positive")
    batch = []
    for record in records:
        batch.append(record)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def leading_space_token_ids(tokenizer: Any, text: str) -> list[int]:
    """Tokenize one candidate exactly as it begins after the final ``A:``."""

    token_ids = tokenizer.encode(f" {text}", add_special_tokens=False)
    if not token_ids:
        raise ValueError(f"candidate has no tokenizer tokens: {text!r}")
    return [int(value) for value in token_ids]


def tokenize_candidates(
    tokenizer: Any, candidates: CandidateValues
) -> dict[str, Any]:
    """Attach complete token IDs to every Fx/GFx candidate value."""

    spec = get_task_spec(candidates.task)
    return {
        "task": candidates.task,
        "measurement": "task_aware_first_token" if spec.numeric_nodes else "first_token_with_leading_space",
        "x": list(candidates.x),
        "Fx": [
            {"value": value, "token_ids": spec.token_ids(tokenizer, "Fx", value)}
            for value in candidates.Fx
        ],
        "GFx": [
            {"value": value, "token_ids": spec.token_ids(tokenizer, "GFx", value)}
            for value in candidates.GFx
        ],
    }


def token_measurement(
    logits: Any, token_id: int, top_ks: Sequence[int]
) -> dict[str, Any]:
    """Measure one token against the complete vocabulary distribution."""

    if logits.ndim != 1:
        raise ValueError("logits must be one-dimensional")
    float_logits = logits.float()
    target_logit = float_logits[token_id]
    rank = 1 + int((float_logits > target_logit).sum().item())
    log_probability = target_logit - float_logits.logsumexp(dim=-1)
    return {
        "token_id": int(token_id),
        "logit": float(target_logit.item()),
        "log_probability": float(log_probability.item()),
        "probability": float(log_probability.exp().item()),
        "rank": rank,
        "reciprocal_rank": 1.0 / rank,
        "in_top_k": {str(value): rank <= value for value in top_ks},
    }


def selected_logits(logits: Any, token_ids: Sequence[int]) -> list[float]:
    """Return logits in candidate-catalog order."""

    if logits.ndim != 1:
        raise ValueError("logits must be one-dimensional")
    return [float(logits[int(token_id)].float().item()) for token_id in token_ids]


def top_tokens(logits: Any, tokenizer: Any, count: int) -> list[dict[str, Any]]:
    """Return readable highest-logit vocabulary alternatives."""

    values, indices = logits.float().topk(min(count, int(logits.shape[0])))
    return [
        {
            "token_id": int(token_id),
            "token": tokenizer.decode([int(token_id)]),
            "logit": float(value),
        }
        for value, token_id in zip(values.tolist(), indices.tolist(), strict=True)
    ]


def evaluate_batch(
    model: Any,
    tokenizer: Any,
    records: list[dict[str, Any]],
    *,
    tokenized_candidates: Mapping[str, Any],
    top_ks: tuple[int, ...],
    torch_module: Any,
) -> list[dict[str, Any]]:
    """Generate answers and save every required baseline measurement."""

    for record in records:
        get_task_spec(record["task"]).validate_prompt(record["prompt"], record["query"]["x"])
    prompts = [record["prompt"] for record in records]
    model_inputs = tokenizer(
        prompts, padding=True, return_tensors="pt", return_token_type_ids=False
    )
    device = model.get_input_embeddings().weight.device
    model_inputs = {name: value.to(device) for name, value in model_inputs.items()}
    prompt_width = int(model_inputs["input_ids"].shape[1])
    with torch_module.inference_mode():
        generated = model.generate(
            **model_inputs,
            tokenizer=tokenizer,
            do_sample=False,
            max_new_tokens=MAX_NEW_TOKENS,
            stop_strings=STOP_SEQUENCE,
            pad_token_id=tokenizer.pad_token_id,
            return_dict_in_generate=True,
            output_logits=True,
        )
    if not generated.logits:
        raise RuntimeError("generation returned no first-step logits")

    first_step_logits = generated.logits[0]
    fx_first_ids = [entry["token_ids"][0] for entry in tokenized_candidates["Fx"]]
    gfx_first_ids = [entry["token_ids"][0] for entry in tokenized_candidates["GFx"]]
    results = []
    for row, record in enumerate(records):
        query = record["query"]
        spec = get_task_spec(record["task"])
        fx_ids = spec.token_ids(tokenizer, "Fx", query["Fx"])
        gfx_ids = spec.token_ids(tokenizer, "GFx", query["GFx"])
        continuation_ids = generated.sequences[row, prompt_width:]
        prediction = tokenizer.decode(continuation_ids, skip_special_tokens=True)
        prediction = prediction.split(STOP_SEQUENCE, maxsplit=1)[0]
        expected = spec.target_text("GFx", query["GFx"])
        logits = first_step_logits[row]

        fx_target = token_measurement(logits, fx_ids[0], top_ks)
        fx_target.update({"value": query["Fx"], "token_ids": fx_ids})
        gfx_target = token_measurement(logits, gfx_ids[0], top_ks)
        gfx_target.update({"value": query["GFx"], "token_ids": gfx_ids})
        output = dict(record)
        output["evaluation"] = {
            "prediction": prediction,
            "label": expected,
            "exact_match": prediction == expected,
            "final_next_token_readout": {
                "target_Fx_first_token": fx_target,
                "target_GFx_first_token": gfx_target,
                "candidate_Fx_first_token_logits": selected_logits(
                    logits, fx_first_ids
                ),
                "candidate_GFx_first_token_logits": selected_logits(
                    logits, gfx_first_ids
                ),
                "top_tokens": top_tokens(logits, tokenizer, max(top_ks)),
            },
        }
        results.append(output)
    return results


def ensure_outputs(paths: Sequence[Path], overwrite: bool) -> None:
    """Create output parents and prevent accidental replacement."""

    existing = [path for path in paths if path.exists()]
    if existing and not overwrite:
        raise FileExistsError(f"outputs already exist; use --overwrite: {existing}")
    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)


def main() -> None:
    args = parse_args()
    spec = get_task_spec(args.task)
    task_directory = PROJECT_DIR / "results" / spec.dataset_task
    input_path = args.input or task_directory / "prompt_manifest.jsonl"
    output_path = args.output or task_directory / "baseline_evaluation.jsonl.gz"
    summary_path = args.summary_output or task_directory / "baseline_summary.json"
    ensure_outputs((output_path, summary_path), args.overwrite)
    if args.progress_every <= 0:
        raise ValueError("progress-every must be positive")
    top_ks = validate_top_ks(args.top_k)
    values = candidate_values(input_path, spec.dataset_task)

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID, revision=STAGE_ONE_COMMIT, padding_side="left"
    )
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        revision=STAGE_ONE_COMMIT,
        device_map="auto",
        dtype=torch.bfloat16,
    )
    model.eval()
    catalog = tokenize_candidates(tokenizer, values)
    records = read_manifest_slice(
        input_path,
        spec.dataset_task,
        start_index=args.start_index,
        num_records=args.num_records,
    )
    counters = RunningSummary(top_ks)
    with open_text(output_path, "wt") as handle:
        for batch_number, batch in enumerate(batched(records, args.batch_size), start=1):
            evaluated = evaluate_batch(
                model,
                tokenizer,
                batch,
                tokenized_candidates=catalog,
                top_ks=top_ks,
                torch_module=torch,
            )
            for result in evaluated:
                handle.write(json.dumps(result, ensure_ascii=False) + "\n")
                counters.add(result)
            handle.flush()
            if batch_number % args.progress_every == 0:
                print(f"Evaluated {counters.evaluated} prompt instances", flush=True)

    summary = {
        "task": spec.dataset_task,
        "model": MODEL_ID,
        "stage_one_revision": STAGE_ONE_REVISION,
        "model_commit": STAGE_ONE_COMMIT,
        "dtype": MODEL_DTYPE,
        "input": str(input_path),
        "output": str(output_path),
        "start_index": args.start_index,
        "requested_num_records": args.num_records,
        "batch_size": args.batch_size,
        "max_new_tokens": MAX_NEW_TOKENS,
        "stop_sequence": STOP_SEQUENCE,
        "rank_scope": "full_vocabulary",
        "target_measurement": catalog["measurement"],
        "candidate_catalog": catalog,
        **counters.as_dict(),
    }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({key: value for key, value in summary.items() if key != "candidate_catalog"}, indent=2))
    print(f"Wrote {output_path}")
    print(f"Wrote {summary_path}")


if __name__ == "__main__":
    main()
