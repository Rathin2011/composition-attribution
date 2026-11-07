"""Prepare validated populations for the multi-path routing experiments.

This module is deliberately limited to Stage 01.  It joins the existing
generalized prompt manifest and behavioral baseline, creates query-entity
selection/test splits, and writes a smaller auditable artifact.  It does not
load a language model or implement any association or intervention logic.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import math
import random
import re
from collections import Counter, defaultdict
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping, TextIO


SCHEMA_VERSION = 1
DEFAULT_SELECTION_FRACTION = 0.30
DEFAULT_SPLIT_SEED = 0
PROMPT_MARKER = re.compile(r"(?:^|\s)[QA]:")


@dataclass(frozen=True)
class TaskSource:
    """Resolved Stage-01 inputs for one task."""

    task: str
    source_directory: Path
    split_method: str
    num_icl_examples: int

    @property
    def manifest(self) -> Path:
        return self.source_directory / "prompt_manifest.jsonl"

    @property
    def baseline(self) -> Path:
        return self.source_directory / "baseline_evaluation.jsonl.gz"

    @property
    def baseline_summary(self) -> Path:
        return self.source_directory / "baseline_summary.json"


@dataclass(frozen=True)
class Entity:
    """One unique query entity and its ground-truth route."""

    query_index: int
    x: str
    Fx: str
    GFx: str

    @property
    def stratum(self) -> tuple[str, str]:
        return self.Fx, self.GFx


def load_json(path: Path) -> Any:
    """Read one JSON value."""

    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


@contextmanager
def open_text(path: Path, mode: str) -> Iterator[TextIO]:
    """Open plain or gzip-compressed UTF-8 text."""

    if "t" not in mode:
        raise ValueError("open_text requires text mode")
    if path.suffix == ".gz":
        with gzip.open(path, mode, encoding="utf-8") as handle:
            yield handle
    else:
        with path.open(mode, encoding="utf-8") as handle:
            yield handle


def read_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    """Stream nonempty JSON objects and identify malformed rows."""

    with open_text(path, "rt") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                raise ValueError(f"{path}:{line_number}: empty line")
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number}: expected an object")
            yield value


def sha256(path: Path) -> str:
    """Return a source-artifact digest without decompressing it."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def normalized_answer(text: str) -> str:
    """Return the display normalization used for alias comparisons only."""

    return " ".join(text.strip().split())


def comparison_key(text: str) -> str:
    """Return a case-insensitive normalized answer key."""

    return normalized_answer(text).casefold()


def classify_answer(
    prediction: str,
    label: str,
    true_answer: str,
    aliases: Mapping[str, list[str]],
    eligibility: Mapping[str, Any],
) -> dict[str, Any]:
    """Classify a generated answer using fixed, auditable precedence rules."""

    normalized = normalized_answer(prediction)
    if prediction == label:
        return {
            "status": "correct",
            "reason": "exact_label_match",
            "matched_surface": true_answer,
            "normalized": normalized,
        }

    target_key = comparison_key(true_answer)
    prediction_key = comparison_key(prediction)
    if prediction_key and prediction_key == target_key:
        return {
            "status": "true_answer_alias",
            "reason": "normalized_canonical_match",
            "matched_surface": true_answer,
            "normalized": normalized,
        }

    for alias in aliases.get(true_answer, []):
        if prediction_key and prediction_key == comparison_key(alias):
            return {
                "status": "true_answer_alias",
                "reason": "configured_alias_match",
                "matched_surface": alias,
                "normalized": normalized,
            }

    reason = None
    if not normalized:
        reason = "empty"
    elif eligibility.get("reject_multiline", True) and ("\n" in prediction or "\r" in prediction):
        reason = "multiple_lines"
    elif eligibility.get("reject_prompt_markers", True) and PROMPT_MARKER.search(prediction):
        reason = "prompt_spillover"
    elif eligibility.get("require_alphanumeric", True) and not any(character.isalnum() for character in normalized):
        reason = "no_alphanumeric_content"
    elif len(normalized.split()) > int(eligibility.get("max_words", 12)):
        reason = "too_many_words"

    return {
        "status": "ineligible" if reason else "eligible_wrong",
        "reason": reason or "well_formed_nonmatching_answer",
        "matched_surface": None,
        "normalized": normalized,
    }


