"""Core logic for generated, single-token Stage-02 association sets."""
from __future__ import annotations

import hashlib
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import torch

from multipath.prepare import comparison_key, load_json, normalized_answer, read_jsonl

SCHEMA_VERSION = 2
TARGET_MODES = ("true", "model")
WORD = re.compile(r"[^\W_]+(?:[-'’][^\W_]+)*", flags=re.UNICODE)
LIST_PREFIX = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s*")


@dataclass(frozen=True)
class GenerationSpec:
    task: str
    answer_type: str
    templates: tuple[str, ...]
    scoring_templates: tuple[str, ...]
    top_n: int
    analysis_k_values: tuple[int, ...]
    primary_k: int
    requested_candidates: int
    max_new_tokens: int
    stopwords: frozenset[str]
    generic_capital_words: frozenset[str]
    excluded_generic_name_pieces: frozenset[str]
    generic_min_answers: int
    generic_max_answer_fraction: float
    provider: str


def stable_target_id(task: str, mode: str, answer: str) -> str:
    digest = hashlib.sha256(f"{task}\0{mode}\0{answer}".encode()).hexdigest()[:20]
    return f"{mode}_{digest}"


def load_generation_specs(path: Path, tasks: Iterable[str]) -> dict[str, GenerationSpec]:
    payload = load_json(path)
    if payload.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("unsupported association-generation configuration schema")
    top_n, requested = payload.get("top_n"), payload.get("requested_candidates")
    k_values, primary_k = payload.get("analysis_k_values"), payload.get("primary_k")
    max_new, minimum = payload.get("max_new_tokens"), payload.get("generic_min_answers")
    fraction = payload.get("generic_max_answer_fraction")
    if not isinstance(top_n, int) or top_n <= 0:
        raise ValueError("top_n must be positive")
    if not isinstance(requested, int) or requested < top_n:
        raise ValueError("requested_candidates must be at least top_n")
    if (not isinstance(k_values, list) or not k_values or
            any(not isinstance(value, int) or value <= 0 or value > top_n for value in k_values) or
            len(k_values) != len(set(k_values)) or k_values != sorted(k_values)):
        raise ValueError("analysis_k_values must be sorted unique positive integers no larger than top_n")
    if primary_k not in k_values:
        raise ValueError("primary_k must be one of analysis_k_values")
    if not isinstance(max_new, int) or max_new <= 0:
        raise ValueError("max_new_tokens must be positive")
    if not isinstance(minimum, int) or minimum < 1:
        raise ValueError("generic_min_answers must be positive")
    if not isinstance(fraction, (int, float)) or not 0 < fraction <= 1:
        raise ValueError("generic_max_answer_fraction must be in (0, 1]")
    stopwords = payload.get("stopwords")
    if not isinstance(stopwords, list) or any(not isinstance(word, str) for word in stopwords):
        raise ValueError("stopwords must be a string list")
    provider = payload.get("provider")
    if not isinstance(provider, str) or not provider:
        raise ValueError("provider must be named")
    capital_words = payload.get("generic_capital_words")
    name_pieces = payload.get("excluded_generic_name_pieces")
    if not isinstance(capital_words, list) or any(not isinstance(word, str) for word in capital_words):
        raise ValueError("generic_capital_words must be a string list")
    if not isinstance(name_pieces, list) or any(not isinstance(word, str) for word in name_pieces):
        raise ValueError("excluded_generic_name_pieces must be a string list")
    output = {}
    for task in tasks:
        settings = payload.get("tasks", {}).get(task)
        if not isinstance(settings, dict):
            raise ValueError(f"configuration lacks task {task}")
        templates = settings.get("templates")
        scoring_templates = settings.get("scoring_templates")
        if not isinstance(templates, list) or len(templates) < 2:
            raise ValueError(f"{task} needs at least two generation prompts")
        if any(not isinstance(t, str) or t.count("{answer}") != 1 or t.count("{count}") != 1 for t in templates):
            raise ValueError(f"each {task} template needs one {{answer}} and one {{count}}")
        if (not isinstance(scoring_templates, list) or len(scoring_templates) < 2 or
                any(not isinstance(t, str) or t.count("{answer}") != 1 for t in scoring_templates)):
            raise ValueError(f"each {task} needs at least two scoring templates with one {{answer}}")
        output[task] = GenerationSpec(
            task=task, answer_type=settings["answer_type"], templates=tuple(templates),
            scoring_templates=tuple(scoring_templates), top_n=top_n,
            analysis_k_values=tuple(k_values), primary_k=primary_k,
            requested_candidates=requested, max_new_tokens=max_new,
            stopwords=frozenset(comparison_key(word) for word in stopwords),
            generic_capital_words=frozenset(comparison_key(word) for word in capital_words),
            excluded_generic_name_pieces=frozenset(comparison_key(word) for word in name_pieces),
            generic_min_answers=minimum, generic_max_answer_fraction=float(fraction), provider=provider,
        )
    return output


