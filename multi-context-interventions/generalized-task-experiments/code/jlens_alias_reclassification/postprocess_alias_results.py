"""Filter, merge, and summarize saved country-alias J-Lens ranks.

This CPU-only stage does not run OLMo or J-Lens.  It uses ranks already saved
by ``evaluate_aliases.py`` and creates a conservative primary analysis:

* an alias must tokenize as one complete token;
* that token cannot be used by another country or its aliases;
* explicit common-word aliases are rejected;
* flagged aliases are included only in a sensitivity analysis.

Canonical rerun drift and genuine alias effects are reported separately.  The
original complete J-Lens file supplies non-shortcut contexts so query-level
shortcut rates have the correct denominator.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from evaluate_baseline import MODEL_ID, STAGE_ONE_COMMIT, ensure_outputs, open_text, read_jsonl
from evaluate_logit_lens import classify_rank
from tasks import get_task_spec
from jlens_alias_reclassification.evaluate_aliases import DEFAULT_ALIASES, load_aliases


PROJECT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_POLICY = Path(__file__).with_name("alias_filter_policy.json")
SUPPORTED_TASKS = ("landmark-country-capital", "park-country-capital")
EXPECTED_SHORTCUT_RECORDS = {
    "landmark-country-capital": 940,
    "park-country-capital": 419,
}
GROUPS = ("compositional", "ambiguous", "shortcut_candidate")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, choices=SUPPORTED_TASKS)
    parser.add_argument("--shard-directory", type=Path)
    parser.add_argument("--original-jlens", type=Path)
    parser.add_argument("--catalog-summary", type=Path, action="append", default=[])
    parser.add_argument("--aliases", type=Path, default=DEFAULT_ALIASES)
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    parser.add_argument("--output-directory", type=Path)
    parser.add_argument("--expected-shortcut-records", type=int)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_policy(path: Path) -> dict[str, Any]:
    policy = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(policy, dict) or not isinstance(policy.get("version"), int):
        raise ValueError("alias policy must be an object with an integer version")
    for key in ("explicit_reject", "sensitivity_only"):
        if not isinstance(policy.get(key), dict):
            raise ValueError(f"alias policy {key} must be an object")
    overlap = set(policy["explicit_reject"]) & set(policy["sensitivity_only"])
    if overlap:
        raise ValueError(f"aliases cannot be both rejected and sensitivity-only: {overlap}")
    return policy


def load_country_values(summary_paths: Sequence[Path]) -> list[str]:
    """Return the union of canonical Fx countries in stable order."""

    values: list[str] = []
    seen: set[str] = set()
    for path in summary_paths:
        summary = json.loads(path.read_text(encoding="utf-8"))
        catalog = summary.get("candidate_catalog", {}).get("Fx")
        if not isinstance(catalog, list):
            raise ValueError(f"{path} lacks candidate_catalog.Fx")
        for row in catalog:
            value = row.get("value") if isinstance(row, Mapping) else None
            if not isinstance(value, str):
                raise ValueError(f"{path} contains an invalid Fx catalog row")
            if value not in seen:
                values.append(value)
                seen.add(value)
    return values


def build_alias_audit(
    alias_map: Mapping[str, Sequence[str]],
    country_values: Sequence[str],
    tokenizer: Any,
    policy: Mapping[str, Any],
    *,
    task: str,
) -> list[dict[str, Any]]:
    """Apply the mechanical alias policy and return one auditable row per alias."""

    spec = get_task_spec(task)
    canonical_tokens: dict[int, set[str]] = defaultdict(set)
    canonical_ids: dict[str, list[int]] = {}
    for country in country_values:
        ids = spec.token_ids(tokenizer, "Fx", country)
        canonical_ids[country] = ids
        canonical_tokens[int(ids[0])].add(country)

    tokenized_aliases: dict[tuple[str, str], list[int]] = {}
    alias_tokens: dict[int, set[str]] = defaultdict(set)
    for country, aliases in alias_map.items():
        if country not in canonical_ids:
            continue
        for alias in aliases:
            ids = spec.token_ids(tokenizer, "Fx", alias)
            tokenized_aliases[(country, alias)] = ids
            alias_tokens[int(ids[0])].add(country)

    output = []
    for (country, alias), ids in tokenized_aliases.items():
        first = int(ids[0])
        other_canonical = sorted(canonical_tokens[first] - {country})
        other_alias = sorted(alias_tokens[first] - {country})
        reasons: list[str] = []
        if len(ids) != 1:
            reasons.append("multi_token_alias")
        if first == int(canonical_ids[country][0]):
            reasons.append("same_measured_token_as_canonical")
        if other_canonical:
            reasons.append("token_shared_with_other_canonical_country")
        if other_alias:
            reasons.append("token_shared_with_other_country_alias")

        explicit_reject = policy["explicit_reject"].get(alias)
        sensitivity_reason = policy["sensitivity_only"].get(alias)
        if explicit_reject:
            reasons.append("explicit_common_word_rejection")

        if reasons:
            status = "rejected"
        elif sensitivity_reason:
            status = "sensitivity_only"
        else:
            status = "accepted"
        output.append(
            {
                "country": country,
                "alias": alias,
                "token_ids": ids,
                "measured_token_id": first,
                "measured_token": tokenizer.decode([first]),
                "status": status,
                "rejection_reasons": reasons,
                "explicit_reject_reason": explicit_reject,
                "sensitivity_reason": sensitivity_reason,
                "other_canonical_countries_with_token": other_canonical,
                "other_alias_countries_with_token": other_alias,
            }
        )
    return output


def aliases_by_status(
    audit: Sequence[Mapping[str, Any]], status: str
) -> dict[str, list[str]]:
    output: dict[str, list[str]] = defaultdict(list)
    for row in audit:
        if row["status"] == status:
            output[row["country"]].append(row["alias"])
    return dict(output)


def rank_for_surface(record: Mapping[str, Any], surface: str) -> int:
    matches = []
    for group in record["alias_reclassification"]["surface_token_groups"]:
        if any(item["surface"] == surface for item in group["surface_forms"]):
            matches.append(int(group["best_vocabulary_rank"]))
    if len(matches) != 1:
        raise ValueError(f"surface {surface!r} must occur in exactly one token group")
    return matches[0]


def filtered_measurement(
    record: Mapping[str, Any],
    primary_aliases: Sequence[str],
    sensitivity_aliases: Sequence[str],
    *,
    policy_version: int,
) -> dict[str, Any]:
    """Derive primary and sensitivity labels from one saved alias-rank row."""

    raw = record["alias_reclassification"]
    validation = raw["canonical_rerun_validation"]
    canonical_rank = int(validation["rerun_rank"])
    canonical_group = validation["rerun_group"]

    def result(aliases: Sequence[str]) -> dict[str, Any]:
        candidates = [(record["query"]["Fx"], canonical_rank)]
        candidates.extend((alias, rank_for_surface(record, alias)) for alias in aliases)
        best_rank = min(rank for _, rank in candidates)
        winners = [surface for surface, rank in candidates if rank == best_rank]
        group = classify_rank(best_rank)
        return {
            "aliases": list(aliases),
            "best_vocabulary_rank": best_rank,
            "peak_reciprocal_rank": 1.0 / best_rank,
            "winning_surface_forms": winners,
            "group": group,
            "transition_from_canonical_rerun": f"{canonical_group}->{group}",
            "rank_improved": best_rank < canonical_rank,
            "classification_improved": group != canonical_group,
        }

    primary = result(primary_aliases)
    sensitivity = result([*primary_aliases, *sensitivity_aliases])
    return {
        "policy_version": policy_version,
        "canonical_drift": {
            **dict(validation),
            "transition": f"{validation['saved_group']}->{validation['rerun_group']}",
        },
        "no_accepted_primary_alias": not primary_aliases,
        "primary": primary,
        "sensitivity": sensitivity,
    }


def load_and_filter_shards(
    shard_directory: Path,
    *,
    task: str,
    primary_by_country: Mapping[str, Sequence[str]],
    sensitivity_by_country: Mapping[str, Sequence[str]],
    policy_version: int,
    expected_records: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Merge shard rows, validate completeness, and attach filtered labels."""

    shard_paths = sorted(shard_directory.glob("alias_reclassification_*.jsonl.gz"))
    if not shard_paths:
        raise FileNotFoundError(f"no alias shards found in {shard_directory}")
    rows: list[dict[str, Any]] = []
    sources = []
    seen: set[str] = set()
    for path in shard_paths:
        summary_path = path.with_name(path.name.removesuffix(".jsonl.gz") + "_summary.json")
        if not summary_path.is_file():
            raise FileNotFoundError(f"missing shard summary: {summary_path}")
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        shard_rows = list(read_jsonl(path))
        if len(shard_rows) != int(summary["num_shortcut_records"]):
            raise ValueError(f"row count disagrees with {summary_path}")
        sources.append(
            {
                "data": str(path),
                "data_sha256": sha256(path),
                "summary": str(summary_path),
                "summary_sha256": sha256(summary_path),
                "records": len(shard_rows),
            }
        )
        for row in shard_rows:
            identifier = row.get("prompt_instance_id")
            if not isinstance(identifier, str) or identifier in seen:
                raise ValueError(f"duplicate or invalid prompt_instance_id: {identifier!r}")
            if row.get("task") != task:
                raise ValueError("alias shard contains the wrong task")
            seen.add(identifier)
            country = row["query"]["Fx"]
            enriched = dict(row)
            enriched["filtered_alias_reclassification"] = filtered_measurement(
                row,
                primary_by_country.get(country, ()),
                sensitivity_by_country.get(country, ()),
                policy_version=policy_version,
            )
            rows.append(enriched)
    if len(rows) != expected_records:
        raise ValueError(f"expected {expected_records} alias rows, found {len(rows)}")
    return rows, sources


