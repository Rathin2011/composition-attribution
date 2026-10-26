# Lens experiment exports

This directory contains one compressed `experiment_results.json` export for
each of the 18 Khandelwal–Pavlick tasks evaluated with OLMo 3 7B Stage 1.

Each archive expands to a JSON object with:

- `x`: the task's possible query values;
- `Fx`: the possible intermediate values;
- `GFx`: the possible composed-answer values;
- `results_lenses`: per-prompt Logit-Lens and J-Lens logits, reciprocal ranks,
  and classifications; and
- `results_intervention`: currently an empty list.

The Logit-Lens matrices contain 32 layer columns. The J-Lens matrices contain
the six fitted layers: 12, 16, 18, 20, 22, and 24.

To inspect an archive without creating the uncompressed multi-gigabyte file:

```bash
gzip -dc antonym-french.experiment_results.json.gz | less
```

The archives are tracked with Git LFS. A clone therefore needs Git LFS to
download their contents:

```bash
git lfs install
git lfs pull
```
