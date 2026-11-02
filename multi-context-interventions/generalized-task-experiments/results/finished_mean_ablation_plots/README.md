# Finished mean-ablation plots

This directory collects the completed J-Lens mean-ablation class-strip plots
for five tasks. Each task has two plots:

- `scma_delta_probability_by_jlens_class.png`: single-coordinate mean ablation
  of the prompt's own intermediate.
- `sdmc_delta_probability_by_jlens_class.png`: summed correction across all
  intermediate directions.

In every panel, the x-axis is
`P(edited complete correct answer) - P(baseline complete correct answer)` and
the y-axis separates the saved J-Lens compositional and shortcut classes. The
six panels correspond to independently edited layers 12, 16, 18, 20, 22, and
24; layers are not edited simultaneously.

Included tasks:

- `landmark-country-capital`
- `park-country-capital`
- `plus-ten-times-two`
- `antonym-french`
- `word-int-times-two`

SDMC can produce very large edits because the intermediate directions overlap;
SCMA is the primary targeted mean-ablation result.
