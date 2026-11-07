# Multi-path routing experiments

This directory is intentionally separate from the existing generalized lens
and intervention pipeline.  Work proceeds one stage at a time.

## Stage 01: prepare

Stage 01 reuses the existing ten-context generalized prompts and baseline
predictions.  It validates the source join and exact-match labels, then assigns
whole query entities to a 30% selection / 70% test split with seed 0.

Geographic and product tasks are stratified by the ground-truth
`(Fx, GFx)` pair.  Groups of at least two query entities receive at least one
entity on each side; singleton groups are seeded-randomly assigned and flagged.
Antonym-Spanish uses a plain entity-level random split.  All ten contexts for a
query remain together.

Run one task with:

```bash
/projectnb/buinlp/rathin/influence-composition/.venv/bin/python \
  multipath-routing/stages/01_prepare.py --task landmark-country-capital
```

The command performs no model inference.  It writes atomically to:

```text
multipath-routing/results/<task>/icl_10/01_prepare/
  prompt_targets.jsonl.gz
  entities.json
  summary.json
```

Association discovery, gradient scoring, and interventions are not part of
this stage.

## Stage 02: associations

Stage 02 uses manually reviewed association lists rather than asking OLMo to
generate them. The validator keeps only exact single-token words, removes the
answer and its pieces, and removes **every intermediate in the task** (not
merely the target's own intermediate). The landmark true-answer catalog covers
all 87 answers. Strict tokenizer validation and a 10% cross-answer frequency
filter retain 5–19 answer-specific words per answer. Every answer therefore
supports the planned K=5 primary analysis without generic padding. Generic
capital/government words and ambiguous pieces of multi-word names are recorded
separately rather than included as associations.

The frozen artifact stores nested K=3, K=5, and K=10 subsets. K=5 is the
primary analysis. Within each answer, words are ordered by increasing
cross-answer document frequency (more answer-specific first), with the curated
catalog order as the deterministic tie-breaker. K=3 and K=5 are available for
all 87 landmark answers; K=10 is a sensitivity analysis only for answers with
at least ten surviving words. No answer is padded with generic words.

The park catalog reuses the 70 capital lists shared with landmark and adds 41
park-only capitals. All 111 park answers support K=3 and K=5; 32 support K=10.
Inheritance is resolved before validation, while inherited answers absent from
the child task are recorded but not treated as child-task coverage errors.

Stage 02 is **not complete** across all five tasks and both target modes.
The previous completion claim counted OLMo-prompted catalogs, but that provider
was not approved for this experiment. All `prompted/` artifacts and their raw
cue scores are rejected as experiment inputs. They remain on disk for audit.
Stage 03 rejects association rows produced using model inference. The Stage-02
`score-cues` and `build-prompted` commands are disabled, so the older GPU job
scripts cannot recreate those catalogs.

`configs/manual_association_additions.json` contains additional words written
directly by Codex for review. `stages/02_manual_catalogs.py` combines those lists
with the existing static landmark/park lists, reusing a list only for an exact
answer match of the same answer type. It applies the existing real-tokenizer,
answer-piece, intermediate and generic-word checks without loading model weights.
These checks verify format and exclusions, not semantic specificity.

Run the tokenizer-only replacement with:

```bash
/projectnb/buinlp/rathin/influence-composition/.venv/bin/python \
  multipath-routing/stages/02_manual_catalogs.py
```

New outputs are under `02_associations/<mode>/manual_replacement/`. The aggregate
`results/manual_associations/coverage.json` records coverage for every task and
mode, and each output directory has `pending_review.json`. Missing lists and
lists with fewer than K=5 surviving words remain pending; they are never padded,
automatically generated, or treated as a completed all-answer experiment.
Stage 03 defaults to the `manual_replacement/` artifact for each task and mode.
Individually reviewed malformed targets are retained with the explicit status
`no_reliable_associations` and a reason, as requested. Their Stage-03 outputs
contain vocabulary rankings but no association comparison. Missing manual lists
remain pending and do not receive this status automatically.

The recoverable subcommands are implemented in:

```text
stages/02_associations.py inventory
stages/02_associations.py build-static
```

The smoke job regenerates the landmark inventory under schema version 2 and
validates the three-answer static review catalog. It loads the tokenizer but
never loads or runs the language model.

```bash
qsub multipath-routing/jobs/run_associations_smoke.sge
```

Gradient ranking and causal interventions remain out of scope.

## Stage 03: gradient ranking

The checked mathematical core is implemented in `multipath/gradient.py`.
For target answer `y`, layer `l`, and prompt position `p`, it defines

```text
g_l,p = gradient of log P(y | prompt) with respect to h_l,p
u_t,l = unit(J_l^T w_t)
score_t,l,p = dot(g_l,p, u_t,l)
```

The target probability includes every token in a multi-token answer. Positive
scores predict that an infinitesimal edit toward token `t` increases the
target answer probability. Frozen association words receive tie-aware ranks
against the full vocabulary using `1 + count(score > selected_score)`.

True-answer and model-answer experiments use the same measurement with a
different `y`.

`stages/03_gradient.py` implements the GPU runner. It captures all six fitted
layers in one teacher-forced forward/backward pass per prompt, then scores the
vocabulary in bounded chunks. Dense vocabulary scores are not written: each
row stores the frozen association words' exact full-vocabulary and
word-vocabulary ranks plus the top 50 word tokens. The position is explicit:
`final_prompt` (the `:` in `A:` for these word tasks) or `entity_last`.

The one-prompt landmark smoke job is:

```bash
qsub multipath-routing/jobs/run_gradient_smoke.sge
```

The job has been written but not submitted. Steering and ablation remain out
of scope.
