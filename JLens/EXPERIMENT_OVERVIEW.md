# OLMo 3 J-Lens Experiment: End-to-End Process

The experiment has two distinct phases: fitting a general J-Lens and applying
that fitted lens to the landmark-country-capital task.

## A. Fit the J-Lens

### 1. Source data

Start with 10,000 sampled OLMo 3 stage-one windows. Each window contains 512
token IDs.

### 2. Build the fitting manifest

`build_fit_manifest.py` and `manifest.py`:

- Select 1,000 windows reproducibly using random seed 0.
- Take the first 128 token IDs from each selected window.
- Decode those token IDs into text.
- Save the text, original token IDs, and source metadata in
  `results/fit_1000/prompt_manifest.jsonl`.

The official J-Lens API accepts text and tokenizes it internally. Therefore,
the text is retokenized during fitting. For 16 of our 1,000 prompts, this
retokenization does not reproduce the original 128 token IDs exactly. This is
consistent with the paper's text-prompt interface, but those 16 inputs should
not be described as the exact original 128-token OLMo windows.

### 3. Check OLMo compatibility

`compatibility.py` verifies that the official J-Lens Hugging Face adapter:

- recognizes OLMo 3's 32 layers and 4,096-dimensional residual stream; and
- reproduces the model's ordinary output logits through its final
  normalization and unembedding path.

This is a smoke test. It does not fit a lens.

### 4. Fit ten shards

`fit_jlens.py` divides the fixed 1,000-prompt manifest into ten non-overlapping
groups of 100 prompts. Each shard loads the pinned OLMo 3 stage-one checkpoint,
wraps it using the authors' official adapter, and calls the authors'
`jlens.fit` implementation.

For each selected source layer, J-Lens estimates

\[
J_\ell =
\mathbb{E}_{t,\,t'\geq t,\,\text{prompt}}
\left[
\frac{\partial h_{\mathrm{final},t'}}
     {\partial h_{\ell,t}}
\right].
\]

The average is over fitting prompts, source token positions \(t\), and later
target positions \(t'\). We fit source layers 12, 16, 18, 20, 22, and 24
against final layer 31.

### 5. Merge the shards

`merge_lenses.py` verifies that the ten shards cover the manifest exactly once
and share the same model and fitting settings. It then uses the authors'
`JacobianLens.merge` operation to compute a prompt-count-weighted average.

The result is one fitted \(4096\times4096\) Jacobian matrix for each of the six
source layers.

## B. Apply the J-Lens to the task

### 6. Load task queries

`evaluate_landmarks.py` loads the saved correctly answered landmark queries
that the earlier logit-lens analysis classified as:

- 370 compositional queries; and
- 105 shortcut candidates.

The 1,000 generic prompts used to fit J-Lens are separate from these task
prompts. The generic prompts estimate the lens; the task prompts evaluate it.

### 7. Run each complete task prompt

OLMo processes the original prompt containing ten in-context examples and the
final landmark query. The evaluation examines activation vectors at the token
positions belonging to that final query.

### 8. Apply J-Lens

For activation \(h_{\ell,t}\) at fitted layer \(\ell\) and query position
\(t\), the readout is computed as

\[
h_{\ell,t}
\longrightarrow J_\ell h_{\ell,t}
\longrightarrow \text{final normalization}
\longrightarrow \text{unembedding logits}.
\]

This produces a score for every vocabulary token.

### 9. Measure country evidence

The primary backward-compatible measurement ranks the first token of the
correct intermediate country in the full model vocabulary. The code also
records diagnostics for:

- every separate token in a multi-token country name; and
- the complete country label, ranked against the country labels in the
  evaluated dataset.

These are readout measurements, not causal interventions.

### 10. Save the results

- `per_query.jsonl` contains layerwise evidence for every query.
- `summary.json` contains aggregate compositional, ambiguous, and
  shortcut-candidate counts.