def build_query_results(
    original_records: Iterable[Mapping[str, Any]],
    filtered_rows: Sequence[Mapping[str, Any]],
    *,
    task: str,
) -> list[dict[str, Any]]:
    """Overlay filtered shortcut labels on every eligible original context."""

    overlay = {
        row["prompt_instance_id"]: row["filtered_alias_reclassification"]["primary"]["group"]
        for row in filtered_rows
    }
    original_shortcuts: set[str] = set()
    queries: dict[tuple[Any, str], dict[str, Any]] = {}
    for row in original_records:
        if row.get("task") != task:
            raise ValueError("original J-Lens file contains the wrong task")
        classification = ((row.get("j_lens") or {}).get("classification") or {})
        group = classification.get("group")
        if group not in GROUPS:
            continue
        identifier = row.get("prompt_instance_id")
        if group == "shortcut_candidate":
            original_shortcuts.add(identifier)
        final_group = overlay.get(identifier, group)
        key = (row.get("query_index"), row["query"]["x"])
        entry = queries.setdefault(
            key,
            {
                "task": task,
                "query_index": row.get("query_index"),
                "query": dict(row["query"]),
                "original_context_counts": Counter(),
                "final_context_counts": Counter(),
            },
        )
        entry["original_context_counts"][group] += 1
        entry["final_context_counts"][final_group] += 1

    if set(overlay) != original_shortcuts:
        missing = original_shortcuts - set(overlay)
        extra = set(overlay) - original_shortcuts
        raise ValueError(
            f"alias rows do not exactly cover original shortcuts: missing={len(missing)}, extra={len(extra)}"
        )

    output = []
    for entry in queries.values():
        original = {group: entry["original_context_counts"][group] for group in GROUPS}
        final = {group: entry["final_context_counts"][group] for group in GROUPS}
        total = sum(final.values())
        original_rate = original["shortcut_candidate"] / total
        final_rate = final["shortcut_candidate"] / total
        output.append(
            {
                "task": task,
                "query_index": entry["query_index"],
                "query": entry["query"],
                "num_eligible_contexts": total,
                "original_context_counts": original,
                "final_context_counts": final,
                "original_shortcut_rate": original_rate,
                "final_shortcut_rate": final_rate,
                "original_majority_shortcut": original["shortcut_candidate"] > total / 2,
                "final_majority_shortcut": final["shortcut_candidate"] > total / 2,
                "original_all_context_shortcut": original["shortcut_candidate"] == total,
                "final_all_context_shortcut": final["shortcut_candidate"] == total,
            }
        )
    return sorted(output, key=lambda row: (row["query_index"] is None, row["query_index"]))


