#!/usr/bin/env python3
"""Boost word directions at layer 20 and measure the target answer.

At the final prompt token of layer 20:   h' = h + alpha * ||h|| * u

u is a J-Lens word direction  u_t = unit(J_20.T @ (gamma * W_U[t])), either one
word at a time ("single") or a whole word set at once ("set",
u = unit(sum_t u_t)). Each word set is run in three versions:

raw                 u_t as above;
centered            unit(u_t - m), m = mean of u_t over all word tokens. All lens
                    directions share a large common component; m removes it;
centered_corrected  centered, with the centered answer direction projected out.

(Projecting the answer out of raw directions is not used: because of the
shared component it leaves a "minus answer" term in every direction.)

Word sets per prompt: the manual K=5 list for the target answer, the prompt's
gradient top 5 (Stage 03b), three frequency-matched random 5-word sets, the
answer's own direction (positive control) and the intermediate's direction.

Measured per row: full-answer log probability, log share of the target first
token among the task's answer first tokens, and top-1 among those answers.
"""
from __future__ import annotations

import argparse
import copy
import gzip
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any

import torch

EXPERIMENT_DIR = Path(__file__).resolve().parent.parent
RESULTS = EXPERIMENT_DIR / "results"
sys.path.insert(0, str(EXPERIMENT_DIR))

_spec = importlib.util.spec_from_file_location("stage03", EXPERIMENT_DIR / "stages/03_gradient.py")
stage03 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(stage03)

from multipath.ablation import matched_random_tokens
from multipath.gradient import target_answer_for_record
from multipath.prepare import read_jsonl, sha256

LAYER = 20
ALPHAS = (-0.4, -0.2, -0.1, -0.05, 0.05, 0.1, 0.2, 0.4)
K = 5
RANDOM_DRAWS = 3
RANDOM_WINDOW = 2000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True)
    parser.add_argument("--target-mode", choices=("true", "model"), required=True)
    parser.add_argument("--context-variant", type=int, default=0)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--num-prompts", type=int)
    parser.add_argument("--count", action="store_true", help="print the number of eligible prompts and exit")
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--prefix-cache", action="store_true",
                        help="reuse the prompt's keys/values across rows (not faster in tests; "
                             "differs from the full recompute by bf16 rounding, up to ~0.08 log share)")
    parser.add_argument("--max-seq-len", type=int, default=512)
    parser.add_argument("--progress-every", type=int, default=25)
    parser.add_argument("--lens", type=Path, default=stage03.DEFAULT_LENS)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def eligible_prompts(args: argparse.Namespace) -> tuple[list[dict], dict, Path, Path]:
    """Test prompts of one context variant whose target has a manual K=5 list and a gradient top 5."""
    root = RESULTS / args.task / "icl_10"
    manual_path = root / f"02_associations/{args.target_mode}/manual_replacement/associations_static.jsonl.gz"
    gradient_path = (root / f"03_gradient/{args.target_mode}/test/context{args.context_variant}/"
                     "gradient_associations_L20_log_share.jsonl.gz")
    manual = {r["answer"]: r for r in read_jsonl(manual_path)}
    gradient = {r["prompt_instance_id"]: r for r in read_jsonl(gradient_path)}
    records = []
    for record in read_jsonl(root / "01_prepare/prompt_targets.jsonl.gz"):
        if record["split"] != "test" or record["context_variant"] != args.context_variant:
            continue
        target = target_answer_for_record(record, args.target_mode)
        row = manual.get(target)
        grad = gradient.get(record["prompt_instance_id"])
        if target is None or row is None or not row["association_subsets"][str(K)]["available"]:
            continue
        if grad is None or len(grad["top5"]) < K:
            continue
        records.append({**record, "target": target,
                        "manual_ids": [int(t) for t in row["association_subsets"][str(K)]["token_ids"]],
                        "gradient_ids": [int(x["token_id"]) for x in grad["top5"]]})
    return records, manual, manual_path, gradient_path


def unit(vectors: torch.Tensor) -> torch.Tensor:
    return vectors / vectors.norm(dim=-1, keepdim=True)


def remove(vectors: torch.Tensor, direction: torch.Tensor) -> torch.Tensor:
    """Project ``direction`` (unit) out of each row and renormalise."""
    return unit(vectors - (vectors @ direction)[:, None] * direction[None, :])