def load_task_sources(config_path: Path, project_root: Path) -> dict[str, TaskSource]:
    """Load and resolve the five fixed Stage-01 task sources."""

    payload = load_json(config_path)
    if payload.get("schema_version") != 1:
        raise ValueError("unsupported task configuration schema")
    num_icl = payload.get("num_icl_examples")
    if not isinstance(num_icl, int) or num_icl <= 0:
        raise ValueError("num_icl_examples must be a positive integer")
    output = {}
    for task, settings in payload.get("tasks", {}).items():
        if settings.get("split_method") not in {
            "intermediate_answer_stratified",
            "entity_random",
        }:
            raise ValueError(f"invalid split method for {task}")
        source = (project_root / settings["source_directory"]).resolve()
        result = TaskSource(task, source, settings["split_method"], num_icl)
        for required in (result.manifest, result.baseline, result.baseline_summary):
            if not required.is_file():
                raise FileNotFoundError(required)
        output[task] = result
    if not output:
        raise ValueError("task configuration contains no tasks")
    return output


def load_alias_config(path: Path, tasks: Iterable[str]) -> tuple[dict[str, dict[str, list[str]]], dict[str, Any]]:
    """Validate the fixed answer-alias catalog and eligibility policy."""

    payload = load_json(path)
    if payload.get("schema_version") != 1:
        raise ValueError("unsupported alias configuration schema")
    eligibility = payload.get("eligibility")
    if not isinstance(eligibility, dict):
        raise ValueError("alias configuration lacks eligibility settings")
    aliases: dict[str, dict[str, list[str]]] = {}
    configured = payload.get("tasks", {})
    for task in tasks:
        task_payload = configured.get(task)
        if not isinstance(task_payload, dict) or not isinstance(task_payload.get("aliases"), dict):
            raise ValueError(f"alias configuration lacks task {task}")
        task_aliases = {}
        for canonical, surfaces in task_payload["aliases"].items():
            if not isinstance(canonical, str) or not canonical.strip():
                raise ValueError(f"invalid canonical alias key for {task}")
            if not isinstance(surfaces, list) or any(
                not isinstance(surface, str) or not surface.strip() for surface in surfaces
            ):
                raise ValueError(f"invalid aliases for {task}: {canonical}")
            keys = [comparison_key(surface) for surface in surfaces]
            if comparison_key(canonical) in keys or len(keys) != len(set(keys)):
                raise ValueError(f"duplicate canonical/alias surface for {task}: {canonical}")
            task_aliases[canonical] = list(surfaces)
        aliases[task] = task_aliases
    return aliases, eligibility


def index_manifest(source: TaskSource) -> tuple[dict[str, dict[str, Any]], list[Entity]]:
    """Load, validate, and index one existing ten-context prompt manifest."""

    records: dict[str, dict[str, Any]] = {}
    entity_by_index: dict[int, Entity] = {}
    index_by_x: dict[str, int] = {}
    variants: dict[int, set[int]] = defaultdict(set)

    for row_number, record in enumerate(read_jsonl(source.manifest), start=1):
        identifier = record.get("prompt_instance_id")
        if not isinstance(identifier, str) or not identifier or identifier in records:
            raise ValueError(f"manifest row {row_number}: invalid or duplicate prompt ID")
        if record.get("task") != source.task:
            raise ValueError(f"manifest row {row_number}: wrong task")
        query = record.get("query")
        context = record.get("context")
        if not isinstance(query, dict) or not all(
            isinstance(query.get(name), str) and query[name] for name in ("x", "Fx", "GFx")
        ):
            raise ValueError(f"manifest row {row_number}: invalid query")
        if not isinstance(context, list) or len(context) != source.num_icl_examples:
            raise ValueError(f"manifest row {row_number}: expected {source.num_icl_examples} demonstrations")
        query_index = record.get("query_index")
        variant = record.get("context_variant")
        if not isinstance(query_index, int) or not isinstance(variant, int):
            raise ValueError(f"manifest row {row_number}: invalid query index or context variant")
        entity = Entity(query_index, query["x"], query["Fx"], query["GFx"])
        previous = entity_by_index.setdefault(query_index, entity)
        if previous != entity:
            raise ValueError(f"query index {query_index} changes identity across contexts")
        previous_index = index_by_x.setdefault(entity.x, query_index)
        if previous_index != query_index:
            raise ValueError(f"query entity {entity.x!r} has multiple query indices")
        if variant in variants[query_index]:
            raise ValueError(f"query {query_index} repeats context variant {variant}")
        variants[query_index].add(variant)
        records[identifier] = record

    expected_variants = set(range(source.num_icl_examples))
    for query_index, found in variants.items():
        if found != expected_variants:
            raise ValueError(
                f"query {query_index} has context variants {sorted(found)}, "
                f"expected {sorted(expected_variants)}"
            )
    return records, sorted(entity_by_index.values(), key=lambda entity: entity.query_index)


