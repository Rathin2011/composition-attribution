"""Run the baseline OLMo 3 evaluation for the multi-context experiment.

High-level purpose
==================
This program answers the behavioral question that must be established before
we use Logit Lens, J-Lens, or interventions:

    Given this exact in-context prompt, what capital does stage-one OLMo 3
    generate, and how strongly does its next-token distribution support the
    correct intermediate country and final capital?

The file loads prompts that have already been created. It does not sample new
demonstrations or modify the model.

Input
=====
``--input`` points to the JSONL manifest written by
``build_prompt_manifest.py``. Each line is one query-context instance::

    {
      "prompt_instance_id": "query_0000_context_00",
      "prompt": "Q: ...\\nA: ...\\n\\nQ: Biedenkopf\\nA:",
      "query": {
        "x": "Biedenkopf",  # landmark
        "Fx": "Germany",    # intermediate country
        "GFx": "Berlin"     # correct capital
      },
      ...
    }

Other input fields, including all demonstrations, are preserved in the output.
``--start-index`` and ``--num-records`` can select a contiguous subset for a
smoke test or scheduler shard.

Output
======
``--output`` is JSONL with one row per evaluated input row. Each row contains
the original manifest data plus::

    "evaluation": {
      "prediction": " Berlin",
      "label": " Berlin",
      "exact_match": true,
      "final_next_token_readout": {
        "Fx_first_token": {
          "logit": ...,
          "log_probability": ...,
          "rank": ...,
          "reciprocal_rank": ...
        },
        "GFx_first_token": { ...same measurements... },
        "top_tokens": [ ...highest-scoring next tokens... ]
      }
    }

Country and capital ranks are calculated against the complete vocabulary. For
a multi-token name, this baseline measures its first token after ``A:``
(including the leading space), matching the convention used in the earlier
experiment. ``exact_match`` instead checks the complete generated answer.

``--summary-output`` is a regular JSON file containing the pinned checkpoint,
run parameters, exact accuracy, capital first-token top-k accuracy, and mean
capital first-token rank.

Functional flow
===============
1. ``parse_args`` reads the run configuration.
2. ``validate_top_ks`` and ``ensure_output_paths`` validate it.
3. ``main`` loads the pinned stage-one tokenizer and model.
4. ``read_manifest`` validates and streams the requested rows.
5. ``batched`` groups them into small model batches.
6. ``evaluate_batch`` generates answers and retrieves the first-answer-token
   full-vocabulary logits.
7. ``leading_space_token_ids``, ``token_measurement``, and ``top_tokens`` turn
   those logits into target-specific measurements.
8. ``RunningSummary`` accumulates aggregate results while ``main`` writes each
   result row to disk.
9. ``main`` writes the final summary JSON.

This file deliberately does not calculate layerwise lens evidence, classify a
prompt as compositional/shortcut, or alter activations.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence


# Model/checkpoint constants make the evaluated model immutable and auditable.
MODEL_ID = "allenai/Olmo-3-1025-7B"
STAGE_ONE_REVISION = "stage1-step1413814"
STAGE_ONE_COMMIT = "373bad25002f1624757a73235c5ca844c6375c25"
MODEL_DTYPE = "bfloat16"
MAX_NEW_TOKENS = 20
STOP_SEQUENCE = "\n\n"
DEFAULT_TOP_KS = (1, 5, 10)

# Defaults keep all inputs and outputs inside this experiment directory.
PROJECT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = PROJECT_DIR / "results" / "all_queries_prompt_manifest.jsonl"
DEFAULT_OUTPUT = PROJECT_DIR / "results" / "baseline_evaluation.jsonl"
DEFAULT_SUMMARY = PROJECT_DIR / "results" / "baseline_evaluation_summary.json"


@dataclass
class RunningSummary:
    """Accumulate aggregate results without retaining every output in memory.

    Input:
        ``top_ks`` is the tuple of requested first-token top-k cutoffs. The
        other fields are counters initialized to zero.

    Output:
        A mutable accumulator. ``as_dict`` converts it into the summary object
        written after evaluation.

    Role:
        ``main`` writes results incrementally instead of building one large
        in-memory list. This object retains only the required totals.
    """

    top_ks: tuple[int, ...]
    evaluated: int = 0
    exact_correct: int = 0
    final_gfx_rank_sum: int = 0

    def __post_init__(self) -> None:
        """Create a correct-count accumulator for every requested k.

        Input: ``self.top_ks`` from dataclass initialization.
        Output: no return value; initializes ``self.top_k_correct``.
        """

        self.top_k_correct = {k: 0 for k in self.top_ks}

    def add(self, result: dict[str, Any]) -> None:
        """Add one evaluated prompt to the aggregate counters.

        Input:
            One result from ``evaluate_batch``, containing exact correctness
            and capital first-token rank/top-k flags.
        Output:
            No return value; mutates this accumulator's counters.
        Role:
            Called immediately after each per-prompt JSONL row is written.
        """

        self.evaluated += 1
        self.exact_correct += int(result["evaluation"]["exact_match"])
        final_readout = result["evaluation"]["final_next_token_readout"]
        final_gfx = final_readout["GFx_first_token"]
        self.final_gfx_rank_sum += int(final_gfx["rank"])
        for k in self.top_ks:
            self.top_k_correct[k] += int(final_gfx["in_top_k"][str(k)])

    def as_dict(self) -> dict[str, Any]:
        """Calculate serializable aggregate counts and averages.

        Input: the accumulator's current counters.
        Output: a dictionary for inclusion in the summary JSON.
        """

        # The fallback avoids division by zero for an intentionally empty slice.
        denominator = self.evaluated or 1
        return {
            "num_prompt_instances": self.evaluated,
            "num_exact_correct": self.exact_correct,
            "exact_accuracy": self.exact_correct / denominator,
            "final_next_token_readout": {
                "GFx_first_token_top_k": {
                    str(k): {
                        "correct": self.top_k_correct[k],
                        "accuracy": self.top_k_correct[k] / denominator,
                    }
                    for k in self.top_ks
                },
                "mean_GFx_first_token_rank": (
                    self.final_gfx_rank_sum / denominator
                ),
            },
        }


def parse_args() -> argparse.Namespace:
    """Read the baseline run configuration from command-line flags.

    Input:
        The process command line: paths, batch size, optional manifest slice,
        top-k values, and overwrite permission.
    Output:
        An ``argparse.Namespace`` consumed by ``main``.
    Role:
        Provides one explicit interface for full, sharded, and smoke-test runs.
    """

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument(
        "--num-records",
        type=int,
        default=None,
        help="Optional number of manifest rows to evaluate after --start-index.",
    )
    parser.add_argument("--top-k", type=int, action="append", default=[])
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Permit replacing existing output files.",
    )
    return parser.parse_args()


def validate_top_ks(values: Iterable[int]) -> tuple[int, ...]:
    """Canonicalize requested top-k cutoffs.

    Input:
        Integers supplied by repeated ``--top-k`` flags. An empty iterable uses
        the defaults ``(1, 5, 10)``.
    Output:
        A sorted tuple of unique positive integers.
    Role:
        Gives per-query and aggregate measurements one consistent definition.
    """

    values = tuple(values)
    top_ks = tuple(sorted(set(values or DEFAULT_TOP_KS)))
    if any(k <= 0 for k in top_ks):
        raise ValueError("top-k values must be positive")
    return top_ks


def validate_manifest_record(record: dict[str, Any], line_number: int) -> None:
    """Check that one manifest row has all data needed for evaluation.

    Inputs:
        ``record`` is one decoded JSON object. ``line_number`` identifies its
        source line for useful error messages.
    Output:
        No return value when valid; raises ``ValueError`` when required fields
        or x/Fx/GFx query nodes are missing.
    Role:
        Fails before model computation on a malformed input row.
    """

    required = {"prompt_instance_id", "prompt", "query"}
    missing = required - record.keys()
    if missing:
        raise ValueError(
            f"manifest line {line_number} is missing fields: {sorted(missing)}"
        )
    query = record["query"]
    if not isinstance(query, dict):
        raise ValueError(f"manifest line {line_number} query must be an object")
    missing_nodes = {"x", "Fx", "GFx"} - query.keys()
    if missing_nodes:
        raise ValueError(
            f"manifest line {line_number} query is missing nodes: "
            f"{sorted(missing_nodes)}"
        )


def read_manifest(
    path: Path,
    *,
    start_index: int = 0,
    num_records: int | None = None,
) -> Iterator[dict[str, Any]]:
    """Stream a validated contiguous slice of the prompt manifest.

    Inputs:
        ``path`` is the JSONL file. ``start_index`` skips initial rows, and
        ``num_records`` optionally limits the number then yielded.
    Output:
        An iterator of validated manifest dictionaries.
    Role:
        Supports full runs, smoke tests, and scheduler shards without loading
        the whole manifest into memory.
    """

    if start_index < 0:
        raise ValueError("start_index must be non-negative")
    if num_records is not None and num_records <= 0:
        raise ValueError("num_records must be positive when supplied")

    yielded = 0
    with path.open(encoding="utf-8") as handle:
        for zero_based_index, line in enumerate(handle):
            # The slice is defined by stable physical JSONL row order.
            if zero_based_index < start_index:
                continue
            if num_records is not None and yielded >= num_records:
                break
            record = json.loads(line)
            validate_manifest_record(record, zero_based_index + 1)
            yield record
            yielded += 1


def batched(records: Iterable[dict[str, Any]], batch_size: int) -> Iterator[list[dict]]:
    """Group streamed records into bounded model batches.

    Inputs:
        ``records`` is an iterable of manifest dictionaries. ``batch_size`` is
        the maximum prompts sent through the model together.
    Output:
        An iterator of record lists; the last list may be smaller.
    Role:
        Separates JSONL streaming from GPU batching and bounds memory use.
    """

    if batch_size <= 0:
        raise ValueError("batch_size must be positive")
    batch: list[dict] = []
    for record in records:
        batch.append(record)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def leading_space_token_ids(tokenizer: Any, text: str) -> list[int]:
    """Tokenize a target as it would begin immediately after ``A:``.

    Inputs:
        ``tokenizer`` is the OLMo tokenizer. ``text`` is a country or capital,
        such as ``"Egypt"`` or ``"United Kingdom"``.
    Output:
        The nonempty vocabulary-ID list for ``" " + text``. Multi-token names
        return multiple IDs even though this baseline measures the first one.
    Role:
        Ensures target IDs use the same leading-space form as model answers.
    """

    token_ids = tokenizer.encode(f" {text}", add_special_tokens=False)
    if not token_ids:
        raise ValueError(f"answer has no tokenizer tokens: {text!r}")
    return [int(token_id) for token_id in token_ids]


def token_measurement(logits: Any, token_id: int, top_ks: Sequence[int]) -> dict:
    """Extract one target token's statistics from full-vocabulary logits.

    Inputs:
        ``logits`` is a one-dimensional tensor of length ``vocabulary_size``.
        ``token_id`` selects the target vocabulary entry. ``top_ks`` supplies
        the requested membership cutoffs.
    Output:
        A dictionary containing logit, log-probability, probability, one-based
        full-vocabulary rank, reciprocal rank, and top-k flags.
    Role:
        Applies one definition to both the country and capital first tokens.

    Rank is ``1 + number of tokens with a strictly greater logit``. Therefore,
    tokens tied at the same value receive the best shared rank.
    """

    if logits.ndim != 1:
        raise ValueError("logits must be a one-dimensional vocabulary vector")
    if not 0 <= token_id < logits.shape[0]:
        raise ValueError("token_id is outside the vocabulary")

    # Model weights use bfloat16, but float32 makes ranking and logsumexp more
    # numerically stable and produces ordinary Python floats for JSON output.
    float_logits = logits.float()
    target_logit = float_logits[token_id]
    rank = 1 + int((float_logits > target_logit).sum().item())
    log_probability = target_logit - float_logits.logsumexp(dim=-1)
    return {
        "token_id": token_id,
        "logit": float(target_logit.item()),
        "log_probability": float(log_probability.item()),
        "probability": float(log_probability.exp().item()),
        "rank": rank,
        "reciprocal_rank": 1.0 / rank,
        "in_top_k": {str(k): rank <= k for k in top_ks},
    }


def top_tokens(logits: Any, tokenizer: Any, k: int) -> list[dict[str, Any]]:
    """Make the highest-scoring next-token alternatives readable.

    Inputs:
        ``logits`` is one full-vocabulary vector; ``tokenizer`` decodes IDs;
        ``k`` requests how many leading entries to retain.
    Output:
        A descending list of token ID, decoded token, and raw logit objects.
    Role:
        Makes individual results inspectable without saving every vocabulary
        logit for every prompt, which would create a multi-gigabyte artifact.
    """

    k = min(k, int(logits.shape[-1]))
    values, indices = logits.float().topk(k)
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
    top_ks: tuple[int, ...],
    torch_module: Any,
) -> list[dict[str, Any]]:
    """Run the model and construct output records for one prompt batch.

    Inputs:
        ``model`` and ``tokenizer`` are the loaded stage-one OLMo components.
        ``records`` comes from ``batched``. ``top_ks`` gives rank cutoffs.
        ``torch_module`` is PyTorch, passed explicitly to keep dependencies
        visible and the surrounding helpers easy to test.
    Output:
        One result dictionary per input record, in matching order. Each result
        preserves all input fields and adds an ``evaluation`` object.
    Role:
        This is the central computation: greedy generation, extraction of the
        first answer step's logits, Fx/GFx measurement, and exact-match scoring.
    """

    # Left padding aligns each prompt's final ``A:`` at the batch's last input
    # column, which is the position used to predict the first answer token.
    prompts = [record["prompt"] for record in records]
    model_inputs = tokenizer(
        prompts,
        padding=True,
        return_tensors="pt",
        return_token_type_ids=False,
    )
    input_device = model.get_input_embeddings().weight.device
    model_inputs = {
        name: tensor.to(input_device) for name, tensor in model_inputs.items()
    }
    # Generated sequences contain the padded prompt followed by new tokens.
    # Save this common width so we can slice out only the continuation later.
    prompt_width = int(model_inputs["input_ids"].shape[1])

    with torch_module.inference_mode():
        # Greedy decoding makes the baseline deterministic. ``output_logits``
        # lets this same call return the distributions used during generation.
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
        raise RuntimeError("generation did not return first-step logits")
    # Element zero is the vocabulary distribution used to select the first
    # token after the prompt's final ``A:``.
    first_step_logits = generated.logits[0]
    max_top_k = max(top_ks)
    results = []

    for row, record in enumerate(records):
        query = record["query"]
        # Keep every target ID in the output to expose one-token versus
        # multi-token targets, while using ID zero for this baseline metric.
        country_ids = leading_space_token_ids(tokenizer, query["Fx"])
        capital_ids = leading_space_token_ids(tokenizer, query["GFx"])

        # Decode only newly generated tokens, then enforce the same textual stop
        # convention as the earlier Khandelwal-Pavlick evaluation port.
        continuation_ids = generated.sequences[row, prompt_width:]
        prediction = tokenizer.decode(continuation_ids, skip_special_tokens=True)
        prediction = prediction.split(STOP_SEQUENCE, maxsplit=1)[0]
        # Because the prompt ends at ``A:``, the expected continuation starts
        # with the whitespace preceding the capital.
        expected = f" {query['GFx']}"
        row_logits = first_step_logits[row]

        # These use the same distribution and differ only in target token:
        # intermediate country Fx versus correct final capital GFx.
        final_fx = token_measurement(row_logits, country_ids[0], top_ks)
        final_fx.update(
            {
                "token": tokenizer.decode([country_ids[0]]),
                "answer_token_ids": country_ids,
                "answer_num_tokens": len(country_ids),
            }
        )
        final_gfx = token_measurement(row_logits, capital_ids[0], top_ks)
        final_gfx.update(
            {
                "token": tokenizer.decode([capital_ids[0]]),
                "answer_token_ids": capital_ids,
                "answer_num_tokens": len(capital_ids),
            }
        )

        # Copy the manifest record instead of mutating the input object.
        result = dict(record)
        result["evaluation"] = {
            "prediction": prediction,
            "label": expected,
            "exact_match": prediction == expected,
            "final_next_token_readout": {
                "Fx_first_token": final_fx,
                "GFx_first_token": final_gfx,
                "top_tokens": top_tokens(row_logits, tokenizer, max_top_k),
            },
        }
        results.append(result)

    return results


def ensure_output_paths(paths: Sequence[Path], *, overwrite: bool) -> None:
    """Validate output destinations before loading the large model.

    Inputs:
        ``paths`` contains JSONL and summary destinations. ``overwrite`` says
        whether existing results may be replaced.
    Output:
        No return value. Creates missing parents or raises ``FileExistsError``.
    Role:
        Prevents an accidental rerun from destroying completed GPU results.
    """

    existing = [path for path in paths if path.exists()]
    if existing and not overwrite:
        names = ", ".join(str(path) for path in existing)
        raise FileExistsError(f"output already exists; use --overwrite: {names}")
    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)


def main() -> None:
    """Orchestrate one complete baseline-evaluation command.

    Input:
        Command-line configuration from ``parse_args`` and the manifest stored
        at ``args.input``.
    Output:
        Writes the per-prompt JSONL and aggregate summary JSON. Prints batch
        progress and the final summary; it returns no experiment value.
    Role and dependency flow:
        ``parse_args`` -> option/path validation -> model load ->
        ``read_manifest`` -> ``batched`` -> ``evaluate_batch`` ->
        ``RunningSummary.add`` -> ``RunningSummary.as_dict``.
    """

    args = parse_args()
    top_ks = validate_top_ks(args.top_k)
    ensure_output_paths(
        (args.output, args.summary_output), overwrite=args.overwrite
    )

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    # Load by immutable commit rather than relying on a moving model revision.
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID,
        revision=STAGE_ONE_COMMIT,
        padding_side="left",
    )
    if tokenizer.pad_token_id is None:
        # Batched causal generation needs a padding token. Reusing EOS changes
        # only padding; the attention mask prevents it from becoming context.
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        revision=STAGE_ONE_COMMIT,
        device_map="auto",
        dtype=torch.bfloat16,
    )
    model.eval()

    # These iterators are lazy, so at most one model batch is resident at once.
    records = read_manifest(
        args.input,
        start_index=args.start_index,
        num_records=args.num_records,
    )
    counters = RunningSummary(top_ks)

    # Results are written and flushed per batch. If a cluster job terminates,
    # rows from completed batches remain available for diagnosis.
    with args.output.open("w", encoding="utf-8") as output_handle:
        for batch_number, batch in enumerate(batched(records, args.batch_size), start=1):
            evaluated = evaluate_batch(
                model,
                tokenizer,
                batch,
                top_ks=top_ks,
                torch_module=torch,
            )
            for result in evaluated:
                output_handle.write(json.dumps(result, ensure_ascii=False) + "\n")
                counters.add(result)
            output_handle.flush()
            print(
                f"Batch {batch_number}: evaluated {counters.evaluated} prompt instances",
                flush=True,
            )

    # Store parameters alongside metrics so downstream comparisons know exactly
    # which checkpoint, row slice, batching, and measurement definition ran.
    summary = {
        "model": MODEL_ID,
        "stage_one_revision": STAGE_ONE_REVISION,
        "model_commit": STAGE_ONE_COMMIT,
        "dtype": MODEL_DTYPE,
        "input": str(args.input),
        "output": str(args.output),
        "start_index": args.start_index,
        "requested_num_records": args.num_records,
        "batch_size": args.batch_size,
        "max_new_tokens": MAX_NEW_TOKENS,
        "stop_sequence": STOP_SEQUENCE,
        "top_k_values": list(top_ks),
        "rank_scope": "full_vocabulary",
        "target_measurement": "first_token_with_leading_space",
        **counters.as_dict(),
    }
    args.summary_output.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))
    print(f"Wrote {args.output}")
    print(f"Wrote {args.summary_output}")


if __name__ == "__main__":
    main()
