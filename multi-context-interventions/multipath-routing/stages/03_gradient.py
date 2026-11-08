#!/usr/bin/env python3
"""Rank vocabulary directions by predicted effect on a target answer.

For each selected Stage-01 prompt, this runner differentiates two objectives
with respect to one residual-stream position:

``log_prob``   the full target answer log probability;
``log_share``  log P(target first token) minus the log-sum-exp over the first
               tokens of every target answer in the task (the target's share
               among answers).

At each of the six fitted J-Lens layers it scores every vocabulary direction
``unit(J_l.T @ (gamma * w_t))`` (``gamma`` is the final RMSNorm weight, as in
the earlier generalized-task experiments). The output stores exact ranks for
the frozen Stage-02 association words, a small top-word list, and summary
statistics of the word-token score distribution, not the dense score vector.
"""
from __future__ import annotations

import argparse
from collections.abc import Mapping, Sequence
import gzip
import json
from pathlib import Path
import re
import sys
from typing import Any

import torch

EXPERIMENT_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = EXPERIMENT_DIR.parent
JLENS_ROOT = PROJECT_ROOT.parent / "JLens"
VENDORED_JLENS = JLENS_ROOT / "vendor/jacobian-lens"
DEFAULT_LENS = JLENS_ROOT / "results/fit_1000/merged/jacobian_lens.pt"
DEFAULT_RESULTS = EXPERIMENT_DIR / "results"
SOURCE_LAYERS = (12, 16, 18, 20, 22, 24)
EXPECTED_FIT_PROMPTS = 1000
MODEL_ID = "allenai/Olmo-3-1025-7B"
MODEL_COMMIT = "373bad25002f1624757a73235c5ca844c6375c25"
WORD = re.compile(r"^[^\W\d_]+(?:[-'’][^\W\d_]+)*$", flags=re.UNICODE)
OBJECTIVES = ("log_prob", "log_share")
DIRECTION = "unit(J_l.T @ (final_norm_weight * lm_head_row))"
SCORE_QUANTILES = (0.5, 0.9, 0.99)
sys.path.insert(0, str(EXPERIMENT_DIR))

from multipath.gradient import (full_answer_log_probability, select_gradient_records,
    selected_vocabulary_rankings, unit_transported_directions)
