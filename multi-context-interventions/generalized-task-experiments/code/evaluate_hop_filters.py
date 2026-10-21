"""Produce composition-only and all-hops-correct populations separately.

Input: saved baseline JSONL plus the pinned task dataset (for Gx values that
older manifests omitted). Only composition-correct instances need new model
calls. For each, reuse the exact demonstration rows in their original order,
but render each required hop independently. Full greedy answers are compared
exactly, with task-aware numeric spacing.

Output under --output-root:
  composition_correct/correct_instances.jsonl.gz
  all_hops_and_composition_correct/correct_instances.jsonl.gz
  hop_evaluation.jsonl.gz (all tested hops, including failures)
  filtering_summary.json

The population files preserve original baseline rows for downstream lens use.
This evaluates behavioral hops only; it does not add Gx lens measurements.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping

from evaluate_baseline import (
    MODEL_ID, MODEL_DTYPE, STAGE_ONE_COMMIT, MAX_NEW_TOKENS, STOP_SEQUENCE,
    ensure_outputs, open_text, read_jsonl,
)
from tasks import DATASET_ID, DATASET_COMMIT, TASKS, get_task_spec


ALTERNATIVE_ROUTE_TASKS = frozenset({
    "antonym-french", "antonym-german", "antonym-spanish",
    "plus-ten-times-two", "plus-hundred-times-two", "mod-twenty-times-two",
    "word-int-times-two", "rgb-rot120-name", "word-substring-reverse",
})
NUMERIC_GX_TASKS = frozenset({
    "plus-ten-times-two", "plus-hundred-times-two", "mod-twenty-times-two",
})
PROJECT_DIR = Path(__file__).resolve().parent.parent


def required_hops(task: str) -> tuple[tuple[str, str], ...]:
    """Return both hops on every route recognized by the original paper."""
    get_task_spec(task)
    hops = (("x", "Fx"), ("Fx", "GFx"))
    if task in ALTERNATIVE_ROUTE_TASKS:
        hops += (("x", "Gx"), ("Gx", "GFx"))
    return hops


def dataset_index(rows: Iterable[Mapping[str, Any]], task: str) -> dict[str, dict]:
    """Index original task rows by x; require every needed intermediate."""
    nodes = {n for hop in required_hops(task) for n in hop}
    index = {}
    for row in rows:
        if row.get("task") != task:
            continue
        if any(not isinstance(row.get(n), str) or not row[n] for n in nodes):
            raise ValueError(f"dataset row lacks required nodes {sorted(nodes)}")
        if row["x"] in index:
            raise ValueError(f"duplicate dataset x: {row['x']!r}")
        index[row["x"]] = dict(row)
    if not index:
        raise ValueError(f"no dataset rows for {task}")
    return index


def enrich(row: Mapping[str, str], index: Mapping[str, dict]) -> dict:
    """Recover Gx by exact identity, rejecting dataset/baseline mismatches."""
    original = index[row["x"]]
    for node in ("x", "Fx", "GFx", "Gx"):
        if node in row and row[node] != original.get(node):
            raise ValueError(f"dataset mismatch for {row['x']!r}, {node}")
    return original


def hop_prompt(record: Mapping[str, Any], index: Mapping[str, dict],
               task: str, source: str, target: str) -> tuple[str, str]:
    """Reformat the saved context for one hop; return prompt and exact label."""
    if (source, target) not in required_hops(task):
        raise ValueError("not a required hop")
    query = enrich(record["query"], index)
    context = [enrich(row, index) for row in record["context"]]
    spec = get_task_spec(task)
    numeric = (task in NUMERIC_GX_TASKS if target == "Gx"
               else target in spec.numeric_nodes)
    prompt = "".join(f"Q: {row[source]}\nA: {row[target]}\n\n" for row in context)
    prompt += f"Q: {query[source]}\nA:" + (" " if numeric else "")
    label = ("" if numeric else " ") + query[target]
    return prompt, label


def write_populations(*, records: Iterable[dict], task: str,
                      index: Mapping[str, dict], predict: Callable[[str], str],
                      output_root: Path, provenance: dict,
                      overwrite: bool = False) -> dict:
    """Evaluate hops and atomically install population files after success.

    predict takes one prompt and returns its complete continuation before the
    stop sequence. Missing tests never count as correct. Composition accuracy
    comes from the saved baseline, while hops are fresh single-prompt runs.
    """
    paths = [
        output_root / "composition_correct/correct_instances.jsonl.gz",
        output_root / "all_hops_and_composition_correct/correct_instances.jsonl.gz",
        output_root / "hop_evaluation.jsonl.gz",
        output_root / "filtering_summary.json",
    ]
    ensure_outputs(paths, overwrite)
    temporary = [p.with_name(p.stem + ".tmp" + p.suffix) for p in paths]
    counts = dict(input_instances=0, composition_correct=0,
                  all_hops_and_composition_correct=0)
    seen = set()
    strict_queries, composition_queries = set(), set()
    hops = required_hops(task)
    hop_counts = {f"{a}->{b}": 0 for a, b in hops}
    try:
        with open_text(temporary[0], "wt") as broad, open_text(temporary[1], "wt") as strict, open_text(temporary[2], "wt") as audit:
            for record in records:
                pid = record.get("prompt_instance_id")
                if not isinstance(pid, str) or not pid or pid in seen:
                    raise ValueError(f"missing or duplicate prompt_instance_id: {pid!r}")
                seen.add(pid)
                if record.get("task") != task:
                    raise ValueError("baseline task mismatch")
                spec = get_task_spec(task)
                spec.validate_prompt(record["prompt"], record["query"]["x"])
                correct = record["evaluation"]["exact_match"]
                if not isinstance(correct, bool):
                    raise ValueError("baseline exact_match must be boolean")
                counts["input_instances"] += 1
                if not correct:
                    continue
                enrich(record["query"], index)
                line = json.dumps(record, ensure_ascii=False) + "\n"
                broad.write(line)
                counts["composition_correct"] += 1
                composition_queries.add(record["query"]["x"])
                results = []
                for source, target in hops:
                    prompt, label = hop_prompt(record, index, task, source, target)
                    prediction = predict(prompt)
                    if not isinstance(prediction, str):
                        raise TypeError("predict must return a string")
                    exact = prediction == label
                    hop_counts[f"{source}->{target}"] += int(exact)
                    results.append(dict(source=source, target=target, prompt=prompt,
                                        prediction=prediction, label=label, exact_match=exact))
                passed = all(r["exact_match"] for r in results)
                audit.write(json.dumps(dict(prompt_instance_id=pid, task=task,
                    query=enrich(record["query"], index), hops=results,
                    all_hops_correct=passed), ensure_ascii=False) + "\n")
                if passed:
                    strict.write(line)
                    counts["all_hops_and_composition_correct"] += 1
                    strict_queries.add(record["query"]["x"])
                if counts["composition_correct"] % 10 == 0:
                    print(f"Checked hops for {counts['composition_correct']} instances", flush=True)
        summary = dict(task=task, **counts, required_hops=hops,
            hop_correct_counts=hop_counts,
            composition_correct_unique_queries=len(composition_queries),
            all_hops_correct_unique_queries=len(strict_queries),
            context_policy="same_saved_demonstration_rows_and_order_for_each_hop",
            composition_correctness="saved_baseline_exact_match",
            hop_correctness="fresh_single_prompt_greedy_full_answer_exact_match",
            provenance=provenance, outputs=[str(p) for p in paths[:3]])
        temporary[3].write_text(json.dumps(summary, indent=2) + "\n")
        for temp, path in zip(temporary, paths):
            temp.replace(path)
        return summary
    finally:
        for temp in temporary:
            temp.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, choices=sorted(TASKS))
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--dataset-jsonl", type=Path, help="Optional local copy of pinned dataset")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    root = PROJECT_DIR / "results" / args.task
    input_path = args.input or root / "baseline_evaluation.jsonl.gz"
    if args.dataset_jsonl:
        rows = read_jsonl(args.dataset_jsonl)
    else:
        from datasets import load_dataset
        rows = load_dataset(DATASET_ID, revision=DATASET_COMMIT, split="train")
    index = dataset_index(rows, args.task)

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=STAGE_ONE_COMMIT, local_files_only=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, revision=STAGE_ONE_COMMIT,
        dtype=torch.bfloat16, device_map="auto", local_files_only=True)
    model.eval()

    def predict(prompt: str) -> str:
        inputs = tokenizer([prompt], return_tensors="pt", return_token_type_ids=False)
        inputs = {k: v.to(model.get_input_embeddings().weight.device) for k, v in inputs.items()}
        with torch.inference_mode():
            output = model.generate(**inputs, tokenizer=tokenizer, do_sample=False,
                max_new_tokens=MAX_NEW_TOKENS, stop_strings=STOP_SEQUENCE,
                pad_token_id=tokenizer.pad_token_id)
        return tokenizer.decode(output[0, inputs["input_ids"].shape[1]:],
                                skip_special_tokens=True).split(STOP_SEQUENCE, 1)[0]

    digest = hashlib.sha256()
    with input_path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    summary = write_populations(records=read_jsonl(input_path), task=args.task,
        index=index, predict=predict, output_root=args.output_root or root,
        overwrite=args.overwrite, provenance=dict(input=str(input_path),
            input_sha256=digest.hexdigest(), model=MODEL_ID, model_commit=STAGE_ONE_COMMIT,
            dtype=MODEL_DTYPE, max_new_tokens=MAX_NEW_TOKENS, stop_sequence=STOP_SEQUENCE,
            dataset=DATASET_ID, dataset_commit=DATASET_COMMIT,
            dataset_jsonl=str(args.dataset_jsonl) if args.dataset_jsonl else None))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