def summarize(
    rows: Sequence[Mapping[str, Any]],
    query_rows: Sequence[Mapping[str, Any]],
    audit: Sequence[Mapping[str, Any]],
    sources: Sequence[Mapping[str, Any]],
    *,
    task: str,
    original_path: Path,
    policy_path: Path,
) -> dict[str, Any]:
    primary_transitions: Counter[str] = Counter()
    sensitivity_transitions: Counter[str] = Counter()
    drift_transitions: Counter[str] = Counter()
    per_country: dict[str, dict[str, Any]] = {}
    for row in rows:
        country = row["query"]["Fx"]
        filtered = row["filtered_alias_reclassification"]
        primary_transitions[filtered["primary"]["transition_from_canonical_rerun"]] += 1
        sensitivity_transitions[filtered["sensitivity"]["transition_from_canonical_rerun"]] += 1
        drift_transitions[filtered["canonical_drift"]["transition"]] += 1
        entry = per_country.setdefault(
            country,
            {
                "original_shortcut_records": 0,
                "unique_queries": set(),
                "primary_classification_counts": Counter(),
                "primary_transition_counts": Counter(),
                "records_without_primary_alias": 0,
                "primary_aliases": filtered["primary"]["aliases"],
                "sensitivity_aliases": filtered["sensitivity"]["aliases"],
            },
        )
        entry["original_shortcut_records"] += 1
        entry["unique_queries"].add(row.get("query_index"))
        entry["primary_classification_counts"][filtered["primary"]["group"]] += 1
        entry["primary_transition_counts"][filtered["primary"]["transition_from_canonical_rerun"]] += 1
        entry["records_without_primary_alias"] += int(filtered["no_accepted_primary_alias"])

    serializable_country = {}
    for country, entry in sorted(per_country.items()):
        serializable_country[country] = {
            **entry,
            "unique_queries": len(entry["unique_queries"]),
            "primary_classification_counts": {
                group: entry["primary_classification_counts"][group] for group in GROUPS
            },
            "primary_transition_counts": dict(sorted(entry["primary_transition_counts"].items())),
        }

    return {
        "task": task,
        "method": "conservative_single_identifying_token_alias_postprocessing",
        "original_jlens": str(original_path),
        "alias_policy": str(policy_path),
        "source_shards": list(sources),
        "num_original_shortcut_records": len(rows),
        "num_records_without_primary_alias": sum(
            row["filtered_alias_reclassification"]["no_accepted_primary_alias"] for row in rows
        ),
        "canonical_drift_transitions": dict(sorted(drift_transitions.items())),
        "primary_alias_transitions_from_canonical_rerun": dict(sorted(primary_transitions.items())),
        "sensitivity_alias_transitions_from_canonical_rerun": dict(sorted(sensitivity_transitions.items())),
        "alias_audit_counts": dict(Counter(row["status"] for row in audit)),
        "per_country": serializable_country,
        "query_level": {
            "definition": "shortcut rate = shortcut contexts / paper-token-eligible contexts; majority is strictly greater than one half",
            "num_queries": len(query_rows),
            "num_queries_with_original_shortcut_context": sum(
                row["original_shortcut_rate"] > 0 for row in query_rows
            ),
            "original_majority_shortcut_queries": sum(
                row["original_majority_shortcut"] for row in query_rows
            ),
            "final_majority_shortcut_queries": sum(
                row["final_majority_shortcut"] for row in query_rows
            ),
            "original_all_context_shortcut_queries": sum(
                row["original_all_context_shortcut"] for row in query_rows
            ),
            "final_all_context_shortcut_queries": sum(
                row["final_all_context_shortcut"] for row in query_rows
            ),
        },
        "limitations": [
            "Aliases use first-token scoring; full-name scoring was not performed.",
            "There is no wrong-country alias null control.",
            "Canonical names retain original first-token scoring while primary aliases must be complete single tokens.",
            "The score maximizes over a fixed alias set whose size differs by country.",
        ],
    }


