# Lens stages for the GFx-only all-task run

No all-hop filtering is applied. Use the existing fitted Stage 1 Jacobian.

The four `run_{logit_lens,jlens}_{smoke,full_array}.sge` scripts accept
`RESULTS_ROOT`. Set it to the absolute directory:

```text
/projectnb/buinlp/rathin/composition-experiments/multi-context-interventions/generalized-task-experiments/results/gfx_only_all_tasks
```

Supply it to qsub with `-v RESULTS_ROOT=...,TASK_NAME=...` (and the actual
`TOTAL_RECORDS` and `RECORDS_PER_TASK` for arrays). Defaults retain the old
`results/<task>` behavior. Set qsub `-o` to the chosen run's logs directory;
scheduler log directives are not changed by the results-root override.

For the Python stages, let D denote the **absolute** task directory under
that root. Pass explicit paths rather than relying on old defaults:

| Script | Required path overrides |
| --- | --- |
| `merge_baseline_shards.py` | `--manifest D/prompt_manifest.jsonl --shard-directory D/baseline_shards --output D/baseline_evaluation.jsonl.gz --summary-output D/baseline_summary.json` |
| `select_correct_instances.py` | `--input D/baseline_evaluation.jsonl.gz --output D/correct_instances.jsonl.gz --summary-output D/correct_instances_summary.json` |
| `merge_logit_lens_shards.py` | `--source D/correct_instances.jsonl.gz --shard-directory D/logit_lens_shards --output D/logit_lens_evaluation.jsonl.gz --summary-output D/logit_lens_summary.json` |
| `merge_jlens_shards.py` | `--source D/logit_lens_evaluation.jsonl.gz --shard-directory D/jlens_shards --output D/jlens_evaluation.jsonl.gz --summary-output D/jlens_summary.json` |
| `export_lens_results.py` | `--input D/jlens_evaluation.jsonl.gz --catalog-summary D/baseline_summary.json --output D/experiment_results.json` |

Every invocation also takes `--task TASK_NAME`. Baseline merging compares
recorded shard paths, so absolute paths are required for these saved shards.

Before full arrays, smoke-test antonym-spanish, plus-ten-times-two, and
book-author-birthyear. Include merging and export in that validation. For a
J-Lens smoke following a Logit Lens smoke, explicitly set `INPUT_PATH` to
`D/logit_lens_smoke_5.jsonl.gz`; its default is the full merged Logit Lens file.
Smoke filenames are not full-array shard filenames: use isolated shard
directories and explicit evaluator output paths when testing the mergers.

The fresh J-Lens evaluator now writes `classification_rank_rule`. No repair
pass is needed. The merger rejects missing required metadata before writing
merged output. These changes do not alter logits, ranks, or classifications.
