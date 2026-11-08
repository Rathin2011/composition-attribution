#!/usr/bin/env python3
"""Turn Stage-03 gradient rankings into top-5 and top-10 association lists.

For each prompt, take the saved top word tokens at one layer/objective
(default: layer 20, log share), drop words that are not associations, and keep
the first 5 and 10 survivors in rank order. Dropped (case-insensitive):

answer       the target answer, its aliases, and pieces/extensions of their
             words (London, london, Lond, Londoners);
intermediate the prompt's own intermediate, its aliases and adjectives, and
             pieces/extensions of them (Britain, UK, British, Brit);
other_name   any word of any other task intermediate or task answer
             (other countries/companies, other capitals/CEOs);
duplicate    a variant of a word already kept (Korea after Korean);
non_english  a lowercase word not in the English word list (selber, partager),
             any word shorter than 3 characters, with non-ASCII letters (Método),
             or with internal capitals (QStringList; all-caps like NHS is kept).
             Other capitalised names are kept.

Writes one per-prompt file per task/mode and one readable Markdown file.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gzip
import json
from pathlib import Path
import re
import sys

EXPERIMENT_DIR = Path(__file__).resolve().parent.parent
RESULTS = EXPERIMENT_DIR / "results"
sys.path.insert(0, str(EXPERIMENT_DIR))
from multipath.prepare import read_jsonl

TASKS = ("landmark-country-capital", "park-country-capital", "product-company-ceo")
TITLES = {"landmark-country-capital": "Landmark → country → capital",
          "park-country-capital": "Park → country → capital",
          "product-company-ceo": "Product → company → CEO"}
ENGLISH = {w.strip().casefold() for w in open("/usr/share/dict/words", encoding="utf-8", errors="ignore")}
SPLIT = re.compile(r"[\s\-.,'’()]+")


def words(text: str) -> list[str]:
    return [w for w in SPLIT.split(text.casefold()) if w]


def is_piece(word: str, term: str) -> bool:
    """Same word, a prefix of it (>=3 chars), or an extension of it (term >=4 chars)."""
    return word == term or (len(word) >= 3 and term.startswith(word)) or (
        len(term) >= 4 and word.startswith(term))


def is_variant(word: str, kept: list[str]) -> bool:
    return any(word == k or (min(len(word), len(k)) >= 4 and (word.startswith(k) or k.startswith(word)))
               or (min(len(word), len(k)) >= 5 and word[:5] == k[:5]) for k in kept)


def answer_terms(answer: str, aliases: dict[str, list[str]]) -> set[str]:
    names = {answer}
    for canonical, alts in aliases.items():
        if answer == canonical or answer in alts:
            names |= {canonical, *alts}
    return {w for name in names for w in words(name)}


def classify(word: str, *, own_answer: set[str], own_intermediate: set[str], other_names: set[str]) -> str | None:
    w = word.casefold()
    if any(is_piece(w, t) for t in own_answer):
        return "answer"
    if any(is_piece(w, t) for t in own_intermediate):
        return "intermediate"
    if w in other_names:
        return "other_name"
    if (len(word) < 3 or not word.isascii() or (word[0].islower() and w not in ENGLISH)
            or (not word.isupper() and any(c.isupper() for c in word[1:]))):
        return "non_english"
    return None


def build(task: str, mode: str, layer: int, objective: str, answer_aliases: dict, inter_aliases: dict):
    root = RESULTS / task / "icl_10"
    shards = sorted((root / f"03_gradient/{mode}/test/context0").glob("gradient_rankings_*.jsonl.gz"))
    if not shards:
        raise FileNotFoundError(f"no Stage-03 shards for {task}/{mode}")
    prompts = list(read_jsonl(root / "01_prepare/prompt_targets.jsonl.gz"))
    intermediates = {r["Fx"] for r in prompts}
    answers = {r["true_answer"] for r in prompts}
    answers |= {json.loads(l)["answer"] for l in gzip.open(
        root / f"02_associations/{mode}/manual_replacement/associations_static.jsonl.gz", "rt")}
    aliases = answer_aliases["tasks"].get(task, {}).get("aliases", {})

    def inter_terms(name: str) -> set[str]:
        return {w for n in [name, *inter_aliases.get(name, [])] for w in words(n)}

    if task != "product-company-ceo":
        intermediates |= set(inter_aliases)  # every country, not only this task's
    all_inter_words = {w for name in intermediates for w in inter_terms(name)}
    all_answer_words = {w for a in answers for w in words(a)}
    rows = []
    for shard in shards:
        for record in read_jsonl(shard):
            entry = next(x for x in record["layers"] if x["layer"] == layer and x["objective"] == objective)
            own_answer = answer_terms(record["target_answer"], aliases)
            own_inter = inter_terms(record["Fx"])
            others = (all_inter_words | all_answer_words) - own_answer - own_inter
            kept, dropped = [], []
            for item in entry["top_word_tokens"]:
                word = item["word"]
                reason = classify(word, own_answer=own_answer, own_intermediate=own_inter, other_names=others)
                if reason is None and is_variant(word.casefold(), [k["word"].casefold() for k in kept]):
                    reason = "duplicate"
                if reason:
                    dropped.append({"word": word, "reason": reason})
                else:
                    kept.append({"word": word, "token_id": item["token_id"], "score": item["directional_score"],
                                 "word_vocabulary_rank": item["word_vocabulary_rank"]})
            rows.append({"task": task, "target_mode": mode, "prompt_instance_id": record["prompt_instance_id"],
                         "x": record["x"], "Fx": record["Fx"], "target_answer": record["target_answer"],
                         "layer": layer, "objective": objective, "num_ranked_words_scanned": len(entry["top_word_tokens"]),
                         "top5": kept[:5], "top10": kept[:10], "num_kept": len(kept), "dropped": dropped})
    return rows


def per_answer(rows: list[dict], k: int) -> dict[str, tuple[int, list[tuple[str, int]]]]:
    """Words most often in an answer's per-prompt top-k (ties broken by mean rank)."""
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row["target_answer"]].append(row)
    out = {}
    for answer, group in grouped.items():
        counts, ranks = Counter(), defaultdict(list)
        for row in group:
            for position, item in enumerate(row[f"top{k}"]):
                counts[item["word"]] += 1
                ranks[item["word"]].append(position)
        order = sorted(counts, key=lambda w: (-counts[w], sum(ranks[w]) / len(ranks[w])))
        out[answer] = (len(group), [(w, counts[w]) for w in order[:k]])
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--layer", type=int, default=20)
    parser.add_argument("--objective", default="log_share", choices=("log_share", "log_prob"))
    parser.add_argument("--modes", nargs="+", default=["true", "model"])
    args = parser.parse_args()
    answer_aliases = json.loads((EXPERIMENT_DIR / "configs/answer_aliases.json").read_text())
    inter_aliases = json.loads((EXPERIMENT_DIR / "configs/intermediate_aliases.json").read_text())["aliases"]
    md = ["# Gradient-based associated words", "",
          f"Per prompt: the top word tokens by gradient score (layer {args.layer}, {args.objective}), after",
          "dropping the answer and its pieces, the intermediate and its adjectives, other answers' and",
          "intermediates' names, and near-duplicates. Below, per answer: the words that most often appear",
          "in the per-prompt top 5 / top 10, with the number of prompts in brackets when an answer has",
          "more than one prompt.", ""]
    stats = {}
    for task in TASKS:
        md.append(f"## {TITLES[task]}")
        for mode in args.modes:
            rows = build(task, mode, args.layer, args.objective, answer_aliases, inter_aliases)
            out = RESULTS / task / f"icl_10/03_gradient/{mode}/test/context0/gradient_associations_L{args.layer}_{args.objective}.jsonl.gz"
            with gzip.open(out, "wt", encoding="utf-8") as handle:
                for row in rows:
                    handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            stats[f"{task}/{mode}"] = {
                "prompts": len(rows), "with_5": sum(r["num_kept"] >= 5 for r in rows),
                "with_10": sum(r["num_kept"] >= 10 for r in rows),
                "dropped": dict(Counter(d["reason"] for r in rows for d in r["dropped"])), "output": str(out)}
            label = "True answers" if mode == "true" else "Model answers"
            top5, top10 = per_answer(rows, 5), per_answer(rows, 10)
            md += ["", f"### {label} ({len(top5)} answers, {len(rows)} prompts)", "",
                   "| Answer | Top 5 | Top 10 |", "|---|---|---|"]
            fmt = lambda items, n: ", ".join(w if n == 1 else f"{w} ({c})" for w, c in items)
            for answer in sorted(top5, key=str.casefold):
                n = top5[answer][0]
                name = answer if n == 1 else f"{answer} ({n} prompts)"
                md.append(f"| {name} | {fmt(top5[answer][1], n)} | {fmt(top10[answer][1], n)} |")
        md.append("")
    target = RESULTS / "gradient_associations" / f"gradient_lists_L{args.layer}_{args.objective}.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(md) + "\n", encoding="utf-8")
    (target.with_suffix(".summary.json")).write_text(json.dumps(stats, indent=2) + "\n")
    print(json.dumps(stats, indent=2))
    print(target)


if __name__ == "__main__":
    main()