from multipath.prepare import read_jsonl, sha256


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True)
    parser.add_argument("--target-mode", choices=("true", "model"), required=True)
    parser.add_argument("--split", choices=("selection", "test"), required=True)
    parser.add_argument("--position", choices=("final_prompt", "entity_last"), default="final_prompt")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--associations", type=Path)
    parser.add_argument("--lens", type=Path, default=DEFAULT_LENS)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--summary-output", type=Path)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--num-prompts", type=int, required=True)
    parser.add_argument("--context-variant", type=int,
                        help="use only this context variant (one prompt per query entity)")
    parser.add_argument("--vocabulary-chunk-size", type=int, default=2048)
    parser.add_argument("--top-words", type=int, default=50)
    parser.add_argument("--max-seq-len", type=int, default=512)
    parser.add_argument("--progress-every", type=int, default=1)
    parser.add_argument("--allow-download", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def load_associations(path: Path, task: str, target_mode: str) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for row_number, row in enumerate(read_jsonl(path), start=1):
        answer = row.get("answer")
        if row.get("task") != task or row.get("target_mode") != target_mode:
            raise ValueError(f"association row {row_number} has wrong task or target mode")
        if not isinstance(answer, str) or not answer or answer in output:
            raise ValueError(f"association row {row_number} has invalid or duplicate answer")
        settings = row.get("settings", {})
        if (settings.get("provider") != "static_reviewed_catalog"
                or settings.get("model_inference") is not False):
            raise ValueError("Stage 03 requires manually written, tokenizer-validated associations")
        associations = row.get("associations")
        unavailable = row.get("association_status") == "no_reliable_associations"
        if unavailable and (associations != [] or not row.get("association_unavailable_reason")):
            raise ValueError(f"association row {row_number} has an invalid unavailable decision")
        if not isinstance(associations, list) or (not associations and not unavailable):
            raise ValueError(f"association row {row_number} has no words")
        output[answer] = row
    if not output:
        raise ValueError("association artifact is empty")
    return output


def answer_token_ids(tokenizer: Any, prompt: str, answer: str) -> list[int]:
    continuation = answer if prompt.endswith((" ", "\n", "\t")) else f" {answer}"
    token_ids = [int(value) for value in tokenizer.encode(continuation, add_special_tokens=False)]
    if not token_ids:
        raise ValueError("target answer tokenizes to an empty sequence")
    return token_ids


def selected_position(tokenizer: Any, prompt: str, entity: str, policy: str) -> tuple[int, str]:
    prompt_ids = tokenizer.encode(prompt, add_special_tokens=False)
    if not prompt_ids:
        raise ValueError("prompt tokenizes to an empty sequence")
    if policy == "final_prompt":
        return len(prompt_ids) - 1, tokenizer.decode([prompt_ids[-1]])
    suffix = f"Q: {entity}\nA:"
    if not prompt.endswith(suffix):
        raise ValueError("prompt does not end in the expected final query")
    entity_end = len(prompt) - len("\nA:")
    prefix_ids = tokenizer.encode(prompt[:entity_end], add_special_tokens=False)
    if not prefix_ids:
        raise ValueError("entity prefix tokenizes to an empty sequence")
    return len(prefix_ids) - 1, tokenizer.decode([prefix_ids[-1]])


def word_token_mask(tokenizer: Any, vocabulary_size: int) -> torch.Tensor:
    values = []
    for token_id in range(vocabulary_size):
        text = tokenizer.decode([token_id])
        stripped = text.strip()
        values.append(bool(text and text[0].isspace() and WORD.fullmatch(stripped)))
    return torch.tensor(values, dtype=torch.bool)


def imported_runtime() -> tuple[Any, Any, Any]:
    if not (VENDORED_JLENS / "jlens/__init__.py").is_file():
        raise FileNotFoundError(VENDORED_JLENS)
    sys.path.insert(0, str(VENDORED_JLENS))
    import jlens
    from transformers import AutoModelForCausalLM, AutoTokenizer
    return jlens, AutoModelForCausalLM, AutoTokenizer


def load_lens(path: Path, jlens: Any) -> Any:
    lens = jlens.JacobianLens.load(str(path))
    layers = tuple(int(value) for value in lens.source_layers)
    if layers != SOURCE_LAYERS or int(lens.n_prompts) != EXPECTED_FIT_PROMPTS:
        raise ValueError("fitted J-Lens metadata does not match the verified six-layer fit")
    if set(lens.jacobians) != set(SOURCE_LAYERS):
        raise ValueError("fitted J-Lens lacks a required Jacobian")
    return lens


def atomic_paths(output: Path, summary: Path, overwrite: bool) -> tuple[Path, Path]:
    if not overwrite and (output.exists() or summary.exists()):
        raise FileExistsError(output if output.exists() else summary)
    output.parent.mkdir(parents=True, exist_ok=True)
    summary.parent.mkdir(parents=True, exist_ok=True)
    return output.with_name(output.name + ".tmp"), summary.with_name(summary.name + ".tmp")


def capture_prompt_gradients(
    model: Any,
    tokenizer: Any,
    records: Sequence[Mapping[str, Any]],
    *,
    answer_first_ids: torch.Tensor,
    position_policy: str,
    max_seq_len: int,
    progress_every: int,
) -> tuple[list[dict[str, Any]], dict[str, dict[int, torch.Tensor]]]:
    captured: dict[int, torch.Tensor] = {}
    gradients: dict[str, dict[int, list[torch.Tensor]]] = {
        objective: {layer: [] for layer in SOURCE_LAYERS} for objective in OBJECTIVES}
    handles = []

    def hook_for(layer: int):
        def capture(_module: Any, _inputs: Any, output: Any) -> None:
            captured[layer] = output[0] if isinstance(output, tuple) else output
        return capture

    for layer in SOURCE_LAYERS:
        handles.append(model.model.layers[layer].register_forward_hook(hook_for(layer)))
    handles.append(model.get_input_embeddings().register_forward_hook(
        lambda _module, _inputs, output: output.requires_grad_(True)))

    metadata = []
    input_device = model.get_input_embeddings().weight.device
    try:
        for index, record in enumerate(records, start=1):
            captured.clear()
            prompt = record["prompt"]
            prompt_ids = [int(value) for value in tokenizer.encode(prompt, add_special_tokens=False)]
            target_ids = answer_token_ids(tokenizer, prompt, record["gradient_target_answer"])
            if len(prompt_ids) + len(target_ids) > max_seq_len:
                raise ValueError(f"{record['prompt_instance_id']} exceeds max_seq_len")
            position, position_token = selected_position(tokenizer, prompt, record["x"], position_policy)
            model.zero_grad(set_to_none=True)
            input_ids = torch.tensor([prompt_ids + target_ids], device=input_device)
            outputs = model(input_ids=input_ids, use_cache=False)
            start = len(prompt_ids) - 1
            logits = outputs.logits[0, start:start + len(target_ids)]
            first = logits[0].float().log_softmax(dim=-1)
            if int(target_ids[0]) not in set(answer_first_ids.tolist()):
                raise ValueError("target first token is missing from the task answer set")
            values = {
                "log_prob": full_answer_log_probability(logits, target_ids),
                "log_share": first[int(target_ids[0])]
                - first[answer_first_ids.to(first.device)].logsumexp(dim=-1),
            }
            if set(captured) != set(SOURCE_LAYERS):
                raise RuntimeError("not every fitted layer was captured")
            layer_tensors = [captured[layer] for layer in SOURCE_LAYERS]
            for objective in OBJECTIVES:
                grads = torch.autograd.grad(values[objective], layer_tensors, retain_graph=True)
                for layer, gradient in zip(SOURCE_LAYERS, grads):
                    gradients[objective][layer].append(gradient[0, position].detach().float().cpu())
            metadata.append({
                "target_token_ids": target_ids,
                "target_num_tokens": len(target_ids),
                "baseline_target_log_probability": float(values["log_prob"].detach().item()),
                "baseline_target_log_share": float(values["log_share"].detach().item()),
                "measurement_position": position,
                "measurement_position_token": position_token,
                "prompt_num_tokens": len(prompt_ids),
            })
            if index % progress_every == 0:
                print(f"captured gradients: {index}/{len(records)}", flush=True)
    finally:
        for handle in handles:
            handle.remove()
    return metadata, {objective: {layer: torch.stack(values) for layer, values in by_layer.items()}
                      for objective, by_layer in gradients.items()}


def ids_and_words(association_row: Mapping[str, Any]) -> tuple[list[int], list[str]]:
    ids = [int(item["token_id"]) for item in association_row["associations"]]
    words = [str(item["text"]) for item in association_row["associations"]]
    if len(ids) != len(set(ids)):
        raise ValueError("association artifact repeats a token ID")
    return ids, words


def annotate_association_rows(
    rankings: list[dict[str, Any]],
    association_row: Mapping[str, Any],
    scores: torch.Tensor,
    mask: torch.Tensor,
) -> list[dict[str, Any]]:
    subsets = association_row.get("association_subsets", {})
    for result in rankings:
        token_id = int(result["token_id"])
        token_score = scores[token_id]
        result["word_vocabulary_rank"] = 1 + int((scores[mask] > token_score).sum().item())
        result["included_in_k"] = [int(k) for k, subset in subsets.items()
            if subset.get("available") and token_id in subset.get("token_ids", [])]
    return rankings


def score_gradients(
    model: Any,
    tokenizer: Any,
    lens: Any,
    records: Sequence[Mapping[str, Any]],
    associations: Mapping[str, Mapping[str, Any]],
    gradients: Mapping[str, Mapping[int, torch.Tensor]],
    *,
    chunk_size: int,
    top_words: int,
) -> list[list[dict[str, Any]]]:
    output_embedding = model.lm_head.weight.detach()
    device = output_embedding.device
    final_norm_weight = model.model.norm.weight.detach().to(device=device, dtype=torch.float32)
    vocabulary_size = int(output_embedding.shape[0])
    mask = word_token_mask(tokenizer, vocabulary_size)
    num_word_tokens = int(mask.sum().item())
    quantiles = torch.tensor(SCORE_QUANTILES)
    layer_outputs: list[list[dict[str, Any]]] = [[] for _ in records]

    for objective, layer, all_scores in iterate_scores(
            lens, output_embedding, final_norm_weight, gradients, len(records),
            vocabulary_size, chunk_size):
        for prompt_index, record in enumerate(records):
            target = record["gradient_target_answer"]
            association_row = associations[target]
            association_ids, association_words = ids_and_words(association_row)
            scores = all_scores[prompt_index]
            rankings = (selected_vocabulary_rankings(scores, association_ids, association_words)
                        if association_ids else [])
            rankings = annotate_association_rows(rankings, association_row, scores, mask)
            for result in rankings:
                result["word_vocabulary_percentile"] = 1.0 - (
                    (result["word_vocabulary_rank"] - 1) / max(1, num_word_tokens - 1))
            word_scores = scores[mask]
            masked = scores.masked_fill(~mask, float("-inf"))
            count = min(top_words, num_word_tokens)
            top_scores, top_ids = torch.topk(masked, k=count)
            layer_outputs[prompt_index].append({
                "objective": objective,
                "layer": layer,
                "gradient_l2": float(gradients[objective][layer][prompt_index].norm().item()),
                "word_score_distribution": {
                    "mean": float(word_scores.mean()),
                    "std": float(word_scores.std()),
                    **{f"q{int(q * 100)}": float(v) for q, v in
                       zip(SCORE_QUANTILES, torch.quantile(word_scores, quantiles).tolist())},
                },
                "association_words": rankings,
                "top_word_tokens": [{
                    "word_vocabulary_rank": rank,
                    "full_vocabulary_rank": 1 + int((scores > score).sum().item()),
                    "token_id": int(token_id),
                    "word": tokenizer.decode([int(token_id)]).strip(),
                    "directional_score": float(score),
                    "is_association": int(token_id) in association_ids,
                } for rank, (token_id, score) in enumerate(zip(top_ids.tolist(), top_scores.tolist()), start=1)],
                "num_full_vocabulary_tokens": vocabulary_size,
                "num_word_vocabulary_tokens": num_word_tokens,
            })
        print(f"scored vocabulary directions: {objective}, layer {layer}", flush=True)
    return layer_outputs


def iterate_scores(lens: Any, output_embedding: torch.Tensor, final_norm_weight: torch.Tensor,
                   gradients: Mapping[str, Mapping[int, torch.Tensor]], num_prompts: int,
                   vocabulary_size: int, chunk_size: int):
    """Yield ``(objective, layer, scores[num_prompts, vocabulary])`` on CPU.

    Directions are built once per layer chunk and applied to both objectives.
    """

    device = output_embedding.device
    for layer in SOURCE_LAYERS:
        jacobian = lens.jacobians[layer].detach().to(device=device, dtype=torch.float32)
        prompt_gradients = {objective: gradients[objective][layer].to(device=device, dtype=torch.float32)
                            for objective in OBJECTIVES}
        scores = {objective: torch.empty((num_prompts, vocabulary_size), dtype=torch.float32)
                  for objective in OBJECTIVES}
        for start in range(0, vocabulary_size, chunk_size):
            stop = min(start + chunk_size, vocabulary_size)
            rows = output_embedding[start:stop].float() * final_norm_weight[None, :]
            directions = unit_transported_directions(jacobian, rows)
            for objective in OBJECTIVES:
                scores[objective][:, start:stop] = (directions @ prompt_gradients[objective].T).T.cpu()
        del jacobian, prompt_gradients
        for objective in OBJECTIVES:
            yield objective, layer, scores[objective]


def main() -> None:
    args = parse_args()
    if min(args.num_prompts, args.vocabulary_chunk_size, args.top_words,
           args.max_seq_len, args.progress_every) <= 0 or args.start_index < 0:
        raise ValueError("counts must be positive and start_index nonnegative")
    task_root = DEFAULT_RESULTS / args.task / "icl_10"
    input_path = args.input or task_root / "01_prepare/prompt_targets.jsonl.gz"
    association_path = args.associations or (
        task_root / f"02_associations/{args.target_mode}/manual_replacement/associations_static.jsonl.gz")
    output = args.output or (
        task_root / f"03_gradient/{args.target_mode}/{args.split}/gradient_rankings_"
        f"{args.position}_{args.start_index:06d}_{args.num_prompts:04d}.jsonl.gz")
    summary = args.summary_output or output.with_name(output.name.removesuffix(".jsonl.gz") + "_summary.json")
    for required in (input_path, association_path, args.lens):
        if not required.is_file():
            raise FileNotFoundError(required)
    temporary_output, temporary_summary = atomic_paths(output, summary, args.overwrite)

    association_index = load_associations(association_path, args.task, args.target_mode)
    records = select_gradient_records(
        read_jsonl(input_path), task=args.task, split=args.split, target_mode=args.target_mode,
        association_answers=set(association_index), start_index=args.start_index,
        num_prompts=args.num_prompts, context_variant=args.context_variant)
    if not records:
        raise ValueError("no prompts selected for this shard")
    jlens, model_class, tokenizer_class = imported_runtime()
    lens = load_lens(args.lens, jlens)
    tokenizer = tokenizer_class.from_pretrained(
        MODEL_ID, revision=MODEL_COMMIT, local_files_only=not args.allow_download)
    model = model_class.from_pretrained(
        MODEL_ID, revision=MODEL_COMMIT, dtype=torch.bfloat16, device_map="auto",
        local_files_only=not args.allow_download)
    model.eval()
    model.requires_grad_(False)

    # Share-among-answers denominator: first tokens of every target answer in the
    # task (all answers in the frozen association artifact), tokenized as answers.
    answer_first_ids = torch.tensor(sorted({
        answer_token_ids(tokenizer, records[0]["prompt"], answer)[0] for answer in association_index}))
    metadata, gradients = capture_prompt_gradients(
        model, tokenizer, records, answer_first_ids=answer_first_ids, position_policy=args.position,
        max_seq_len=args.max_seq_len, progress_every=args.progress_every)
    rankings = score_gradients(
        model, tokenizer, lens, records, association_index, gradients,
        chunk_size=args.vocabulary_chunk_size, top_words=args.top_words)
    try:
        with gzip.open(temporary_output, "wt", encoding="utf-8") as handle:
            for record, prompt_metadata, layer_rows in zip(records, metadata, rankings):
                handle.write(json.dumps({
                    "schema_version": 1,
                    "task": args.task,
                    "prompt_instance_id": record["prompt_instance_id"],
                    "query_index": record["query_index"],
                    "context_variant": record["context_variant"],
                    "split": args.split,
                    "x": record["x"],
                    "Fx": record["Fx"],
                    "true_answer": record["true_answer"],
                    "model_answer": record["model_answer_normalized"],
                    "model_answer_status": record["answer_status"],
                    "target_mode": args.target_mode,
                    "target_answer": record["gradient_target_answer"],
                    "association_status": association_index[record["gradient_target_answer"]].get(
                        "association_status", "available"),
                    "association_unavailable_reason": association_index[record["gradient_target_answer"]].get(
                        "association_unavailable_reason"),
                    "position_policy": args.position,
                    **prompt_metadata,
                    "layers": layer_rows,
                    "settings": {
                        "objectives": list(OBJECTIVES),
                        "direction": DIRECTION,
                        "source_layers": list(SOURCE_LAYERS),
                        "rank_rule": "1 + count(score > selected_score)",
                    },
                }, ensure_ascii=False) + "\n")
        summary_payload = {
            "schema_version": 1, "task": args.task, "target_mode": args.target_mode,
            "split": args.split, "position_policy": args.position,
            "start_index": args.start_index, "num_prompts": len(records),
            "context_variant": args.context_variant,
            "source_layers": list(SOURCE_LAYERS), "model": MODEL_ID,
            "model_commit": MODEL_COMMIT, "model_dtype": "bfloat16",
            "gradient_and_direction_dtype": "float32",
            "objectives": list(OBJECTIVES),
            "direction": DIRECTION,
            "num_answer_first_tokens": int(answer_first_ids.numel()),
            "input": str(input_path), "input_sha256": sha256(input_path),
            "associations": str(association_path), "associations_sha256": sha256(association_path),
            "lens": str(args.lens), "lens_sha256": sha256(args.lens),
            "output": str(output),
        }
        temporary_summary.write_text(json.dumps(summary_payload, indent=2) + "\n", encoding="utf-8")
        temporary_output.replace(output)
        temporary_summary.replace(summary)
    finally:
        temporary_output.unlink(missing_ok=True)
        temporary_summary.unlink(missing_ok=True)
    print(json.dumps({"output": str(output), "summary": str(summary), "num_prompts": len(records)}))


if __name__ == "__main__":
    main()