def main() -> None:
    args = parse_args()
    records, manual, manual_path, gradient_path = eligible_prompts(args)
    if args.count:
        print(len(records))
        return
    if not args.num_prompts:
        raise ValueError("--num-prompts is required")
    records = records[args.start_index:args.start_index + args.num_prompts]
    if len(records) != args.num_prompts:
        raise ValueError(f"requested {args.num_prompts} prompts at {args.start_index}, found {len(records)}")
    output = args.output or (RESULTS / args.task / f"icl_10/04_boost/{args.target_mode}/test/"
                             f"context{args.context_variant}/boost_{args.start_index:06d}.jsonl.gz")
    if output.exists() and not args.overwrite:
        raise FileExistsError(output)

    jlens, model_class, tokenizer_class = stage03.imported_runtime()
    lens = stage03.load_lens(args.lens, jlens)
    tokenizer = tokenizer_class.from_pretrained(stage03.MODEL_ID, revision=stage03.MODEL_COMMIT, local_files_only=True)
    model = model_class.from_pretrained(stage03.MODEL_ID, revision=stage03.MODEL_COMMIT, dtype=torch.bfloat16,
                                        device_map="auto", local_files_only=True)
    model.eval()
    model.requires_grad_(False)
    device = model.get_input_embeddings().weight.device
    jacobian = lens.jacobians[LAYER].to(device=device, dtype=torch.float32)
    readout = model.lm_head.weight
    gamma = model.model.norm.weight.float()

    def directions(ids: list[int]) -> torch.Tensor:
        return unit((readout[ids].float() * gamma[None, :]) @ jacobian)

    def centered(vectors: torch.Tensor) -> torch.Tensor:
        return unit(vectors - mean_direction[None, :])

    first = lambda prompt, text: stage03.answer_token_ids(tokenizer, prompt, text)[0]
    prompt0 = records[0]["prompt"]
    answer_first = sorted({first(prompt0, a) for a in manual})
    answer_first_t = torch.tensor(answer_first, device=device)
    intermediate_first = {first(prompt0, r["Fx"]) for r in records}
    word_mask = stage03.word_token_mask(tokenizer, int(readout.shape[0]))
    word_ids = torch.nonzero(word_mask).flatten().tolist()
    mean_direction = torch.zeros(jacobian.shape[0], device=device)
    for chunk_start in range(0, len(word_ids), 4096):
        mean_direction += directions(word_ids[chunk_start:chunk_start + 4096]).sum(dim=0)
    mean_direction /= len(word_ids)

    plan: list[tuple[int, torch.Tensor, float]] = []
    position = 0

    def boost(_module: Any, _inputs: Any, out: Any) -> Any:
        if not plan:
            return None
        hidden = (out[0] if isinstance(out, tuple) else out).clone()
        for row, direction, alpha in plan:
            state = hidden[row, position].float()
            hidden[row, position] = (state + alpha * state.norm() * direction).to(hidden.dtype)
        return (hidden, *out[1:]) if isinstance(out, tuple) else hidden

    handle_hook = model.model.layers[LAYER].register_forward_hook(boost)
    tmp = output.with_name(output.name + ".tmp")
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        with gzip.open(tmp, "wt", encoding="utf-8") as handle, torch.no_grad():
            for index, record in enumerate(records, start=1):
                prompt = record["prompt"]
                prompt_ids = tokenizer.encode(prompt, add_special_tokens=False)
                target_ids = stage03.answer_token_ids(tokenizer, prompt, record["target"])
                if len(prompt_ids) + len(target_ids) > args.max_seq_len:
                    raise ValueError(f"{record['prompt_instance_id']} exceeds max_seq_len")
                position = len(prompt_ids) - 1
                answer_id, inter_id = int(target_ids[0]), first(prompt, record["Fx"])
                sets = {"manual": record["manual_ids"], "gradient": record["gradient_ids"]}
                excluded = (set(record["manual_ids"]) | set(record["gradient_ids"]) | set(answer_first)
                            | intermediate_first | {inter_id})
                for draw in range(RANDOM_DRAWS):
                    sets[f"random_{draw}"] = matched_random_tokens(
                        record["manual_ids"], word_mask, excluded=excluded, window=RANDOM_WINDOW,
                        seed_key=f"{record['prompt_instance_id']}:{draw}")
                u_answer = directions([answer_id])[0]
                u_inter = directions([inter_id])[0]
                c_answer = centered(u_answer[None])[0]
                c_inter = centered(u_inter[None])[0]

                # (set, variant, kind, word index, direction)
                conditions: list[tuple[str, str, str, int | None, torch.Tensor]] = [
                    ("answer", "raw", "single", 0, u_answer),
                    ("answer", "centered", "single", 0, c_answer),
                    ("intermediate", "raw", "single", 0, u_inter),
                    ("intermediate", "centered", "single", 0, c_inter),
                    ("intermediate", "centered_corrected", "single", 0, remove(c_inter[None], c_answer)[0]),
                ]
                cosines = {}
                for name, ids in sets.items():
                    raw = directions(ids)
                    cosines[name] = (raw @ u_answer).tolist()
                    cen = centered(raw)
                    for variant, vectors in (("raw", raw), ("centered", cen),
                                             ("centered_corrected", remove(cen, c_answer))):
                        conditions += [(name, variant, "single", i, vectors[i]) for i in range(len(ids))]
                        conditions.append((name, variant, "set", None, unit(vectors.sum(dim=0))))
                rows = [(None, 0.0)] + [(c, alpha) for c in conditions for alpha in ALPHAS]

                target_t = torch.tensor(target_ids, device=device)
                if not args.prefix_cache:
                    input_ids = torch.tensor([prompt_ids + target_ids], device=device)
                else:
                    # Every row differs only from the final prompt token on, so run the
                    # tokens before it once and reuse their keys/values for all rows.
                    plan.clear()
                    prefix_cache = model(input_ids=torch.tensor([prompt_ids[:-1]], device=device),
                                         use_cache=True).past_key_values
                    input_ids = torch.tensor([prompt_ids[-1:] + target_ids], device=device)
                    position = 0
                metrics = []
                for start in range(0, len(rows), args.batch_size):
                    chunk = rows[start:start + args.batch_size]
                    plan[:] = [(r, c[4], alpha) for r, (c, alpha) in enumerate(chunk) if c is not None]
                    if not args.prefix_cache:
                        logits = model(input_ids=input_ids.expand(len(chunk), -1), use_cache=False,
                                       logits_to_keep=len(target_ids) + 1).logits
                    else:
                        cache = copy.deepcopy(prefix_cache)
                        cache.batch_repeat_interleave(len(chunk))
                        logits = model(input_ids=input_ids.expand(len(chunk), -1), past_key_values=cache,
                                       use_cache=True).logits
                    logits = logits[:, :len(target_ids)].float()
                    logp = logits.log_softmax(dim=-1)
                    full = logp.gather(2, target_t[None, :, None].expand(len(chunk), -1, -1)).sum(dim=(1, 2))
                    head = logp[:, 0]
                    share = head[:, answer_id] - head[:, answer_first_t].logsumexp(dim=-1)
                    top1 = answer_first_t[head[:, answer_first_t].argmax(dim=-1)] == answer_id
                    metrics += list(zip(full.tolist(), share.tolist(), top1.tolist()))
                plan.clear()
                base = metrics[0]
                results = [{"set": c[0], "variant": c[1], "kind": c[2], "word_index": c[3], "alpha": alpha,
                            "d_log_prob": m[0] - base[0], "d_log_share": m[1] - base[1], "top1": bool(m[2])}
                           for (c, alpha), m in zip(rows[1:], metrics[1:])]
                handle.write(json.dumps({
                    "schema_version": 1, "task": args.task, "target_mode": args.target_mode,
                    "prompt_instance_id": record["prompt_instance_id"], "x": record["x"], "Fx": record["Fx"],
                    "true_answer": record["true_answer"], "target_answer": record["target"],
                    "model_answer": record["model_answer_normalized"],
                    "baseline": {"log_prob": base[0], "log_share": base[1], "top1": bool(base[2])},
                    "sets": {n: {"token_ids": ids, "words": [tokenizer.decode([i]).strip() for i in ids],
                                 "cos_with_answer": cosines[n]} for n, ids in sets.items()},
                    "intermediate_token": {"token_id": inter_id, "word": tokenizer.decode([inter_id]).strip(),
                                           "cos_with_answer": float(u_inter @ u_answer),
                                           "centered_cos_with_answer": float(c_inter @ c_answer)},
                    "answer_cos_with_mean_direction": float(u_answer @ unit(mean_direction)),
                    "intermediate_equals_answer_first_token": inter_id == answer_id,
                    "results": results,
                }, ensure_ascii=False) + "\n")
                if index % args.progress_every == 0:
                    print(f"boosted: {index}/{len(records)}", flush=True)
        tmp.replace(output)
    finally:
        handle_hook.remove()
        tmp.unlink(missing_ok=True)
    output.with_name(output.name.removesuffix(".jsonl.gz") + "_summary.json").write_text(json.dumps({
        "task": args.task, "target_mode": args.target_mode, "split": "test",
        "context_variant": args.context_variant, "start_index": args.start_index, "num_prompts": len(records),
        "layer": LAYER, "position": "final_prompt", "alphas": list(ALPHAS), "k": K,
        "push": "h + alpha * ||h|| * u; set u = unit(sum of word directions)",
        "direction": stage03.DIRECTION,
        "variants": {"raw": "u_t", "centered": "unit(u_t - mean word direction)",
                     "centered_corrected": "centered, centered answer direction projected out"},
        "random": {"draws": RANDOM_DRAWS, "window": RANDOM_WINDOW, "matched_to": "manual words"},
        "num_answer_first_tokens": len(answer_first),
        "manual_sha256": sha256(manual_path), "gradient_sha256": sha256(gradient_path),
        "lens_sha256": sha256(args.lens), "model": stage03.MODEL_ID, "model_commit": stage03.MODEL_COMMIT,
    }, indent=2) + "\n")
    print(json.dumps({"output": str(output), "num_prompts": len(records)}))


if __name__ == "__main__":
    main()