def rounded_count(total: int, fraction: float) -> int:
    """Round halves upward rather than using Python's banker rounding."""

    return int(math.floor(total * fraction + 0.5))


def create_split(
    entities: list[Entity],
    method: str,
    *,
    selection_fraction: float,
    seed: int,
) -> tuple[dict[str, str], dict[str, int], set[str]]:
    """Assign query entities to deterministic selection/test populations."""

    if not 0 < selection_fraction < 1:
        raise ValueError("selection_fraction must lie strictly between zero and one")
    rng = random.Random(seed)
    assignment: dict[str, str] = {}
    stratum_sizes: dict[str, int] = {}
    singleton_entities: set[str] = set()

    if method == "entity_random":
        shuffled = sorted(entities, key=lambda entity: (entity.x, entity.query_index))
        rng.shuffle(shuffled)
        selection_count = min(max(1, rounded_count(len(shuffled), selection_fraction)), len(shuffled) - 1)
        selected = {entity.x for entity in shuffled[:selection_count]}
        for entity in entities:
            assignment[entity.x] = "selection" if entity.x in selected else "test"
            stratum_sizes[entity.x] = 1
        return assignment, stratum_sizes, singleton_entities

    if method != "intermediate_answer_stratified":
        raise ValueError(f"unknown split method: {method}")

    strata: dict[tuple[str, str], list[Entity]] = defaultdict(list)
    for entity in entities:
        strata[entity.stratum].append(entity)
    for stratum in sorted(strata):
        members = sorted(strata[stratum], key=lambda entity: (entity.x, entity.query_index))
        rng.shuffle(members)
        size = len(members)
        if size == 1:
            singleton_entities.add(members[0].x)
            selection_count = 1 if rng.random() < selection_fraction else 0
        else:
            selection_count = min(max(1, rounded_count(size, selection_fraction)), size - 1)
        selected = {entity.x for entity in members[:selection_count]}
        for entity in members:
            assignment[entity.x] = "selection" if entity.x in selected else "test"
            stratum_sizes[entity.x] = size
    return assignment, stratum_sizes, singleton_entities


def demonstration_overlap(
    manifest: Mapping[str, Mapping[str, Any]], assignment: Mapping[str, str]
) -> dict[str, Any]:
    """Audit cross-split query entities reused as ICL demonstrations."""

    directions = {
        "test_entities_in_selection_demonstrations": ("selection", "test"),
        "selection_entities_in_test_demonstrations": ("test", "selection"),
    }
    output = {}
    entities_by_split = {
        split: {entity for entity, assigned in assignment.items() if assigned == split}
        for split in ("selection", "test")
    }
    for name, (query_split, demo_split) in directions.items():
        affected_prompts = 0
        occurrences = 0
        overlapping_entities: set[str] = set()
        candidates = entities_by_split[demo_split]
        for record in manifest.values():
            if assignment[record["query"]["x"]] != query_split:
                continue
            found = [example["x"] for example in record["context"] if example["x"] in candidates]
            if found:
                affected_prompts += 1
                occurrences += len(found)
                overlapping_entities.update(found)
        output[name] = {
            "num_affected_prompts": affected_prompts,
            "num_demonstration_occurrences": occurrences,
            "num_distinct_entities": len(overlapping_entities),
            "entities": sorted(overlapping_entities),
        }
    return output


