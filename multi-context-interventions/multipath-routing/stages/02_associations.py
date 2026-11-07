#!/usr/bin/env python3
"""Generate and freeze single-token answer associations for Stage 02."""
from __future__ import annotations

import argparse
import gzip
import json
import sys
from pathlib import Path
from typing import Any, Mapping

EXPERIMENT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_RESULTS = EXPERIMENT_DIR / "results"
DEFAULT_CONFIG = EXPERIMENT_DIR / "configs/cues.json"
DEFAULT_ALIASES = EXPERIMENT_DIR / "configs/answer_aliases.json"
DEFAULT_STATIC_CATALOG = EXPERIMENT_DIR / "configs/predefined_associations.json"
sys.path.insert(0, str(EXPERIMENT_DIR))

from multipath.associations import (TARGET_MODES, WORD, build_candidate_pool, build_target_inventory,
    finalize_associations, inventory_targets, leave_one_out_contrast, load_generation_specs,
    load_static_catalog, render_scoring_prompts, surface_piece_keys)
from multipath.prepare import comparison_key, load_alias_config, load_json, read_jsonl


def atomic_json(path: Path, value: Any, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    try:
        temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def stage_directory(root: Path, task: str) -> Path:
    return root / task / "icl_10" / "02_associations"


def inventory_path(root: Path, task: str) -> Path:
    return stage_directory(root, task) / "target_inventory.json"


def mode_directory(root: Path, task: str, mode: str) -> Path:
    return stage_directory(root, task) / mode


def load_tokenizer(inventory: Mapping[str, Any]):
    from transformers import AutoTokenizer

    metadata = inventory.get("model", {})
    model_id, commit = metadata.get("model"), metadata.get("model_commit")
    if not isinstance(model_id, str) or not isinstance(commit, str):
        raise ValueError("inventory lacks pinned tokenizer metadata")
    return AutoTokenizer.from_pretrained(model_id, revision=commit)


def command_inventory(args: argparse.Namespace) -> None:
    configured = load_json(args.config)["tasks"]
    tasks = args.task or list(configured)
    specs = load_generation_specs(args.config, tasks)
    for task in tasks:
        prepared = args.results_root / task / "icl_10" / "01_prepare" / "prompt_targets.jsonl.gz"
        inventory = build_target_inventory(prepared, task, specs[task].answer_type)
        inventory["generation_config"] = str(args.config)
        inventory["provider"] = specs[task].provider
        inventory["templates"] = list(specs[task].templates)
        output = inventory_path(args.results_root, task)
        atomic_json(output, inventory, args.overwrite)
        print(json.dumps({"task": task, "output": str(output),
                          "true_targets": len(inventory["modes"]["true"]),
                          "model_targets": len(inventory["modes"]["model"]),
                          "task_intermediates": len(inventory["task_intermediates"])}), flush=True)


def command_build_static(args: argparse.Namespace) -> None:
    """Validate and freeze a predefined association catalog; never load model weights."""

    inventory = load_json(inventory_path(args.results_root, args.task))
    spec = load_generation_specs(args.config, [args.task])[args.task]
    targets = inventory_targets(inventory, args.mode)
    target_by_answer = {target["answer"]: target for target in targets}
    catalog = load_static_catalog(args.catalog, args.task, args.mode)
    catalog_settings = load_json(args.catalog).get("tasks", {}).get(args.task, {})
    unavailable = catalog_settings.get("no_reliable_associations", {}).get(args.mode, {})
    if not isinstance(unavailable, dict) or any(
            answer not in catalog or catalog[answer] or not isinstance(reason, str) or not reason.strip()
            for answer, reason in unavailable.items()):
        raise ValueError("unavailable decisions require empty lists and an explicit review reason")
    explicit_answers = set(catalog_settings.get(args.mode, {}))
    unknown_explicit = explicit_answers - set(target_by_answer)
    unused_inherited = (set(catalog) - set(target_by_answer)) - explicit_answers
    missing = set(target_by_answer) - set(catalog)
    if unknown_explicit or (missing and not args.allow_partial):
        raise ValueError(
            f"catalog coverage mismatch: missing={len(missing)}, "
            f"unknown_explicit={sorted(unknown_explicit)[:3]}"
        )
    catalog = {answer: words for answer, words in catalog.items() if answer in target_by_answer}
    aliases_by_task, _ = load_alias_config(args.alias_config, [args.task])
    aliases = aliases_by_task[args.task]
    tokenizer = load_tokenizer(inventory)
    rows = []
    for answer in sorted(catalog, key=lambda value: target_by_answer[value]["target_id"]):
        target = target_by_answer[answer]
        pool, intermediate_words, capital_words, name_pieces, rejected = build_candidate_pool(
            tokenizer=tokenizer, target=target, generations=[", ".join(catalog[answer])],
            task_intermediates=inventory["task_intermediates"],
            aliases=aliases.get(answer, []), spec=spec)
        rows.append({"schema_version": 2, "task": args.task, "target_mode": args.mode, **target,
                     "curated_words": catalog[answer], "candidate_pool": pool,
                     "generated_intermediate_words": intermediate_words,
                     "generic_capital_words_removed": capital_words,
                     "generic_name_pieces_removed": name_pieces,
                     "audit": {"rejected_counts": dict(rejected)},
                     "settings": {"provider": "static_reviewed_catalog", "catalog": str(args.catalog),
                                  "top_n": spec.top_n,
                                  "analysis_k_values": list(spec.analysis_k_values),
                                  "primary_k": spec.primary_k,
                                  "subset_selection_rule":
                                      "lowest answer-document frequency; curated-order tie-break",
                                  "model_inference": False}})
    final_rows, merge_audit = finalize_associations(rows, spec, filter_generic=True)
    for row in final_rows:
        reason = unavailable.get(row["answer"])
        row["association_status"] = ("no_reliable_associations" if reason else
            "available" if len(row["associations"]) >= spec.primary_k else
            "insufficient_validated_words")
        row["association_unavailable_reason"] = reason
    merge_audit["num_no_reliable_associations"] = len(unavailable)
    output = args.output or mode_directory(args.results_root, args.task, args.mode) / "static_review" / "associations_static.jsonl.gz"
    summary = output.with_name("summary.json")
    if (output.exists() or summary.exists()) and not args.overwrite:
        raise FileExistsError(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.name + ".tmp")
    try:
        with gzip.open(temporary, "wt", encoding="utf-8") as handle:
            for row in final_rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        temporary.replace(output)
        atomic_json(summary, {"schema_version": 2, "task": args.task, "target_mode": args.mode,
            "num_catalog_answers": len(final_rows), "num_inventory_answers": len(targets),
            "partial_catalog": bool(missing), "missing_answers": sorted(missing), **merge_audit,
            "unused_inherited_answers": sorted(unused_inherited),
            "output": str(output), "catalog": str(args.catalog), "model_inference": False}, args.overwrite)
    finally:
        temporary.unlink(missing_ok=True)
    print(json.dumps({"output": str(output), "num_answers": len(final_rows), "missing": len(missing), **merge_audit}), flush=True)


def atomic_torch(path: Path, value: Any, overwrite: bool) -> None:
    import torch

    if path.exists() and not overwrite:
        raise FileExistsError(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    try:
        torch.save(value, temporary)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def command_score_cues(args: argparse.Namespace) -> None:
    """Score fixed next-token cues and save one reusable row per answer."""

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if args.batch_size <= 0:
        raise ValueError("batch_size must be positive")
    inventory = load_json(inventory_path(args.results_root, args.task))
    spec = load_generation_specs(args.config, [args.task])[args.task]
    targets = inventory_targets(inventory, args.mode)
    metadata = inventory["model"]
    tokenizer = AutoTokenizer.from_pretrained(
        metadata["model"], revision=metadata["model_commit"],
        local_files_only=not args.allow_download, padding_side="left")
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        metadata["model"], revision=metadata["model_commit"], dtype=torch.bfloat16,
        device_map="auto", local_files_only=not args.allow_download)
    model.eval(); model.requires_grad_(False)
    device = model.get_input_embeddings().weight.device
    batches = []
    with torch.inference_mode():
        for start in range(0, len(targets), args.batch_size):
            batch = targets[start:start + args.batch_size]
            prompts = [prompt for target in batch
                       for prompt in render_scoring_prompts(target["answer"], spec)]
            encoded = tokenizer(prompts, padding=True, return_tensors="pt").to(device)
            logits = model(**encoded, use_cache=False).logits[:, -1].detach().to(
                device="cpu", dtype=torch.bfloat16)
            logits = logits.reshape(len(batch), len(spec.scoring_templates), -1).float().mean(1).to(torch.bfloat16)
            batches.append(logits)
            print(f"cue scores: {min(start + len(batch), len(targets))}/{len(targets)}", flush=True)
    scores = torch.cat(batches)
    output = args.output or mode_directory(args.results_root, args.task, args.mode) / "prompted/raw_cue_scores.pt"
    atomic_torch(output, {
        "schema_version": 1, "task": args.task, "target_mode": args.mode,
        "target_ids": [target["target_id"] for target in targets],
        "answers": [target["answer"] for target in targets],
        "scoring_templates": list(spec.scoring_templates), "scores": scores,
        "model": metadata, "score_dtype": "bfloat16",
    }, args.overwrite)
    print(json.dumps({"output": str(output), "shape": list(scores.shape)}), flush=True)


def surface_token_ids(tokenizer: Any, surfaces: list[str]) -> set[int]:
    """Return every tokenizer piece used inside the supplied surfaces."""

    output: set[int] = set()
    for surface in surfaces:
        stripped = surface.strip()
        if not stripped:
            continue
        output.update(int(value) for value in tokenizer.encode(stripped, add_special_tokens=False))
        output.update(int(value) for value in tokenizer.encode(f" {stripped}", add_special_tokens=False))
    return output


def is_strict_surface_fragment(key: str, blocked_surfaces: set[str]) -> bool:
    """Reject BPE prefixes of names while retaining unrelated short words."""

    return len(key) >= 3 and any(key != blocked and key in blocked for blocked in blocked_surfaces)


def prompted_word_catalog(tokenizer: Any, vocabulary_size: int, excluded_keys: set[str],
                          excluded_token_ids: set[int], accepted_words: set[str]) -> tuple[list[int], list[str]]:
    token_ids, surfaces = [], []
    for token_id in range(vocabulary_size):
        decoded = tokenizer.decode([token_id])
        surface = decoded.strip()
        key = comparison_key(surface)
        if (token_id not in excluded_token_ids and decoded and decoded[0].isspace()
                and WORD.fullmatch(surface) and key in accepted_words and key not in excluded_keys):
            token_ids.append(token_id); surfaces.append(surface)
    return token_ids, surfaces


def command_build_prompted(args: argparse.Namespace) -> None:
    """Turn cached cue scores into filtered, contrastive association lists."""

    import torch

    if min(args.search_k, args.candidate_pool_size, args.progress_every) <= 0:
        raise ValueError("search and progress settings must be positive")
    if args.search_k < args.candidate_pool_size:
        raise ValueError("search_k must be at least candidate_pool_size")
    inventory = load_json(inventory_path(args.results_root, args.task))
    spec = load_generation_specs(args.config, [args.task])[args.task]
    targets = inventory_targets(inventory, args.mode)
    score_path = args.scores or mode_directory(args.results_root, args.task, args.mode) / "prompted/raw_cue_scores.pt"
    artifact = torch.load(score_path, map_location="cpu", weights_only=False)
    expected_ids = [target["target_id"] for target in targets]
    if (artifact.get("schema_version") != 1 or artifact.get("task") != args.task
            or artifact.get("target_mode") != args.mode or artifact.get("target_ids") != expected_ids
            or artifact.get("answers") != [target["answer"] for target in targets]):
        raise ValueError("cue-score artifact does not match the current inventory")
    scores = artifact.get("scores")
    if not isinstance(scores, torch.Tensor) or scores.ndim != 2 or scores.shape[0] != len(targets):
        raise ValueError("cue-score artifact has invalid score shape")
    comparison_mean = scores.float().mean(0)
    aliases_by_task, _ = load_alias_config(args.alias_config, [args.task])
    aliases = aliases_by_task[args.task]
    tokenizer = load_tokenizer(inventory)
    if not args.word_list.is_file():
        raise FileNotFoundError(args.word_list)
    accepted_words = {
        comparison_key(line) for line in args.word_list.read_text(
            encoding="utf-8", errors="ignore").splitlines()
        if WORD.fullmatch(line.strip())
    }
    prepared_path = args.results_root / args.task / "icl_10/01_prepare/prompt_targets.jsonl.gz"
    for record in read_jsonl(prepared_path):
        accepted_words.update(surface_piece_keys([record["x"]]))
    excluded = set(spec.stopwords) | set(spec.generic_capital_words) | set(spec.excluded_generic_name_pieces)
    excluded |= surface_piece_keys(inventory["task_intermediates"])
    intermediate_surface_keys = {comparison_key(value) for value in inventory["task_intermediates"]}
    intermediate_token_ids = surface_token_ids(tokenizer, inventory["task_intermediates"])
    word_ids, word_surfaces = prompted_word_catalog(
        tokenizer, scores.shape[1], excluded, intermediate_token_ids, accepted_words)
    word_id_tensor = torch.tensor(word_ids, dtype=torch.long)
    rows = []
    search_k = min(args.search_k, len(word_ids))
    for index, target in enumerate(targets):
        raw = scores[index].float()
        contrast = leave_one_out_contrast(raw, comparison_mean, len(targets))
        answer_keys = surface_piece_keys([target["answer"], *aliases.get(target["answer"], [])])
        answer_surface_keys = {
            comparison_key(value) for value in [target["answer"], *aliases.get(target["answer"], [])]
        }
        answer_token_ids = surface_token_ids(
            tokenizer, [target["answer"], *aliases.get(target["answer"], [])])
        candidate_scores = contrast[word_id_tensor]
        _, order = torch.topk(candidate_scores, k=search_k)
        pool = []
        seen_keys: set[str] = set()
        for word_rank, word_index in enumerate(order.tolist(), start=1):
            surface = word_surfaces[word_index]
            key = comparison_key(surface)
            token_id = word_ids[word_index]
            if (key in seen_keys or key in answer_keys or token_id in answer_token_ids
                    or is_strict_surface_fragment(key, intermediate_surface_keys)
                    or is_strict_surface_fragment(key, answer_surface_keys)):
                continue
            seen_keys.add(key)
            pool.append({
                "text": surface, "token_id": token_id, "generation_count": 1,
                "cue_indices": list(range(len(spec.scoring_templates))),
                "first_seen": word_rank, "raw_score": float(raw[token_id].item()),
                "contrastive_score": float(contrast[token_id].item()),
                "contrastive_word_rank": word_rank,
            })
            if len(pool) == args.candidate_pool_size:
                break
        if len(pool) < spec.top_n:
            raise ValueError(f"{target['answer']!r} has only {len(pool)} prompted candidates")
        rows.append({
            "schema_version": 2, "task": args.task, "target_mode": args.mode, **target,
            "candidate_pool": pool, "generated_intermediate_words": [],
            "generic_capital_words_removed": [], "generic_name_pieces_removed": [],
            "audit": {"word_vocabulary_size": len(word_ids), "search_k": search_k},
            "settings": {"provider": "prompted_next_token_contrast",
                "scoring_templates": list(spec.scoring_templates), "top_n": spec.top_n,
                "analysis_k_values": list(spec.analysis_k_values), "primary_k": spec.primary_k,
                "contrast": "target cue mean minus leave-one-out same-type answer mean",
                "model_inference": True},
        })
        if (index + 1) % args.progress_every == 0:
            print(f"prompted candidates: {index + 1}/{len(targets)}", flush=True)
    final_rows, merge_audit = finalize_associations(rows, spec, filter_generic=True)
    output = args.output or mode_directory(args.results_root, args.task, args.mode) / "prompted/associations_prompted.jsonl.gz"
    summary = args.summary_output or output.with_name("summary.json")
    if (output.exists() or summary.exists()) and not args.overwrite:
        raise FileExistsError(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.name + ".tmp")
    try:
        with gzip.open(temporary, "wt", encoding="utf-8") as handle:
            for row in final_rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        atomic_json(summary, {
            "schema_version": 2, "task": args.task, "target_mode": args.mode,
            "provider": "prompted_next_token_contrast", "num_answers": len(final_rows),
            "scores": str(score_path), **merge_audit, "output": str(output),
        }, args.overwrite)
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    print(json.dumps({"output": str(output), "num_answers": len(final_rows), **merge_audit}), flush=True)


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--results-root", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--overwrite", action="store_true")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    inventory = commands.add_parser("inventory"); add_common(inventory)
    inventory.add_argument("--task", action="append", default=[]); inventory.set_defaults(function=command_inventory)
    static = commands.add_parser("build-static"); add_common(static)
    static.add_argument("--task", required=True); static.add_argument("--mode", required=True, choices=TARGET_MODES)
    static.add_argument("--catalog", type=Path, default=DEFAULT_STATIC_CATALOG)
    static.add_argument("--alias-config", type=Path, default=DEFAULT_ALIASES)
    static.add_argument("--allow-partial", action="store_true"); static.add_argument("--output", type=Path)
    static.set_defaults(function=command_build_static)
    score = commands.add_parser("score-cues"); add_common(score)
    score.add_argument("--task", required=True); score.add_argument("--mode", required=True, choices=TARGET_MODES)
    score.add_argument("--batch-size", type=int, default=16); score.add_argument("--output", type=Path)
    score.add_argument("--allow-download", action="store_true"); score.set_defaults(function=command_score_cues)
    prompted = commands.add_parser("build-prompted"); add_common(prompted)
    prompted.add_argument("--task", required=True); prompted.add_argument("--mode", required=True, choices=TARGET_MODES)
    prompted.add_argument("--scores", type=Path); prompted.add_argument("--alias-config", type=Path, default=DEFAULT_ALIASES)
    prompted.add_argument("--search-k", type=int, default=512)
    prompted.add_argument("--candidate-pool-size", type=int, default=100)
    prompted.add_argument("--progress-every", type=int, default=100)
    prompted.add_argument("--word-list", type=Path, default=Path("/usr/share/dict/words"))
    prompted.add_argument("--output", type=Path); prompted.add_argument("--summary-output", type=Path)
    prompted.set_defaults(function=command_build_prompted)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command in {"score-cues", "build-prompted"}:
        raise SystemExit("OLMo association prompting is disabled. Use build-static with manually written lists.")
    args.function(args)


if __name__ == "__main__":
    main()
