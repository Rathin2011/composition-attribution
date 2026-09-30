"""Run causal J-Lens interventions on landmark-country-capital queries.

The runner compares an ordinary OLMo 3 stage-one forward/generation pass with
one in which the correct intermediate country's J-Lens direction is edited at
selected layers during the initial prompt pass.  It supports:

* full or partial projection-out (``ablate``); and
* signed additive steering (``steer``); and
* coordinate swapping from the true country to a replacement country
  (``swap``).

By default, only queries whose intermediate country is exactly one tokenizer
token are evaluated.  The basic J-Lens vector is token-specific, so treating
the first token of a multi-token country as the complete intermediate would
change the scientific claim.

Inputs
------
* Saved correctly answered compositional and shortcut-candidate query JSONL.
* The merged 1,000-prompt Jacobian lens.
* The pinned OLMo 3 stage-one checkpoint.

Outputs
-------
* ``per_query.jsonl`` with baseline/intervened logits, probabilities, ranks,
  generated answers, and changes for every evaluated query.
* ``summary.json`` with settings and group-level aggregate effects.
"""

from __future__ import annotations

import argparse
from contextlib import ExitStack
import json
import math
import os
from pathlib import Path
import statistics
import sys
from typing import Any, Iterable, Sequence

from .compatibility import MODEL_COMMIT, MODEL_ID, MODEL_REVISION, VENDORED_JLENS
from .evaluate_landmarks import (
    DEFAULT_GROUP_FILES,
    DEFAULT_LENS,
    EXPECTED_COUNTS,
    read_group,
)
from .fit_jlens import DEFAULT_LAYERS
from .interventions import LayerIntervention, jlens_token_direction


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "results" / "interventions"
GROUP_ARGUMENTS = {
    "compositional": ("compositional", DEFAULT_GROUP_FILES["compositional"]),
    "shortcut_candidate": (
        "shortcut_candidate",
        DEFAULT_GROUP_FILES["shortcut_candidate"],
    ),
}
STOP_SEQUENCE = "\n\n"
DEFAULT_SWAP_TARGET_COUNTRY = "Japan"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--groups",
        nargs="+",
        choices=tuple(GROUP_ARGUMENTS),
        default=list(GROUP_ARGUMENTS),
    )
    parser.add_argument("--compositional", type=Path, default=DEFAULT_GROUP_FILES["compositional"])
    parser.add_argument("--shortcut", type=Path, default=DEFAULT_GROUP_FILES["shortcut_candidate"])
    parser.add_argument("--lens", type=Path, default=DEFAULT_LENS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--layers", type=int, nargs="+", default=list(DEFAULT_LAYERS))
    parser.add_argument(
        "--token-scope",
        choices=("final", "query", "all"),
        default="final",
        help="Edit the final ':' token, all final-query tokens, or all prompt tokens.",
    )
    parser.add_argument(
        "--kind",
        choices=("ablate", "steer", "swap"),
        default="ablate",
    )
    parser.add_argument(
        "--strength",
        type=float,
        help="Ablation fraction in [0,1]; defaults to 1 (full projection-out).",
    )
    parser.add_argument(
        "--coefficient",
        type=float,
        help="Required signed alpha for steering; invalid for ablation.",
    )
    parser.add_argument(
        "--swap-target-country",
        default=DEFAULT_SWAP_TARGET_COUNTRY,
        help=(
            "Replacement country for coordinate swapping (default: Japan). "
            "It must be represented by one tokenizer token."
        ),
    )
    parser.add_argument(
        "--swap-scale",
        type=float,
        help="Coordinate-swap update scale; defaults to 1 (a full swap).",
    )
    parser.add_argument("--max-new-tokens", type=int, default=20)
    parser.add_argument("--max-seq-len", type=int, default=512)
    parser.add_argument("--progress-every", type=int, default=10)
    parser.add_argument("--max-queries", type=int)
    parser.add_argument(
        "--allow-multitoken-country",
        action="store_true",
        help="Use the first country token as the intervention target.",
    )
    parser.add_argument(
        "--allow-download",
        action="store_true",
        help="Allow Hugging Face downloads instead of requiring cached files.",
    )
    return parser.parse_args()


def validate_settings(args: argparse.Namespace, lens_layers: Sequence[int]) -> dict[str, Any]:
    """Validate CLI settings and return their canonical representation."""

    layers = sorted(set(args.layers))
    if not layers:
        raise ValueError("at least one intervention layer is required")
    missing = sorted(set(layers) - set(lens_layers))
    if missing:
        raise ValueError(
            f"layers {missing} are absent from the fitted lens; available="
            f"{sorted(lens_layers)}"
        )
    if args.kind == "ablate":
        if args.coefficient is not None:
            raise ValueError("--coefficient is only valid for steering")
        if args.swap_scale is not None:
            raise ValueError("--swap-scale is only valid for swapping")
        strength = 1.0 if args.strength is None else args.strength
        if not 0.0 <= strength <= 1.0:
            raise ValueError("ablation strength must lie in [0,1]")
        coefficient = None
        swap_scale = None
        swap_target_country = None
    elif args.kind == "steer":
        if args.strength is not None:
            raise ValueError("--strength is only valid for ablation")
        if args.swap_scale is not None:
            raise ValueError("--swap-scale is only valid for swapping")
        if args.coefficient is None:
            raise ValueError("steering requires --coefficient")
        strength = None
        coefficient = args.coefficient
        swap_scale = None
        swap_target_country = None
    else:
        if args.strength is not None or args.coefficient is not None:
            raise ValueError("swapping does not accept --strength or --coefficient")
        if not args.swap_target_country.strip():
            raise ValueError("--swap-target-country must not be empty")
        strength = None
        coefficient = None
        swap_scale = 1.0 if args.swap_scale is None else args.swap_scale
        if not math.isfinite(swap_scale) or swap_scale < 0.0:
            raise ValueError("swap scale must be finite and non-negative")
        swap_target_country = args.swap_target_country.strip()
    for name in ("max_new_tokens", "max_seq_len", "progress_every"):
        if getattr(args, name) < 1:
            raise ValueError(f"{name} must be positive")
    if args.max_queries is not None and args.max_queries < 1:
        raise ValueError("max_queries must be positive when provided")
    return {
        "kind": args.kind,
        "layers": layers,
        "token_scope": args.token_scope,
        "strength": strength,
        "coefficient": coefficient,
        "swap_scale": swap_scale,
        "swap_target_country": swap_target_country,
        "single_token_countries_only": not args.allow_multitoken_country,
        "max_new_tokens": args.max_new_tokens,
        "max_seq_len": args.max_seq_len,
    }


def country_capital_pairs(records: Iterable[dict[str, Any]]) -> dict[str, str]:
    """Collect and validate the country-to-capital relation in saved rows."""

    pairs: dict[str, str] = {}
    for record in records:
        for example in [*record["context"], record["query"]]:
            country = example["Fx"]
            capital = example["GFx"]
            previous = pairs.setdefault(country, capital)
            if previous != capital:
                raise ValueError(
                    f"country {country!r} has conflicting capitals: "
                    f"{previous!r} and {capital!r}"
                )
    return pairs


def resolve_swap_target(
    requested_country: str,
    country_capitals: dict[str, str],
) -> tuple[str, str]:
    """Resolve a case-insensitive swap target to its canonical name/capital."""

    matches = [
        country
        for country in country_capitals
        if country.casefold() == requested_country.strip().casefold()
    ]
    if len(matches) != 1:
        available = ", ".join(sorted(country_capitals))
        raise ValueError(
            f"swap target {requested_country!r} is not a unique country in the "
            f"saved task data; available countries: {available}"
        )
    country = matches[0]
    return country, country_capitals[country]


def _label_token_ids(tokenizer: Any, value: str) -> list[int]:
    """Tokenize a task value with the leading space used by answer labels."""

    encoded = tokenizer(
        f" {value}",
        add_special_tokens=False,
        return_token_type_ids=False,
    )
    token_ids = encoded["input_ids"]
    if not token_ids:
        raise ValueError(f"value {value!r} tokenized to an empty sequence")
    return token_ids


def load_queries(
    args: argparse.Namespace,
) -> tuple[
    list[tuple[str, dict[str, Any]]],
    dict[str, int],
    dict[str, str],
]:
    """Load requested groups and filter scientifically ambiguous countries."""

    paths = {
        "compositional": args.compositional,
        "shortcut_candidate": args.shortcut,
    }
    selected: list[tuple[str, dict[str, Any]]] = []
    skipped = {"multitoken_country": 0, "source_equals_swap_target": 0}
    all_records: list[dict[str, Any]] = []
    for group in args.groups:
        records = read_group(paths[group], group, EXPECTED_COUNTS[group])
        all_records.extend(records)
        for record in records:
            country_tokens = record["node_evidence"]["Fx"]["token_ids"]
            if len(country_tokens) != 1 and not args.allow_multitoken_country:
                skipped["multitoken_country"] += 1
                continue
            if (
                args.kind == "swap"
                and record["query"]["Fx"].casefold()
                == args.swap_target_country.strip().casefold()
            ):
                skipped["source_equals_swap_target"] += 1
                continue
            selected.append((group, record))
    if args.max_queries is not None:
        selected = selected[: args.max_queries]
    if not selected:
        raise ValueError("no queries remain after filtering")
    identities = [
        (group, record["evaluation_index"], record["dataset_index"])
        for group, record in selected
    ]
    if len(identities) != len(set(identities)):
        raise ValueError("query identities overlap within the selected inputs")
    return selected, skipped, country_capital_pairs(all_records)


def intervention_positions(record: dict[str, Any], scope: str) -> tuple[int, ...] | None:
    """Translate a named intervention scope into prompt-token positions."""

    if scope == "final":
        return (-1,)
    if scope == "query":
        start = record["query_token_start"]
        count = record["num_query_positions"]
        return tuple(range(start, start + count))
    if scope == "all":
        return None
    raise ValueError(f"unsupported token scope: {scope!r}")


def token_measurement(logits: Any, token_id: int) -> dict[str, Any]:
    """Convert one vocabulary-logit vector into target-specific measurements."""

    if logits.ndim != 1:
        raise ValueError("logits must have shape [vocabulary]")
    if not 0 <= token_id < logits.shape[0]:
        raise ValueError("token_id is outside the vocabulary")
    float_logits = logits.float()
    target_logit = float_logits[token_id]
    log_probability = float_logits.log_softmax(dim=-1)[token_id]
    rank = 1 + int((float_logits > target_logit).sum().item())
    return {
        "token_id": token_id,
        "logit": float(target_logit.item()),
        "log_probability": float(log_probability.item()),
        "probability": float(log_probability.exp().item()),
        "rank": rank,
    }


def answer_from_completion(completion: str) -> str:
    """Apply the same double-newline answer boundary as task evaluation."""

    return completion.split(STOP_SEQUENCE, maxsplit=1)[0]


def greedy_completion(
    model: Any,
    tokenizer: Any,
    input_ids: Any,
    *,
    max_new_tokens: int,
    interventions: Iterable[LayerIntervention] = (),
) -> tuple[Any, str]:
    """Generate greedily while applying interventions only to the prompt pass.

    The initial pass is run with KV caching while the hooks are active.  The
    hooks are then removed, and subsequent answer tokens are decoded from the
    resulting intervened cache.  The returned logits are the initial
    next-token logits, before choosing the first answer token.
    """

    import torch

    generated: list[int] = []
    with torch.inference_mode():
        with ExitStack() as stack:
            for intervention in interventions:
                stack.enter_context(intervention)
            output = model(input_ids=input_ids, use_cache=True)
        first_logits = output.logits[0, -1].detach()
        past_key_values = output.past_key_values

        next_token = first_logits.argmax(dim=-1).reshape(1, 1)
        for step in range(max_new_tokens):
            token_id = int(next_token.item())
            generated.append(token_id)
            completion = tokenizer.decode(
                generated,
                skip_special_tokens=True,
                clean_up_tokenization_spaces=False,
            )
            if token_id == tokenizer.eos_token_id or STOP_SEQUENCE in completion:
                break
            if step + 1 == max_new_tokens:
                break
            output = model(
                input_ids=next_token,
                past_key_values=past_key_values,
                use_cache=True,
            )
            past_key_values = output.past_key_values
            next_token = output.logits[0, -1].argmax(dim=-1).reshape(1, 1)

    return first_logits, tokenizer.decode(
        generated,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )


def summarize_group(rows: Sequence[dict[str, Any]], group: str) -> dict[str, Any]:
    """Aggregate behavioral and probability effects for one query group."""

    selected = [row for row in rows if row["group"] == group]
    if not selected:
        return {"num_queries": 0}
    deltas = [row["change"] for row in selected]
    summary = {
        "num_queries": len(selected),
        "baseline_exact": sum(row["baseline"]["exact_match"] for row in selected),
        "intervention_exact": sum(
            row["intervention"]["exact_match"] for row in selected
        ),
        "generated_answer_changed": sum(item["generated_answer_changed"] for item in deltas),
        "mean_correct_token_logit_change": statistics.mean(
            item["correct_token_logit"] for item in deltas
        ),
        "mean_correct_token_log_probability_change": statistics.mean(
            item["correct_token_log_probability"] for item in deltas
        ),
        "mean_correct_token_probability_change": statistics.mean(
            item["correct_token_probability"] for item in deltas
        ),
    }
    if selected[0].get("swap_target") is not None:
        summary.update(
            {
                "swap_target_exact": sum(
                    row["intervention"]["swap_target_exact_match"]
                    for row in selected
                ),
                "mean_swap_target_token_log_probability_change": statistics.mean(
                    item["swap_target_token_log_probability"] for item in deltas
                ),
            }
        )
    return summary


def atomic_write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    """Write JSONL atomically so interrupted jobs do not look complete."""

    temporary = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    try:
        with temporary.open("w", encoding="utf-8") as handle:
            for record in records:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _import_runtime() -> tuple[Any, Any, Any, Any]:
    if not (VENDORED_JLENS / "jlens" / "__init__.py").is_file():
        raise FileNotFoundError(f"missing official J-Lens checkout: {VENDORED_JLENS}")
    sys.path.insert(0, str(VENDORED_JLENS))
    import jlens
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    return jlens, torch, AutoModelForCausalLM, AutoTokenizer


def run(args: argparse.Namespace) -> dict[str, Any]:
    """Run baseline/intervened inference and save per-query and aggregate data."""

    jlens, torch, model_class, tokenizer_class = _import_runtime()
    lens = jlens.JacobianLens.load(str(args.lens))
    settings = validate_settings(args, lens.source_layers)
    queries, skipped, country_capitals = load_queries(args)

    output_dir = args.output_dir
    rows_path = output_dir / "per_query.jsonl"
    summary_path = output_dir / "summary.json"
    if rows_path.exists() or summary_path.exists():
        raise FileExistsError("completed intervention output already exists")

    tokenizer = tokenizer_class.from_pretrained(
        MODEL_ID,
        revision=MODEL_COMMIT,
        local_files_only=not args.allow_download,
    )
    swap_target: dict[str, Any] | None = None
    if settings["kind"] == "swap":
        target_country, target_capital = resolve_swap_target(
            settings["swap_target_country"],
            country_capitals,
        )
        target_country_token_ids = _label_token_ids(tokenizer, target_country)
        if len(target_country_token_ids) != 1:
            raise ValueError(
                f"swap target country {target_country!r} has "
                f"{len(target_country_token_ids)} tokens; basic J-Lens swapping "
                "requires exactly one"
            )
        target_capital_token_ids = _label_token_ids(tokenizer, target_capital)
        swap_target = {
            "country": target_country,
            "country_token_id": target_country_token_ids[0],
            "capital": target_capital,
            "capital_label": f" {target_capital}",
            "capital_first_token_id": target_capital_token_ids[0],
        }
        settings["swap_target_country"] = target_country
        settings["swap_target_capital"] = target_capital

    model = model_class.from_pretrained(
        MODEL_ID,
        revision=MODEL_COMMIT,
        dtype=torch.bfloat16,
        device_map="auto",
        local_files_only=not args.allow_download,
    )
    adapter = jlens.from_hf(model, tokenizer, compile=False, force_bos=False)
    lens.jacobians = {
        layer: matrix.to(adapter.input_device)
        for layer, matrix in lens.jacobians.items()
    }
    output_embedding = model.get_output_embeddings().weight
    direction_cache: dict[tuple[int, int], Any] = {}

    rows: list[dict[str, Any]] = []
    for group, record in queries:
        prompt = record["prediction"]["prompt"]
        encoded = tokenizer(
            prompt,
            return_tensors="pt",
            return_token_type_ids=False,
        )
        input_ids = encoded.input_ids.to(adapter.input_device)
        if input_ids.shape[1] > settings["max_seq_len"]:
            raise ValueError(
                f"prompt exceeds max_seq_len for evaluation_index="
                f"{record['evaluation_index']}"
            )
        query_end = record["query_token_start"] + record["num_query_positions"]
        if query_end != input_ids.shape[1]:
            raise ValueError(
                "saved final-query positions do not end at the prompt boundary for "
                f"evaluation_index={record['evaluation_index']}"
            )

        country_token_ids = record["node_evidence"]["Fx"]["token_ids"]
        country_token_id = country_token_ids[0]
        correct_token_id = record["node_evidence"]["GFx"]["first_token_id"]
        positions = intervention_positions(record, settings["token_scope"])

        baseline_logits, baseline_completion = greedy_completion(
            model,
            tokenizer,
            input_ids,
            max_new_tokens=settings["max_new_tokens"],
        )

        layer_interventions: list[LayerIntervention] = []
        for layer in settings["layers"]:
            cache_key = (layer, country_token_id)
            if cache_key not in direction_cache:
                direction_cache[cache_key] = jlens_token_direction(
                    lens.jacobians[layer],
                    output_embedding[country_token_id],
                )
            target_direction = None
            if swap_target is not None:
                target_cache_key = (layer, swap_target["country_token_id"])
                if target_cache_key not in direction_cache:
                    direction_cache[target_cache_key] = jlens_token_direction(
                        lens.jacobians[layer],
                        output_embedding[swap_target["country_token_id"]],
                    )
                target_direction = direction_cache[target_cache_key]
            layer_interventions.append(
                LayerIntervention(
                    adapter.layers,
                    layer_index=layer,
                    token_positions=positions,
                    direction=direction_cache[cache_key],
                    kind=settings["kind"],
                    coefficient=settings["coefficient"],
                    strength=settings["strength"],
                    target_direction=target_direction,
                    swap_scale=settings["swap_scale"],
                )
            )

        intervention_logits, intervention_completion = greedy_completion(
            model,
            tokenizer,
            input_ids,
            max_new_tokens=settings["max_new_tokens"],
            interventions=layer_interventions,
        )
        baseline_answer = answer_from_completion(baseline_completion)
        intervention_answer = answer_from_completion(intervention_completion)
        correct_answer = record["prediction"]["label"]
        baseline_correct = token_measurement(baseline_logits, correct_token_id)
        intervention_correct = token_measurement(
            intervention_logits,
            correct_token_id,
        )
        baseline_country = token_measurement(baseline_logits, country_token_id)
        intervention_country = token_measurement(
            intervention_logits,
            country_token_id,
        )
        baseline_swap_target = None
        intervention_swap_target = None
        swap_target_exact_match = None
        if swap_target is not None:
            baseline_swap_target = token_measurement(
                baseline_logits,
                swap_target["capital_first_token_id"],
            )
            intervention_swap_target = token_measurement(
                intervention_logits,
                swap_target["capital_first_token_id"],
            )
            swap_target_exact_match = (
                intervention_answer == swap_target["capital_label"]
            )
        rows.append(
            {
                "evaluation_index": record["evaluation_index"],
                "dataset_index": record["dataset_index"],
                "group": group,
                "query": record["query"],
                "country_token_count": len(country_token_ids),
                "country_target_token_id": country_token_id,
                "country_target_token": tokenizer.decode(
                    [country_token_id], clean_up_tokenization_spaces=False
                ),
                "swap_target": swap_target,
                "correct_answer_first_token_id": correct_token_id,
                "intervention_settings": {
                    "kind": settings["kind"],
                    "layers": settings["layers"],
                    "token_scope": settings["token_scope"],
                    "positions": positions,
                    "strength": settings["strength"],
                    "coefficient": settings["coefficient"],
                    "swap_scale": settings["swap_scale"],
                },
                "baseline": {
                    "completion": baseline_completion,
                    "answer": baseline_answer,
                    "exact_match": baseline_answer == correct_answer,
                    "correct_answer_first_token": baseline_correct,
                    "country_token": baseline_country,
                    "swap_target_answer_first_token": baseline_swap_target,
                },
                "intervention": {
                    "completion": intervention_completion,
                    "answer": intervention_answer,
                    "exact_match": intervention_answer == correct_answer,
                    "correct_answer_first_token": intervention_correct,
                    "country_token": intervention_country,
                    "swap_target_answer_first_token": intervention_swap_target,
                    "swap_target_exact_match": swap_target_exact_match,
                },
                "change": {
                    "correct_token_logit": (
                        intervention_correct["logit"] - baseline_correct["logit"]
                    ),
                    "correct_token_log_probability": (
                        intervention_correct["log_probability"]
                        - baseline_correct["log_probability"]
                    ),
                    "correct_token_probability": (
                        intervention_correct["probability"]
                        - baseline_correct["probability"]
                    ),
                    "correct_token_rank": (
                        intervention_correct["rank"] - baseline_correct["rank"]
                    ),
                    "country_token_log_probability": (
                        intervention_country["log_probability"]
                        - baseline_country["log_probability"]
                    ),
                    "generated_answer_changed": intervention_answer != baseline_answer,
                    "swap_target_token_log_probability": (
                        None
                        if swap_target is None
                        else intervention_swap_target["log_probability"]
                        - baseline_swap_target["log_probability"]
                    ),
                },
            }
        )
        if len(rows) % args.progress_every == 0 or len(rows) == len(queries):
            print(f"evaluated {len(rows)}/{len(queries)}", flush=True)

    output_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_jsonl(rows_path, rows)
    summary = {
        "status": "complete",
        "model": MODEL_ID,
        "stage_one_revision": MODEL_REVISION,
        "model_commit": MODEL_COMMIT,
        "lens": str(args.lens),
        "lens_prompts": lens.n_prompts,
        "settings": settings,
        "selected_groups": args.groups,
        "num_queries": len(rows),
        "skipped": skipped,
        "groups": {
            group: summarize_group(rows, group)
            for group in args.groups
        },
        "outputs": {"per_query": str(rows_path)},
    }
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return summary


def main() -> None:
    run(parse_args())


if __name__ == "__main__":
    main()