def prepare_task(
    source: TaskSource,
    *,
    output_directory: Path,
    aliases: Mapping[str, list[str]],
    eligibility: Mapping[str, Any],
    selection_fraction: float = DEFAULT_SELECTION_FRACTION,
    seed: int = DEFAULT_SPLIT_SEED,
    overwrite: bool = False,
) -> dict[str, Any]:
    """Run Stage 01 for one task and return its installed summary."""

    output_path = output_directory / "prompt_targets.jsonl.gz"
    entities_path = output_directory / "entities.json"
    summary_path = output_directory / "summary.json"
    existing = [path for path in (output_path, entities_path, summary_path) if path.exists()]
    if existing and not overwrite:
        raise FileExistsError(f"Stage-01 outputs already exist: {existing}")

    manifest, entities = index_manifest(source)
    assignment, stratum_sizes, singleton_entities = create_split(
        entities,
        source.split_method,
        selection_fraction=selection_fraction,
        seed=seed,
    )
    baseline_summary = load_json(source.baseline_summary)
    if baseline_summary.get("task") != source.task:
        raise ValueError("baseline summary belongs to the wrong task")
    model_metadata = {
        key: baseline_summary.get(key)
        for key in (
            "model",
            "stage_one_revision",
            "model_commit",
            "dtype",
            "batch_size",
            "max_new_tokens",
            "stop_sequence",
        )
    }
    if not model_metadata["model"] or not model_metadata["model_commit"]:
        raise ValueError("baseline summary lacks pinned model metadata")

    output_directory.mkdir(parents=True, exist_ok=True)
    temporary_output = output_path.with_name(output_path.name + ".tmp")
    temporary_entities = entities_path.with_name(entities_path.name + ".tmp")
    temporary_summary = summary_path.with_name(summary_path.name + ".tmp")
    seen: set[str] = set()
    split_prompt_counts = Counter()
    split_correct_counts = Counter()
    answer_status_counts: dict[str, Counter[str]] = defaultdict(Counter)
    try:
        with gzip.open(temporary_output, "wt", encoding="utf-8") as handle:
            for row_number, record in enumerate(read_jsonl(source.baseline), start=1):
                identifier = record.get("prompt_instance_id")
                if not isinstance(identifier, str) or identifier in seen:
                    raise ValueError(f"baseline row {row_number}: invalid or duplicate prompt ID")
                expected = manifest.get(identifier)
                if expected is None:
                    raise ValueError(f"baseline row {row_number}: ID not found in manifest")
                seen.add(identifier)
                for field in ("task", "query_index", "context_variant", "query", "context", "prompt"):
                    if record.get(field) != expected.get(field):
                        raise ValueError(f"baseline row {row_number}: manifest mismatch in {field}")
                evaluation = record.get("evaluation")
                if not isinstance(evaluation, dict):
                    raise ValueError(f"baseline row {row_number}: missing evaluation")
                prediction = evaluation.get("prediction")
                label = evaluation.get("label")
                if not isinstance(prediction, str) or not isinstance(label, str):
                    raise ValueError(f"baseline row {row_number}: invalid prediction or label")
                if "\n\n" in prediction:
                    raise ValueError(f"baseline row {row_number}: prediction was not cut at blank line")
                query = record["query"]
                expected_label = f" {query['GFx']}"
                if label != expected_label:
                    raise ValueError(f"baseline row {row_number}: label does not equal the full true answer")
                exact_match = prediction == label
                if evaluation.get("exact_match") is not exact_match:
                    raise ValueError(f"baseline row {row_number}: incorrect saved exact-match flag")
                split = assignment[query["x"]]
                answer = classify_answer(prediction, label, query["GFx"], aliases, eligibility)
                prepared = {
                    "schema_version": SCHEMA_VERSION,
                    "prompt_instance_id": identifier,
                    "task": source.task,
                    "split": split,
                    "split_seed": seed,
                    "selection_fraction": selection_fraction,
                    "split_method": source.split_method,
                    "query_index": record["query_index"],
                    "context_variant": record["context_variant"],
                    "num_icl_examples": source.num_icl_examples,
                    "x": query["x"],
                    "Fx": query["Fx"],
                    "true_answer": query["GFx"],
                    "stratum": {"Fx": query["Fx"], "GFx": query["GFx"]},
                    "stratum_size": stratum_sizes[query["x"]],
                    "singleton_stratum": query["x"] in singleton_entities,
                    "context": record["context"],
                    "prompt": record["prompt"],
                    "model_answer_raw": prediction,
                    "model_answer_normalized": answer["normalized"],
                    "answer_status": answer["status"],
                    "answer_status_reason": answer["reason"],
                    "matched_true_answer_surface": answer["matched_surface"],
                    "exact_match": exact_match,
                    "model": model_metadata,
                }
                handle.write(json.dumps(prepared, ensure_ascii=False) + "\n")
                split_prompt_counts[split] += 1
                split_correct_counts[split] += int(exact_match)
                answer_status_counts[split][answer["status"]] += 1
        if seen != set(manifest):
            missing = set(manifest) - seen
            raise ValueError(f"baseline is missing {len(missing)} manifest records")

        entity_rows = []
        for entity in entities:
            entity_rows.append(
                {
                    "query_index": entity.query_index,
                    "x": entity.x,
                    "Fx": entity.Fx,
                    "GFx": entity.GFx,
                    "split": assignment[entity.x],
                    "stratum_size": stratum_sizes[entity.x],
                    "singleton_stratum": entity.x in singleton_entities,
                }
            )
        entity_counts = Counter(row["split"] for row in entity_rows)
        summary = {
            "schema_version": SCHEMA_VERSION,
            "task": source.task,
            "num_icl_examples": source.num_icl_examples,
            "split": {
                "method": source.split_method,
                "selection_fraction": selection_fraction,
                "seed": seed,
                "small_group_rule": "n>=2: at least one entity per side; n=1: seeded random assignment and flag",
                "num_singleton_strata": len(singleton_entities),
            },
            "counts": {
                split: {
                    "entities": entity_counts[split],
                    "prompts": split_prompt_counts[split],
                    "exact_correct": split_correct_counts[split],
                    "exact_accuracy": split_correct_counts[split] / split_prompt_counts[split],
                    "answer_status": dict(sorted(answer_status_counts[split].items())),
                }
                for split in ("selection", "test")
            },
            "total_entities": len(entities),
            "total_prompts": len(seen),
            "demonstration_overlap": demonstration_overlap(manifest, assignment),
            "answer_aliases": {
                "num_canonical_answers_with_aliases": len(aliases),
                "num_alias_surfaces": sum(len(values) for values in aliases.values()),
            },
            "model": model_metadata,
            "sources": {
                "manifest": {"path": str(source.manifest), "sha256": sha256(source.manifest)},
                "baseline": {"path": str(source.baseline), "sha256": sha256(source.baseline)},
                "baseline_summary": {
                    "path": str(source.baseline_summary),
                    "sha256": sha256(source.baseline_summary),
                },
            },
            "outputs": {
                "prompt_targets": str(output_path),
                "entities": str(entities_path),
                "summary": str(summary_path),
            },
        }
        temporary_entities.write_text(
            json.dumps(
                {"schema_version": SCHEMA_VERSION, "task": source.task, "entities": entity_rows},
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        temporary_summary.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        # Install only after every validation and every temporary write succeeds.
        temporary_output.replace(output_path)
        temporary_entities.replace(entities_path)
        temporary_summary.replace(summary_path)
        return summary
    finally:
        temporary_output.unlink(missing_ok=True)
        temporary_entities.unlink(missing_ok=True)
        temporary_summary.unlink(missing_ok=True)

