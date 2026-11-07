#!/usr/bin/env python3
"""Assemble and validate manually written lists across tasks and target modes.

Only the two named JSON sources are read for association words. Prompted
artifacts and cue scores are never inputs. Missing lists stay missing; this
script does not invent replacements or silently select a smaller population.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

EXPERIMENT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(EXPERIMENT_DIR))

from multipath.associations import load_static_catalog
from multipath.prepare import load_json, read_jsonl, sha256


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    try:
        temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-root", type=Path, default=EXPERIMENT_DIR / "results")
    args = parser.parse_args()
    base_path = EXPERIMENT_DIR / "configs/predefined_associations.json"
    additions_path = EXPERIMENT_DIR / "configs/manual_association_additions.json"
    config_path = EXPERIMENT_DIR / "configs/cues.json"
    base = load_json(base_path)
    additions = load_json(additions_path)
    if additions.get("schema_version") != 1:
        raise ValueError("unsupported manual-additions schema")
    libraries = {kind: dict(values) for kind, values in additions["answer_types"].items()}
    unavailable = additions.get("no_reliable_associations", {})
    source_by_type = {kind: {answer: str(additions_path) for answer in words}
                      for kind, words in libraries.items()}
    for task in base["tasks"]:
        # Both original tasks have city answers. Existing lists take priority
        # over supplemental lists so the accepted true-answer lists stay intact.
        for answer, words in load_static_catalog(base_path, task, "true").items():
            libraries.setdefault("city", {})[answer] = words
            source_by_type.setdefault("city", {})[answer] = str(base_path)
    for kind, words_by_answer in libraries.items():
        for answer, words in words_by_answer.items():
            if not isinstance(words, list) or not words or any(
                    not isinstance(word, str) or not word.strip() for word in words):
                raise ValueError(f"invalid manual list: {kind}/{answer}")
            if len({word.strip().casefold() for word in words}) != len(words):
                raise ValueError(f"duplicate manual word: {kind}/{answer}")

    compiled = {"schema_version": 1, "provenance": "Exact-answer reuse of manually written lists; no OLMo association inference.",
                "sources": {str(path): sha256(path) for path in (base_path, additions_path)},
                "tasks": {}}
    inventories = {}
    for task in load_json(config_path)["tasks"]:
        path = args.results_root / task / "icl_10/02_associations/target_inventory.json"
        inventory = load_json(path)
        if inventory["task"] != task:
            raise ValueError(f"wrong inventory: {path}")
        inventories[task] = inventory
        kind = inventory["answer_type"]
        library = libraries[kind]
        settings = compiled["tasks"][task] = {"manual_sources": {}}
        settings["no_reliable_associations"] = {}
        for mode in ("true", "model"):
            settings[mode] = {target["answer"]: library[target["answer"]]
                              for target in inventory["modes"][mode]
                              if target["answer"] in library}
            settings["manual_sources"][mode] = {
                answer: source_by_type[kind][answer] for answer in settings[mode]}
            decisions = {target["answer"]: unavailable[kind][target["answer"]]
                         for target in inventory["modes"][mode]
                         if target["answer"] in unavailable.get(kind, {})}
            if set(decisions) & set(settings[mode]):
                raise ValueError("an answer cannot have both a manual list and an unavailable decision")
            settings["no_reliable_associations"][mode] = decisions
            settings[mode].update({answer: [] for answer in decisions})
    root = args.results_root / "manual_associations"
    compiled_path = root / "compiled_manual_catalog.json"
    write_json(compiled_path, compiled)
    report = {"model_inference": False, "prompted_artifacts_accepted": False,
              "catalog": str(compiled_path), "catalog_sha256": sha256(compiled_path),
              "status": "incomplete", "tasks": {}}
    for task, inventory in inventories.items():
        task_report = report["tasks"][task] = {}
        for mode in ("true", "model"):
            directory = args.results_root / task / f"icl_10/02_associations/{mode}/manual_replacement"
            output = directory / "associations_static.jsonl.gz"
            subprocess.run([
                sys.executable, str(EXPERIMENT_DIR / "stages/02_associations.py"),
                "build-static", "--results-root", str(args.results_root), "--task", task,
                "--mode", mode, "--catalog", str(compiled_path), "--allow-partial",
                "--output", str(output), "--overwrite"], check=True)
            summary = load_json(directory / "summary.json")
            accepted = {row["answer"]: row for row in read_jsonl(output)}
            pending = []
            for target in inventory["modes"][mode]:
                row = accepted.get(target["answer"])
                if row and row.get("association_status") == "no_reliable_associations":
                    continue
                count = len(row["associations"]) if row else 0
                if row is None or count < summary["primary_k"]:
                    pending.append({**target, "reason": "manual_list_missing" if row is None
                                    else "fewer_than_primary_k_after_validation",
                                    "accepted_word_count": count})
            write_json(directory / "pending_review.json", pending)
            task_report[mode] = {
                "inventory_answers": len(inventory["modes"][mode]),
                "manual_lists": len(accepted) - summary.get("num_no_reliable_associations", 0),
                "k_coverage": summary["k_coverage"],
                "no_reliable_associations": summary.get("num_no_reliable_associations", 0),
                "pending_answers": len(pending), "complete": not pending,
                "output": str(output), "pending_review": str(directory / "pending_review.json")}
    report["status"] = ("complete" if all(mode["complete"] for task in report["tasks"].values()
                                          for mode in task.values()) else "incomplete")
    write_json(root / "coverage.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
