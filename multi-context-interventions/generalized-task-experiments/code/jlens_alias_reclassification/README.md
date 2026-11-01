# Conservative alias-aware J-Lens classification

This directory tests whether prompts originally classified as J-Lens shortcut
candidates contain their correct country intermediate under another surface
form.  It supports `landmark-country-capital` and `park-country-capital`.

## Measurement

`evaluate_aliases.py` reruns only original shortcut instances.  For the
canonical country and every predeclared alias, it computes the first token's
full-vocabulary rank at all query positions and fitted J-Lens layers
`{12,16,18,20,22,24}`.  The best rank determines the alias-aware label:

- rank 1--2: compositional;
- rank 3--4: ambiguous;
- rank 5 or worse: shortcut candidate.

The prompt is unchanged and no intervention is performed.

## Conservative postprocessing

`postprocess_alias_results.py` uses the saved ranks without rerunning the
model.  The primary analysis keeps an alias only if its complete spelling is
one tokenizer token and that token is not used for another country.  `CAR` is
explicitly rejected as a common word.  `US` is reported only as a sensitivity
analysis because it is also an English pronoun when case is ignored.  The
policy is recorded in `alias_filter_policy.json`, and every alias receives an
audit row with its tokenization, status, and rejection reasons.

Canonical rerun drift is separated from genuine alias effects.  The final
query-level result overlays the filtered labels on the complete original
J-Lens population, including contexts that were already compositional or
ambiguous.  A query's shortcut rate is the fraction of paper-token-eligible
contexts that remain shortcut; majority shortcut means strictly more than
half, and all-context shortcut means every eligible context.

## Limitations

- Canonical names retain the original first-token scoring, while primary
  aliases must be complete single tokens.
- Full-name/sequence scoring was not performed.
- There is no wrong-country alias null control.
- The fixed number of accepted aliases differs across countries.
