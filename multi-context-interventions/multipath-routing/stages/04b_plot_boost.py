#!/usr/bin/env python3
"""Plot Stage-04 boosting results (true answers, whole word set, centred directions).

Figures (written to results/figures/):
  boost_dose_response.png   mean change in log share vs alpha, per task
  boost_prompts_rising.png  % of prompts whose answer probability rises vs alpha
  boost_wrong_fixed.png     % of wrong-at-baseline prompts that become correct vs alpha
"""
from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

EXPERIMENT_DIR = Path(__file__).resolve().parent.parent
RESULTS = EXPERIMENT_DIR / "results"
TASKS = {"landmark-country-capital": "Landmark → country → capital",
         "park-country-capital": "Park → country → capital",
         "product-company-ceo": "Product → company → CEO"}
ALPHAS = (-0.4, -0.2, -0.1, -0.05, 0.05, 0.1, 0.2, 0.4)

# Validated categorical slots 1-4 (light mode); random is a neutral reference, not a series hue.
SERIES = [  # key, label, color
    ("manual", "Manual associations", "#2a78d6"),
    ("gradient", "Gradient associations", "#eb6834"),
    ("intermediate", "Intermediate (country / company)", "#1baf7a"),
    ("answer", "Answer itself (ceiling)", "#eda100"),
    ("random", "Random words (control)", "#8a8984"),
]
SURFACE, TEXT, TEXT2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"


def load(task: str, mode: str, variant: str) -> dict:
    files = sorted((RESULTS / task / f"icl_10/04_boost/{mode}/test/context0").glob("boost_0*.jsonl.gz"))
    records = [json.loads(line) for f in files for line in gzip.open(f, "rt")]
    out = {"n": len(records), "wrong": np.array([not r["baseline"]["top1"] for r in records])}
    for key, *_ in SERIES:
        sets = [f"random_{i}" for i in range(3)] if key == "random" else [key]
        kind, var = ("single", "centered") if key in ("answer", "intermediate") else ("set", variant)
        share, logp, top1 = (np.zeros((len(records), len(ALPHAS))) for _ in range(3))
        for i, r in enumerate(records):
            index = {(x["set"], x["alpha"]): x for x in r["results"] if x["kind"] == kind and x["variant"] == var}
            for j, a in enumerate(ALPHAS):
                xs = [index[(s, a)] for s in sets]
                share[i, j] = np.mean([x["d_log_share"] for x in xs])
                logp[i, j] = np.mean([x["d_log_prob"] for x in xs])
                top1[i, j] = np.mean([x["top1"] for x in xs])
        out[key] = {"share": share, "logp": logp, "top1": top1}
    return out


def style(ax, title: str) -> None:
    ax.set_facecolor(SURFACE)
    ax.set_title(title, color=TEXT, fontsize=11, loc="left")
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=TEXT2, labelsize=9)
    ax.set_xticks([-0.4, -0.2, 0, 0.2, 0.4])


def label_ends(ax, items: list[tuple[str, float, str]]) -> None:
    """Direct labels at the right end, nudged apart so they do not overlap."""
    lo, hi = ax.get_ylim()
    gap = (hi - lo) * 0.055
    placed = []
    for text, y, color in sorted(items, key=lambda t: t[1]):
        y = max(y, placed[-1] + gap) if placed else y
        placed.append(y)
        ax.annotate(text, (ALPHAS[-1], y), xytext=(6, 0), textcoords="offset points",
                    va="center", fontsize=8, color=TEXT2)
        ax.plot([ALPHAS[-1] + 0.012], [y], marker="o", markersize=4, color=color, clip_on=False)


VERSION = {"raw": "raw word directions", "centered": "centred word directions",
           "centered_corrected": "centred word directions, answer direction removed"}


def figure(data: dict, metric: str, ylabel: str, title: str, path: Path, keys: list[str],
           subset: str | None = None, alphas: tuple = ALPHAS, ref: float | None = 0.0,
           version: str = "") -> None:
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), facecolor=SURFACE)
    idx = [ALPHAS.index(a) for a in alphas]
    for ax, (task, name) in zip(axes, TASKS.items()):
        d = data[task]
        rows = d["wrong"] if subset == "wrong" else np.ones(d["n"], bool)
        style(ax, f"{name}  (n = {int(rows.sum())})")
        if ref is not None:
            ax.axhline(ref, color=TEXT2, linewidth=0.8, linestyle=(0, (2, 2)))
        ends = []
        for key, label, color in SERIES:
            if key not in keys:
                continue
            values = d[key][metric][rows][:, idx]
            if metric == "rises":
                values = values  # already fractions
            mean = values.mean(axis=0) * (100 if metric != "share" else 1)
            se = values.std(axis=0, ddof=1) / np.sqrt(len(values)) * (100 if metric != "share" else 1)
            dashed = key == "random"
            ax.fill_between(alphas, mean - 1.96 * se, mean + 1.96 * se, color=color, alpha=0.15, linewidth=0)
            ax.plot(alphas, mean, color=color, linewidth=2, linestyle="--" if dashed else "-",
                    marker="o", markersize=5, markeredgecolor=SURFACE, markeredgewidth=1.5, label=label)
            ends.append((label.split(" (")[0], mean[-1], color))
        ax.set_xlim(alphas[0] - 0.02, alphas[-1] + 0.02)
        ax.set_xlabel("boost strength α  (push = α·‖h‖, layer 20)", color=TEXT2, fontsize=9)
        label_ends(ax, ends)
    axes[0].set_ylabel(ylabel, color=TEXT2, fontsize=9)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=len(labels), frameon=False, fontsize=9,
               bbox_to_anchor=(0.5, 1.0), labelcolor=TEXT2)
    fig.suptitle(title, x=0.01, y=1.13, ha="left", fontsize=13, color=TEXT)
    fig.text(0.01, 1.055, version, ha="left", fontsize=10, color=TEXT2)
    fig.tight_layout(rect=(0, 0, 0.93, 0.93))
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    print(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", default="true", choices=("true", "model"))
    parser.add_argument("--variant", default="centered", choices=("raw", "centered", "centered_corrected"))
    args = parser.parse_args()
    data = {task: load(task, args.mode, args.variant) for task in TASKS}
    for d in data.values():  # fraction of prompts whose full-answer log probability rises
        for key, *_ in SERIES:
            d[key]["rises"] = (d[key]["logp"] > 0).astype(float)
    out = RESULTS / "figures"
    out.mkdir(parents=True, exist_ok=True)
    suffix = "" if (args.mode, args.variant) == ("true", "centered") else f"_{args.mode}_{args.variant}"
    all_keys = [k for k, *_ in SERIES]
    version = (f"{'True' if args.mode == 'true' else 'Model'} answers · whole 5-word set · "
               f"{VERSION[args.variant]} · mean with 95% CI")
    figure(data, "share", "change in log share of the answer",
           "Effect of boosting word directions on the answer",
           out / f"boost_dose_response{suffix}.png", all_keys, version=version)
    figure(data, "rises", "% of prompts where P(answer) rises",
           "Share of prompts where boosting raises the answer's probability",
           out / f"boost_prompts_rising{suffix}.png", ["manual", "gradient", "random"], ref=50.0,
           version=version)
    figure(data, "top1", "% of wrong prompts now answered correctly",
           "Wrong answers fixed by boosting (prompts the model got wrong at baseline)",
           out / f"boost_wrong_fixed{suffix}.png", ["manual", "gradient", "answer", "random"],
           subset="wrong", alphas=(0.05, 0.1, 0.2, 0.4), ref=None, version=version)


if __name__ == "__main__":
    main()
