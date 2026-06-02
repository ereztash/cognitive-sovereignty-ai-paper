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

## Working title

From Cognitive Offloading to Cognitive Sovereignty: A Computational-Metacognitive Model of Human-AI Thinking
