"""Evaluate Khandelwal--Pavlick Logit Lens on correct prompt instances.

High-level purpose
==================
The behavioral baseline has already identified prompt instances for which
stage-one OLMo 3 generated the correct capital.  This program asks a separate
internal-representation question for each of those exact prompts:

    Across the final query's token positions and OLMo's 32 decoder blocks,
    how strongly can Logit Lens read out the landmark ``x``, intermediate
    country ``F(x)``, and correct capital ``G(F(x))``?

The intermediate-country result is then assigned to the same reciprocal-rank
bands used in the verified earlier experiment:

* compositional: peak reciprocal rank >= 0.5 (vocabulary rank 1 or 2);
* ambiguous: 0.2 < peak reciprocal rank < 0.5; and
* shortcut candidate: peak reciprocal rank <= 0.2 (rank 5 or worse).

These are evidence labels, not causal conclusions.  In particular,
``shortcut_candidate`` means that this particular Logit Lens measurement did
not strongly expose ``F(x)``; it does not prove that no compositional route was
used.

Input
=====
``--input`` is the JSONL written by ``filter_correct_baselines.py``.  Every row
must contain one exact-correct query-context instance, including:

* ``prompt_instance_id``: stable identity for this query and context;
* ``prompt``: the complete 10-demonstration ICL prompt;
* ``query``: strings for ``x``, ``Fx``, and ``GFx``; and
* ``evaluation.exact_match == true``: the already-computed behavioral result.

``--start-index`` and ``--num-records`` select a contiguous input slice, so a
later scheduler script can run independent shards without changing this code.

Output
======
``--output`` is JSONL with one row for every selected input row.  The original
row is preserved and receives a ``logit_lens`` field.

Paper-filter-eligible rows contain:

* first-token metadata for ``x``, ``Fx``, and ``GFx``;
* every selected target's raw logit, full-vocabulary rank, and reciprocal rank
  at every retained query position and layer;
* the per-layer processing signature (maximum RR over query positions);
* peak positions/layers; and
* the intermediate-country evidence classification.

Rows rejected by the authors' first-token-overlap filter are still written,
but are marked ``paper_token_eligible: false`` and are not sent through OLMo.
Keeping them makes the exclusion count and the correspondence with the 5,491
correct input instances auditable.

``--summary-output`` is regular JSON containing checkpoint provenance, run
parameters, paper-filter counts, and classification counts.

Functional flow
===============
1. ``parse_args`` reads paths, slice settings, and projection chunk size.
2. ``read_correct_records`` streams and validates the requested input rows.
3. ``node_token_info`` tokenizes all three task variables exactly as answer
   continuations, including their leading space.
4. ``paper_token_filter_reason`` reproduces the reference token-overlap filter.
5. ``first_query_token_index`` reproduces the reference right-to-left boundary
   calculation for the final ``landmark\nA:`` query segment.
6. ``analyze_record`` captures post-block residual activations, projects them
   with ``target_token_logits_and_ranks``, and summarizes each task node.
7. ``classify_reciprocal_rank`` labels the peak intermediate-country evidence.
8. ``RunningSummary`` accumulates counts while ``main`` writes and flushes each
   output row immediately.

This file performs no J-Lens calculation, Jacobian fitting, intervention, or
new text generation.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator, Literal

import torch

from evaluate_baseline import (
    MODEL_DTYPE,
    MODEL_ID,
    STAGE_ONE_COMMIT,
    STAGE_ONE_REVISION,
    ensure_output_paths,
)
from olmo3_logit_lens import (
    REFERENCE_CODE_COMMIT,
    capture_residual_stream,
    target_token_logits_and_ranks,
)


# A one-way landmark -> country -> capital task has exactly these three nodes.
NODES = ("x", "Fx", "GFx")
INTERMEDIATE_NODE = "Fx"

# These thresholds reproduce the earlier verified analysis.  They are kept as
# named constants so every output summary records one unambiguous definition.
COMPOSITION_RR_THRESHOLD = 0.5
SHORTCUT_RR_THRESHOLD = 0.2
EvidenceGroup = Literal["compositional", "ambiguous", "shortcut_candidate"]

PROJECT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = PROJECT_DIR / "results" / "correct_query_contexts.jsonl"
DEFAULT_OUTPUT = PROJECT_DIR / "results" / "logit_lens_evaluation.jsonl"
DEFAULT_SUMMARY = PROJECT_DIR / "results" / "logit_lens_evaluation_summary.json"


@dataclass
class RunningSummary:
    """Accumulate a mutually exclusive accounting of processed input rows.

    Input:
        No required arguments. All counters begin at zero.
    Output:
        ``as_dict`` returns serializable filter and evidence-group counts.
    Role:
        Lets ``main`` stream large JSONL outputs without retaining all results
        in memory, while verifying that every selected input row is accounted
        for exactly once.
    """

    input_records: int = 0
    eligible_records: int = 0
    excluded_records: int = 0
    group_counts: Counter[str] = field(default_factory=Counter)
    exclusion_counts: Counter[str] = field(default_factory=Counter)

    def add(self, result: dict[str, Any]) -> None:
        """Add one output record to the aggregate counters.

        Input:
            One row produced by ``excluded_result`` or ``analyze_record``.
        Output:
            No return value; updates this object's counters.
        """

        self.input_records += 1
        lens = result["logit_lens"]
        if lens["paper_token_eligible"]:
            self.eligible_records += 1
            self.group_counts[lens["classification"]["group"]] += 1
        else:
            self.excluded_records += 1
            self.exclusion_counts[lens["paper_token_filter_reason"]] += 1

    def as_dict(self) -> dict[str, Any]:
        """Return counts and validate that the categories form a partition."""

        if self.input_records != self.eligible_records + self.excluded_records:
            raise RuntimeError("eligible and excluded rows do not partition input")
        classified = sum(self.group_counts.values())
        if classified != self.eligible_records:
            raise RuntimeError("evidence groups do not partition eligible rows")
        return {
            "num_input_records": self.input_records,
            "num_paper_token_eligible": self.eligible_records,
            "num_paper_token_excluded": self.excluded_records,
            "paper_token_exclusion_reasons": dict(sorted(self.exclusion_counts.items())),
            "classification_counts": {
                group: self.group_counts[group]
                for group in ("compositional", "ambiguous", "shortcut_candidate")
            },
            "compositional_fraction_among_eligible": (
                self.group_counts["compositional"] / self.eligible_records
                if self.eligible_records
                else None
            ),
        }


def parse_args() -> argparse.Namespace:
    """Read paths, input slicing, memory, and overwrite options.

    Input:
        Command-line flags.
    Output:
        An ``argparse.Namespace`` consumed by ``main``.
    Role:
        Provides one interface for smoke tests, full runs, and scheduler shards.
    """

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument(
        "--num-records",
        type=int,
        default=None,
        help="Optional number of rows after --start-index.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=32,
        help="Number of flattened position-layer activations projected at once.",
    )
    parser.add_argument("--progress-every", type=int, default=10)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def validate_correct_record(record: dict[str, Any], line_number: int) -> None:
    """Require the identity, prompt, task nodes, and exact-correct baseline.

    Input:
        One decoded JSON object and its one-based physical line number.
    Output:
        No value when valid; raises ``ValueError`` on malformed or non-correct
        input so lens results cannot silently include an unintended population.
    """

    required = {"prompt_instance_id", "prompt", "query", "evaluation"}
    missing = required - record.keys()
    if missing:
        raise ValueError(f"input line {line_number} is missing: {sorted(missing)}")
    if not isinstance(record["prompt_instance_id"], str):
        raise ValueError(f"input line {line_number} prompt_instance_id is not text")
    if not isinstance(record["prompt"], str):
        raise ValueError(f"input line {line_number} prompt is not text")
    query = record["query"]
    if not isinstance(query, dict):
        raise ValueError(f"input line {line_number} query is not an object")
    missing_nodes = set(NODES) - query.keys()
    if missing_nodes:
        raise ValueError(
            f"input line {line_number} query is missing: {sorted(missing_nodes)}"
        )
    evaluation = record["evaluation"]
    if not isinstance(evaluation, dict):
        raise ValueError(f"input line {line_number} evaluation is not an object")
    if evaluation.get("exact_match") is not True:
        raise ValueError(f"input line {line_number} is not exact-correct")


def read_correct_records(
    path: Path,
    *,
    start_index: int = 0,
    num_records: int | None = None,
) -> Iterator[dict[str, Any]]:
    """Stream a validated contiguous slice of correct baseline JSONL.

    Inputs:
        ``path`` is the input JSONL. ``start_index`` skips physical rows;
        ``num_records`` optionally limits the number subsequently yielded.
    Output:
        An iterator of validated dictionaries in stable input order.
    """

    if start_index < 0:
        raise ValueError("start_index must be non-negative")
    if num_records is not None and num_records <= 0:
        raise ValueError("num_records must be positive when supplied")

    yielded = 0
    seen_ids: set[str] = set()
    with path.open(encoding="utf-8") as handle:
        for zero_based_index, line in enumerate(handle):
            if zero_based_index < start_index:
                continue
            if num_records is not None and yielded >= num_records:
                break
            if not line.strip():
                raise ValueError(f"input line {zero_based_index + 1} is empty")
            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError(f"input line {zero_based_index + 1} is not an object")
            validate_correct_record(record, zero_based_index + 1)
            prompt_id = record["prompt_instance_id"]
            if prompt_id in seen_ids:
                raise ValueError(f"duplicate prompt_instance_id in slice: {prompt_id!r}")
            seen_ids.add(prompt_id)
            yielded += 1
            yield record


def leading_space_token_ids(tokenizer: Any, text: str) -> list[int]:
    """Tokenize a task value in the form expected immediately after ``A:``.

    Input:
        The OLMo tokenizer and a node value such as ``"Germany"``.
    Output:
        Vocabulary IDs for ``" Germany"``; never an empty list.
    Role:
        Matches the reference task's leading-space convention and preserves
        all IDs for overlap auditing, even though the lens target is ID zero.
    """

    token_ids = tokenizer.encode(f" {text}", add_special_tokens=False)
    if not token_ids:
        raise ValueError(f"task value has no tokenizer tokens: {text!r}")
    return [int(token_id) for token_id in token_ids]


def node_token_info(tokenizer: Any, query: dict[str, str]) -> dict[str, dict]:
    """Build auditable first-token metadata for ``x``, ``Fx``, and ``GFx``.

    Input:
        OLMo tokenizer and one query dictionary.
    Output:
        A node-keyed dictionary containing the original value, complete token
        ID sequence, decoded pieces, and first target token.
    Role:
        Supplies both the paper filter and Logit Lens target token IDs.
    """

    info: dict[str, dict] = {}
    for node in NODES:
        token_ids = leading_space_token_ids(tokenizer, query[node])
        info[node] = {
            "value": query[node],
            "token_ids": token_ids,
            "tokens": [tokenizer.decode([token_id]) for token_id in token_ids],
            "num_tokens": len(token_ids),
            "first_token_id": token_ids[0],
            "first_token": tokenizer.decode([token_ids[0]]),
        }
    return info


def paper_token_filter_reason(token_info: dict[str, dict]) -> str | None:
    """Apply the authors' two first-token-overlap exclusions.

    Input:
        Output of ``node_token_info``.
    Output:
        ``None`` when eligible. Otherwise a stable reason string.
    Role:
        Avoids treating a shared token identity as evidence that the model
        internally represented a different compositional node.
    """

    first_tokens = [token_info[node]["first_token_id"] for node in NODES]
    if len(first_tokens) != len(set(first_tokens)):
        return "node_first_tokens_overlap"

    non_x_first_tokens = {
        token_info[node]["first_token_id"] for node in NODES if node != "x"
    }
    if non_x_first_tokens & set(token_info["x"]["token_ids"]):
        return "target_first_token_occurs_inside_x"
    return None


def first_query_token_index(tokenizer: Any, prompt: str, x: str) -> int:
    """Locate the reference implementation's first retained query token.

    Inputs:
        OLMo tokenizer, complete ICL prompt, and final landmark string ``x``.
    Output:
        Zero-based token index at which the suffix ``x + "\\nA:"`` begins.
    Role:
        Reproduces Khandelwal--Pavlick's right-to-left decoded-character
        boundary instead of analyzing all demonstration-token activations.
    """

    expected_suffix = f"Q: {x}\nA:"
    if not prompt.endswith(expected_suffix):
        raise ValueError(
            f"prompt does not end with expected final query: {expected_suffix!r}"
        )

    characters_remaining = len(f"{x}\nA:")
    prompt_token_ids = tokenizer.encode(prompt, add_special_tokens=False)
    for token_index in range(len(prompt_token_ids) - 1, -1, -1):
        # This deliberately mirrors the paper code rather than introducing a
        # different offset-mapping convention.
        characters_remaining -= len(tokenizer.decode(prompt_token_ids[token_index]))
        if characters_remaining <= 0:
            return token_index
    raise ValueError("could not locate final query tokens in prompt")


def classify_reciprocal_rank(reciprocal_rank: float) -> EvidenceGroup:
    """Map peak intermediate-country RR to the predefined evidence bands."""

    if not 0.0 <= reciprocal_rank <= 1.0:
        raise ValueError("reciprocal_rank must be between zero and one")
    if reciprocal_rank >= COMPOSITION_RR_THRESHOLD:
        return "compositional"
    if reciprocal_rank <= SHORTCUT_RR_THRESHOLD:
        return "shortcut_candidate"
    return "ambiguous"


def summarize_node_evidence(
    target_logits: torch.Tensor,
    ranks: torch.Tensor,
    token_info: dict[str, dict],
    *,
    prompt_position_offset: int,
) -> dict[str, dict]:
    """Convert ``[P,L,K]`` tensors into node-keyed JSON measurements.

    Inputs:
        Raw selected logits and one-based full-vocabulary ranks with identical
        shape ``[P,L,3]``; target metadata; and the first retained token's
        absolute prompt position.
    Output:
        For each task node: all positionwise/layerwise logits, ranks and RRs;
        the layerwise maximum RR processing signature; and peak locations.
    Role:
        Preserves the detailed measurements needed for later correlation and
        intervention analyses while calculating the exact paper summary.
    """

    expected_shape = target_logits.shape
    if target_logits.ndim != 3 or expected_shape[2] != len(NODES):
        raise ValueError("target_logits must have shape [positions, layers, 3]")
    if ranks.shape != expected_shape:
        raise ValueError("ranks must have the same shape as target_logits")
    if (ranks < 1).any():
        raise ValueError("all vocabulary ranks must be one-based positive values")

    reciprocal_ranks = 1.0 / ranks.float()
    evidence: dict[str, dict] = {}
    for node_index, node in enumerate(NODES):
        node_logits = target_logits[:, :, node_index].float()
        node_ranks = ranks[:, :, node_index].long()
        node_rr = reciprocal_ranks[:, :, node_index]

        # This maximum over query positions is the paper's layerwise processing
        # signature. A second maximum finds the strongest layer overall.
        layerwise_max_rr = node_rr.max(dim=0).values
        peak_rr = float(layerwise_max_rr.max().item())
        best_rank = int(node_ranks.min().item())
        peak_locations = (node_rr == peak_rr).nonzero(as_tuple=False)
        peak_layers = sorted({int(location[1]) for location in peak_locations})

        evidence[node] = {
            **token_info[node],
            "positionwise_layerwise_logits": node_logits.tolist(),
            "positionwise_layerwise_ranks": node_ranks.tolist(),
            "positionwise_layerwise_reciprocal_ranks": node_rr.tolist(),
            "layerwise_max_reciprocal_rank": layerwise_max_rr.tolist(),
            "peak_reciprocal_rank": peak_rr,
            # Read this directly from integer ranks rather than reconstructing
            # it from a rounded float reciprocal rank.
            "best_vocabulary_rank": best_rank,
            "peak_layers": peak_layers,
            "first_peak_layer": peak_layers[0],
            "peak_locations": [
                {
                    "query_position": int(location[0]),
                    "prompt_position": prompt_position_offset + int(location[0]),
                    "layer": int(location[1]),
                }
                for location in peak_locations
            ],
        }
    return evidence


def intermediate_classification(evidence: dict[str, dict]) -> dict[str, Any]:
    """Build the auditable classification object from ``Fx`` evidence."""

    intermediate = evidence[INTERMEDIATE_NODE]
    peak_rr = float(intermediate["peak_reciprocal_rank"])
    group = classify_reciprocal_rank(peak_rr)
    return {
        "group": group,
        "intermediate_node": INTERMEDIATE_NODE,
        "intermediate_value": intermediate["value"],
        "peak_reciprocal_rank": peak_rr,
        "best_vocabulary_rank": intermediate["best_vocabulary_rank"],
        "peak_layers": intermediate["peak_layers"],
        "first_peak_layer": intermediate["first_peak_layer"],
        "composition_rr_threshold": COMPOSITION_RR_THRESHOLD,
        "shortcut_rr_threshold": SHORTCUT_RR_THRESHOLD,
    }


def excluded_result(
    record: dict[str, Any],
    token_info: dict[str, dict],
    reason: str,
) -> dict[str, Any]:
    """Preserve a filter-excluded input row without running the model."""

    result = dict(record)
    result["logit_lens"] = {
        "paper_token_eligible": False,
        "paper_token_filter_reason": reason,
        "node_token_info": token_info,
        "classification": None,
        "node_evidence": None,
    }
    return result


def analyze_record(
    model: Any,
    tokenizer: Any,
    record: dict[str, Any],
    token_info: dict[str, dict],
    *,
    chunk_size: int,
) -> dict[str, Any]:
    """Run the complete Logit Lens calculation for one eligible prompt.

    Inputs:
        Loaded model/tokenizer; one validated exact-correct input row; its
        token metadata; and the projection chunk size.
    Output:
        A copy of the input row with detailed ``logit_lens`` measurements.
    Role:
        Connects prompt position selection, activation capture, optimized
        full-vocabulary ranking, node summarization, and classification.
    """

    prompt = record["prompt"]
    query_start = first_query_token_index(
        tokenizer, prompt, record["query"]["x"]
    )
    model_inputs = tokenizer(
        [prompt],
        return_tensors="pt",
        return_token_type_ids=False,
    )
    input_device = model.get_input_embeddings().weight.device
    model_inputs = {
        name: tensor.to(input_device) for name, tensor in model_inputs.items()
    }

    # The complete prompt is processed, but only final-query rows are retained.
    residual_stream = capture_residual_stream(
        model,
        model_inputs,
        position_slice=slice(query_start, None),
    )
    target_logits, ranks = target_token_logits_and_ranks(
        model,
        residual_stream,
        [token_info[node]["first_token_id"] for node in NODES],
        chunk_size=chunk_size,
    )
    evidence = summarize_node_evidence(
        target_logits,
        ranks,
        token_info,
        prompt_position_offset=query_start,
    )

    result = dict(record)
    result["logit_lens"] = {
        "paper_token_eligible": True,
        "paper_token_filter_reason": None,
        "query_token_start": query_start,
        "num_query_positions": int(residual_stream.shape[0]),
        "num_layers": int(residual_stream.shape[1]),
        "layer_index_definition": "post_decoder_block_zero_based",
        "rank_scope": "complete_vocabulary",
        "target_definition": "leading_space_first_token",
        "position_summary": "maximum_reciprocal_rank_over_query_positions",
        "classification": intermediate_classification(evidence),
        "node_evidence": evidence,
    }
    return result


def main() -> None:
    """Load the pinned model, stream records, and write lens results."""

    args = parse_args()
    if args.chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if args.progress_every <= 0:
        raise ValueError("progress_every must be positive")
    ensure_output_paths(
        (args.output, args.summary_output), overwrite=args.overwrite
    )

    # Heavy imports and model loading remain inside main so unit tests can
    # exercise every data/measurement helper without allocating a 7B model.
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID,
        revision=STAGE_ONE_COMMIT,
    )
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        revision=STAGE_ONE_COMMIT,
        device_map="auto",
        dtype=torch.bfloat16,
    )
    model.eval()

    records = read_correct_records(
        args.input,
        start_index=args.start_index,
        num_records=args.num_records,
    )
    counters = RunningSummary()

    # Flush every row so a terminated cluster job retains completed work for
    # diagnosis. Existing outputs are protected unless --overwrite is explicit.
    with args.output.open("w", encoding="utf-8") as output_handle:
        for record in records:
            token_info = node_token_info(tokenizer, record["query"])
            exclusion_reason = paper_token_filter_reason(token_info)
            if exclusion_reason is None:
                result = analyze_record(
                    model,
                    tokenizer,
                    record,
                    token_info,
                    chunk_size=args.chunk_size,
                )
            else:
                result = excluded_result(record, token_info, exclusion_reason)

            output_handle.write(json.dumps(result, ensure_ascii=False) + "\n")
            output_handle.flush()
            counters.add(result)
            if counters.input_records % args.progress_every == 0:
                print(
                    f"Processed {counters.input_records} selected input records",
                    flush=True,
                )

    summary = {
        "model": MODEL_ID,
        "stage_one_revision": STAGE_ONE_REVISION,
        "model_commit": STAGE_ONE_COMMIT,
        "dtype": MODEL_DTYPE,
        "reference_code_commit": REFERENCE_CODE_COMMIT,
        "input": str(args.input),
        "output": str(args.output),
        "start_index": args.start_index,
        "requested_num_records": args.num_records,
        "chunk_size": args.chunk_size,
        "nodes": list(NODES),
        "intermediate_node": INTERMEDIATE_NODE,
        "rank_scope": "complete_vocabulary",
        "target_definition": "leading_space_first_token",
        "query_positions": "tokens_covering_x_plus_newline_A_colon",
        "layers": "all_32_post_decoder_block_outputs",
        "processing_signature": "maximum_RR_over_query_positions_per_layer",
        "overall_evidence": "maximum_RR_over_query_positions_and_layers",
        "composition_rr_threshold": COMPOSITION_RR_THRESHOLD,
        "shortcut_rr_threshold": SHORTCUT_RR_THRESHOLD,
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
