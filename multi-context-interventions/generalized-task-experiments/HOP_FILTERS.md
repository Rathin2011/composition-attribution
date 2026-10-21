# Separate behavioral correctness filters

`code/evaluate_hop_filters.py` reads the saved baseline and evaluates single
hops only for composition-correct query-context instances. It does not modify
the baseline, lens code, or existing lens outputs.

Run from `generalized-task-experiments`, in the model environment on a GPU:

```bash
python code/evaluate_hop_filters.py --task landmark-country-capital
```

By default it reads `results/<task>/baseline_evaluation.jsonl.gz` and writes:

- `results/<task>/composition_correct/correct_instances.jsonl.gz`
- `results/<task>/all_hops_and_composition_correct/correct_instances.jsonl.gz`
- `results/<task>/hop_evaluation.jsonl.gz`
- `results/<task>/filtering_summary.json`

The first population requires saved `x -> GFx` correctness. The second also
requires fresh `x -> Fx` and `Fx -> GFx` correctness. For alternative-route
tasks it additionally requires `x -> Gx` and `Gx -> GFx`. Every hop must pass
for that specific context instance, not just somewhere among a query's contexts.
Full generated answers are compared, not their first tokens.

The same demonstration rows and order are reused, but reformatted for each hop.
Missing Gx values are recovered from the pinned original dataset, with existing
x/Fx/GFx values checked for agreement. This preserves the existing contexts;
it does not resample them or add Gx-overlap exclusions to old manifests. Therefore
this implements the correctness criterion, not an exact reproduction of the
paper's entire prompt-sampling procedure.

The population files retain the original baseline records unchanged. Pass the
desired file explicitly to a lens runner's `--input`; existing default paths
are not switched automatically. Gx lens readouts are not added by this script.

Composition correctness remains the saved baseline result; individual hops
are evaluated singly with greedy generation. The audit saves every hop prompt,
label and prediction, including failures. The summary records model revision,
generation settings and baseline hash. Existing outputs are protected unless
`--overwrite` is passed. `--input`, `--output-root`, and `--dataset-jsonl` allow
explicit alternatives; a supplied dataset JSONL must be a trusted local snapshot.

No strict population can be inferred from composition answers alone: running
this stage requires additional model forward passes.