def word_parts(text: str) -> set[str]:
    return {comparison_key(match.group(0)) for match in WORD.finditer(text)}


def surface_piece_keys(surfaces: Iterable[str]) -> set[str]:
    keys: set[str] = set()
    for surface in surfaces:
        if comparison_key(surface):
            keys.add(comparison_key(surface))
            keys.update(word_parts(surface))
    return keys


def build_target_inventory(prepared_path: Path, task: str, answer_type: str) -> dict[str, Any]:
    aggregates: dict[str, dict[str, dict[str, Any]]] = {mode: {} for mode in TARGET_MODES}
    task_intermediates: set[str] = set()
    model_metadata = None
    num_records = 0
    for row_number, record in enumerate(read_jsonl(prepared_path), start=1):
        if record.get("task") != task or record.get("split") not in {"selection", "test"}:
            raise ValueError(f"invalid prepared row {row_number}")
        row_model = record.get("model")
        if not isinstance(row_model, dict):
            raise ValueError(f"prepared row {row_number} lacks model metadata")
        model_metadata = dict(row_model) if model_metadata is None else model_metadata
        if row_model != model_metadata:
            raise ValueError("model metadata changes within prepared data")
        intermediate = record.get("Fx")
        if not isinstance(intermediate, str) or not intermediate.strip():
            raise ValueError(f"prepared row {row_number} lacks Fx")
        intermediate = normalized_answer(intermediate)
        task_intermediates.add(intermediate)
        num_records += 1
        values = {"true": record.get("true_answer")}
        if record.get("answer_status") != "ineligible":
            values["model"] = record.get("model_answer_normalized")
        for mode, answer in values.items():
            if not isinstance(answer, str) or not answer.strip():
                raise ValueError(f"prepared row {row_number} has invalid {mode} answer")
            answer = normalized_answer(answer)
            entry = aggregates[mode].setdefault(answer, {"prompt_count": 0, "entities": set(), "relevant": set()})
            entry["prompt_count"] += 1
            entry["entities"].add(record["x"])
            entry["relevant"].add(intermediate)
    result: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION, "task": task, "answer_type": answer_type,
        "source": str(prepared_path), "num_prepared_records": num_records, "model": model_metadata,
        "task_intermediates": sorted(task_intermediates, key=comparison_key), "modes": {},
    }
    for mode in TARGET_MODES:
        rows = []
        for answer in sorted(aggregates[mode], key=lambda value: (comparison_key(value), value)):
            entry = aggregates[mode][answer]
            rows.append({
                "target_id": stable_target_id(task, mode, answer), "target_mode": mode,
                "answer": answer, "answer_type": answer_type, "prompt_count": entry["prompt_count"],
                "num_query_entities": len(entry["entities"]),
                "relevant_intermediates": sorted(entry["relevant"], key=comparison_key),
            })
        result["modes"][mode] = rows
    return result


def render_generation_prompts(answer: str, spec: GenerationSpec) -> list[str]:
    return [template.format(answer=answer, count=spec.requested_candidates) for template in spec.templates]


def render_scoring_prompts(answer: str, spec: GenerationSpec) -> list[str]:
    """Render the fixed next-token cues used by the prompted provider."""

    return [template.format(answer=answer) for template in spec.scoring_templates]


def leave_one_out_contrast(
    target_scores: torch.Tensor,
    comparison_mean: torch.Tensor,
    num_answers: int,
) -> torch.Tensor:
    """Contrast one answer's scores against all other answers of its type."""

    if num_answers < 2:
        raise ValueError("contrast requires at least two answers")
    if target_scores.shape != comparison_mean.shape or target_scores.ndim != 1:
        raise ValueError("target scores and comparison mean must be aligned vectors")
    if not torch.isfinite(target_scores).all() or not torch.isfinite(comparison_mean).all():
        raise ValueError("contrast inputs must be finite")
    others_mean = (comparison_mean.float() * num_answers - target_scores.float()) / (num_answers - 1)
    return target_scores.float() - others_mean


