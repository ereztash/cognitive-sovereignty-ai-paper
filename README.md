# Cognitive Sovereignty AI Paper

This repository contains a reproducible academic research project on the relationship between AI-mediated cognitive offloading, metacognitive calibration, critical thinking, and cognitive sovereignty.

## Core thesis

AI use does not inherently weaken or strengthen human cognition. The decisive variable is metacognitive calibration.

When AI offloading is uncalibrated, it may improve short-term performance while weakening critical thinking and cognitive sovereignty. When AI is designed as a calibrated and effort-preserving interface, it can become a cognitive amplifier rather than a cognitive bypass.

## Repository structure

```text
.
├── manuscript/                 # Article draft and references
├── scripts/                    # Reproducible Python analyses
├── data/                       # Source-text placeholder and data notes
├── results/                    # Generated tables
├── figures/                    # Generated visual outputs
└── docs/                       # Research design and model assumptions
```

## Reproducibility

Install dependencies:

```bash
pip install -r requirements.txt
```

Run all analyses:

```bash
python scripts/run_all.py
```

Expected outputs:

- `results/category_summary.csv`
- `results/cooccurrence_matrix.csv`
- `results/pairwise_associations.csv`
- `results/simulation_final_outcomes.csv`
- `results/simulation_session_level.csv`
- `figures/critical_thinking_trajectory.png`
- `figures/sovereignty_trajectory.png`

## Methodological status

This is currently a theoretical-computational paper. The Python outputs provide internal structure diagnostics and model-based predictions. They do not yet constitute causal empirical proof.

The next empirical step is a controlled study comparing three conditions:

1. No AI
2. Uncalibrated AI
3. Fortified AI with metacognitive calibration gates

## Research roadmap

Starter materials for turning the framework into a citable empirical
contribution live in `docs/` and `scripts/`:

- `docs/cognitive_sovereignty_scale_v0.md` — draft Cognitive Sovereignty Scale (CSS) item pool + a validation roadmap (content validity → EFA/CFA → behavioral criterion validity).
- `docs/preregistration_template.md` — pre-registration draft (hypotheses, design, measures, analysis plan) ready to time-stamp on OSF/AsPredicted before data collection.
- `scripts/power_analysis.py` — simulation-based power analysis that estimates the per-group sample size needed for the planned study; writes `results/power_analysis.csv` and `figures/power_curve.png`.

```bash
python scripts/power_analysis.py
```

### Analysis pipeline (dry run on synthetic data)

`scripts/experiment/` runs the **entire study analysis end-to-end on synthetic
data** generated under the pre-registered assumptions: it builds a participant
dataset, validates the CSS scale (reliability, factor structure, convergent/
discriminant validity), and runs every confirmatory test (H1–H4, Holm-corrected).

```bash
python scripts/experiment/run_experiment.py
```

> The outputs in `results/experiment/` and `figures/experiment/` are **SYNTHETIC**
> — a dry run that validates the analysis is correct and analyzable, **not**
> empirical findings. To analyze a real study, replace
> `results/experiment/synthetic_participants.csv` with real data of the same
> schema and re-run. See `results/experiment/REPORT.md`.

### Tests and robustness

```bash
python tests/test_pipeline.py                      # 16 checks: stats, scoring, schema, app
python scripts/experiment/robustness_check.py      # recovery rate across many datasets
```

`tests/test_pipeline.py` verifies the statistics helpers against known values,
the CSS scoring, the data schema, end-to-end effect recovery, and app/config
consistency. `robustness_check.py` re-runs the pipeline across 100 synthetic
datasets at several sample sizes and reports how reliably each hypothesis is
recovered — empirically cross-checking `scripts/power_analysis.py` (main
contrasts reach ~80% power near n≈60/group, while the H2 moderation test needs
more, consistent with the closed-form analysis).

## Working title

From Cognitive Offloading to Cognitive Sovereignty: A Computational-Metacognitive Model of Human-AI Thinking