def write_jsonl(path: Path, rows: Iterable[Mapping[str, Any]]) -> None:
    with open_text(path, "wt") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    args = parse_args()
    task_dir = PROJECT_DIR / "results" / args.task
    alias_root = PROJECT_DIR / "results" / "jlens_alias_reclassification" / args.task
    shard_dir = args.shard_directory or alias_root / "shards"
    original_path = args.original_jlens or task_dir / "jlens_evaluation.jsonl.gz"
    output_dir = args.output_directory or alias_root / "final"
    data_output = output_dir / "alias_reclassification.jsonl.gz"
    query_output = output_dir / "alias_reclassification_queries.jsonl"
    audit_output = output_dir / "alias_audit.json"
    summary_output = output_dir / "alias_reclassification_summary.json"
    ensure_outputs(
        (data_output, query_output, audit_output, summary_output), args.overwrite
    )

    catalog_paths = args.catalog_summary or [
        PROJECT_DIR / "results" / name / "baseline_summary.json"
        for name in SUPPORTED_TASKS
    ]
    alias_map, alias_metadata = load_aliases(args.aliases)
    policy = load_policy(args.policy)
    country_values = load_country_values(catalog_paths)

    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID, revision=STAGE_ONE_COMMIT, local_files_only=True
    )
    audit = build_alias_audit(
        alias_map, country_values, tokenizer, policy, task=args.task
    )
    primary = aliases_by_status(audit, "accepted")
    sensitivity = aliases_by_status(audit, "sensitivity_only")
    expected = args.expected_shortcut_records or EXPECTED_SHORTCUT_RECORDS[args.task]
    rows, sources = load_and_filter_shards(
        shard_dir,
        task=args.task,
        primary_by_country=primary,
        sensitivity_by_country=sensitivity,
        policy_version=policy["version"],
        expected_records=expected,
    )
    query_rows = build_query_results(
        read_jsonl(original_path), rows, task=args.task
    )
    summary = summarize(
        rows,
        query_rows,
        audit,
        sources,
        task=args.task,
        original_path=original_path,
        policy_path=args.policy,
    )
    summary["alias_catalog_metadata"] = dict(alias_metadata)
    summary["outputs"] = {
        "records": str(data_output),
        "queries": str(query_output),
        "audit": str(audit_output),
        "summary": str(summary_output),
    }

    write_jsonl(data_output, rows)
    write_jsonl(query_output, query_rows)
    audit_output.write_text(
        json.dumps(
            {
                "task": args.task,
                "policy": policy,
                "country_catalogs": [str(path) for path in catalog_paths],
                "aliases": audit,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    summary_output.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