def load_static_catalog(path: Path, task: str, mode: str) -> dict[str, list[str]]:
    """Load a human-reviewed answer-to-word catalog without model inference."""

    payload = load_json(path)
    if payload.get("schema_version") != 1:
        raise ValueError("unsupported static-association catalog schema")
    configured = payload.get("tasks", {})

    def resolve(task_name: str, ancestry: tuple[str, ...]) -> dict[str, list[str]]:
        if task_name in ancestry:
            raise ValueError("static catalog inheritance contains a cycle")
        settings = configured.get(task_name)
        if not isinstance(settings, dict):
            raise ValueError(f"static catalog lacks task {task_name}")
        parent = settings.get("inherit_from")
        output = resolve(parent, (*ancestry, task_name)) if isinstance(parent, str) else {}
        raw = settings.get(mode, {})
        if not isinstance(raw, dict):
            raise ValueError(f"static catalog has invalid {task_name}/{mode}")
        for answer, words in raw.items():
            if not isinstance(answer, str) or not answer.strip():
                raise ValueError("static catalog contains an invalid answer")
            if not isinstance(words, list) or any(
                not isinstance(word, str) or not word.strip() for word in words
            ):
                raise ValueError(f"invalid static words for {answer}")
            keys = [comparison_key(word) for word in words]
            if len(keys) != len(set(keys)):
                raise ValueError(f"duplicate static words for {answer}")
            output[answer] = list(words)
        return output

    result = resolve(task, ())
    if not result:
        raise ValueError(f"static catalog lacks {task}/{mode}")
    return result


def parse_generated_candidates(text: str) -> list[str]:
    candidates = []
    for item in re.split(r"[,;|\n]+", text):
        item = LIST_PREFIX.sub("", item).strip().strip('"“”\'` .:()[]{}')
        matches = list(WORD.finditer(item))
        if len(matches) == 1 and matches[0].span() == (0, len(item)):
            candidates.append(item)
    return candidates


def single_token_word(tokenizer: Any, word: str) -> tuple[int, str] | None:
    if not word or " " in word.strip() or not any(character.isalpha() for character in word):
        return None
    ids = tokenizer.encode(f" {word.strip()}", add_special_tokens=False)
    if len(ids) != 1:
        return None
    token_id = int(ids[0])
    decoded = tokenizer.decode([token_id])
    if not decoded or not decoded[0].isspace() or comparison_key(decoded) != comparison_key(word):
        return None
    return token_id, decoded.strip()


def build_candidate_pool(*, tokenizer: Any, target: Mapping[str, Any], generations: Sequence[str],
                         task_intermediates: Sequence[str], aliases: Sequence[str],
                         spec: GenerationSpec) -> tuple[list[dict[str, Any]], list[dict[str, Any]],
                                                        list[dict[str, Any]], list[dict[str, Any]], Counter[str]]:
    answer_keys = surface_piece_keys([target["answer"], *aliases])
    intermediate_keys = surface_piece_keys(task_intermediates)
    kept: dict[str, dict[str, Any]] = {}
    rejected: Counter[str] = Counter()
    intermediate_words: dict[str, dict[str, Any]] = {}
    capital_words: dict[str, dict[str, Any]] = {}
    name_pieces: dict[str, dict[str, Any]] = {}
    order = 0
    for cue_index, generation in enumerate(generations):
        for word in parse_generated_candidates(generation):
            order += 1
            token = single_token_word(tokenizer, word)
            if token is None:
                rejected["not_single_token"] += 1
                continue
            token_id, surface = token
            key = comparison_key(surface)
            if key in spec.stopwords:
                rejected["stopword"] += 1
                continue
            if key in answer_keys:
                rejected["answer_or_answer_piece"] += 1
                continue
            if key in intermediate_keys:
                rejected["task_intermediate_or_piece"] += 1
                row = intermediate_words.setdefault(key, {"text": surface, "token_id": token_id, "count": 0})
                row["count"] += 1
                continue
            if key in spec.generic_capital_words:
                rejected["generic_capital_word"] += 1
                row = capital_words.setdefault(key, {"text": surface, "token_id": token_id, "count": 0})
                row["count"] += 1
                continue
            if key in spec.excluded_generic_name_pieces:
                rejected["generic_name_piece"] += 1
                row = name_pieces.setdefault(key, {"text": surface, "token_id": token_id, "count": 0})
                row["count"] += 1
                continue
            row = kept.setdefault(key, {"text": surface, "token_id": token_id, "generation_count": 0,
                                        "cue_indices": set(), "first_seen": order})
            row["generation_count"] += 1
            row["cue_indices"].add(cue_index)
    pool = sorted(kept.values(), key=lambda row: (-row["generation_count"], row["first_seen"], comparison_key(row["text"])))
    for row in pool:
        row["cue_indices"] = sorted(row["cue_indices"])
    sort_rows = lambda values: sorted(values, key=lambda row: comparison_key(row["text"]))
    return pool, sort_rows(intermediate_words.values()), sort_rows(capital_words.values()), \
        sort_rows(name_pieces.values()), rejected


def generic_document_limit(num_targets: int, spec: GenerationSpec) -> int:
    return max(spec.generic_min_answers, math.floor(spec.generic_max_answer_fraction * num_targets))


def finalize_associations(rows: Sequence[dict[str, Any]], spec: GenerationSpec,
                          filter_generic: bool = True) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    frequency: Counter[str] = Counter()
    for row in rows:
        frequency.update({comparison_key(item["text"]) for item in row["candidate_pool"]})
    limit = generic_document_limit(len(rows), spec)
    output, returned = [], Counter()
    k_coverage = Counter()
    for row in rows:
        eligible, generic = [], []
        for candidate in row["candidate_pool"]:
            count = frequency[comparison_key(candidate["text"])]
            enriched = {**candidate, "answer_document_frequency": count}
            if filter_generic and count > limit:
                generic.append(enriched)
            else:
                eligible.append(enriched)
        # This ranking is frozen before causal experiments: rarer words first,
        # with the manually curated order as the deterministic tie-breaker.
        accepted = sorted(
            eligible,
            key=lambda candidate: (
                candidate["answer_document_frequency"],
                candidate["first_seen"],
                comparison_key(candidate["text"]),
            ),
        )[:spec.top_n]
        final = dict(row)
        final.pop("candidate_pool")
        final["associations"] = [{"association_rank": rank, **candidate}
                                 for rank, candidate in enumerate(accepted, start=1)]
        final["association_subsets"] = {}
        for k in spec.analysis_k_values:
            available = len(accepted) >= k
            if available:
                k_coverage[k] += 1
            final["association_subsets"][str(k)] = {
                "available": available,
                "is_primary": k == spec.primary_k,
                "selection_rule": "lowest answer-document frequency; curated-order tie-break",
                "token_ids": [candidate["token_id"] for candidate in accepted[:k]] if available else [],
                "words": [candidate["text"] for candidate in accepted[:k]] if available else [],
            }
        final["generic_words_removed"] = generic
        final["audit"] = {**final.get("audit", {}), "candidate_pool_size": len(row["candidate_pool"]),
                          "returned_top_n": len(accepted), "generic_document_frequency_limit": limit}
        returned[len(accepted)] += 1
        output.append(final)
    return output, {"returned_top_n_counts": dict(sorted(returned.items())),
                    "generic_document_frequency_limit": limit,
                    "analysis_k_values": list(spec.analysis_k_values),
                    "primary_k": spec.primary_k,
                    "k_coverage": {str(k): k_coverage[k] for k in spec.analysis_k_values},
                    "subset_selection_rule": "lowest answer-document frequency; curated-order tie-break"}


def inventory_targets(inventory: Mapping[str, Any], mode: str) -> list[dict[str, Any]]:
    if mode not in TARGET_MODES:
        raise ValueError(f"unknown target mode: {mode}")
    targets = inventory.get("modes", {}).get(mode)
    if not isinstance(targets, list) or not targets:
        raise ValueError(f"inventory has no targets for mode {mode}")
    ids = [row.get("target_id") for row in targets]
    if any(not isinstance(value, str) for value in ids) or len(ids) != len(set(ids)):
        raise ValueError("invalid or duplicate target IDs")
    return targets


def slice_targets(targets: Sequence[dict[str, Any]], start: int, count: int | None) -> list[dict[str, Any]]:
    if start < 0 or (count is not None and count <= 0):
        raise ValueError("invalid target slice")
    return list(targets[start:] if count is None else targets[start:start + count])
