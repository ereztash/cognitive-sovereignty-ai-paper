# Real-data analysis — cognitive offloading (Hu, Luo & Fleming 2019)

> **Real, published, openly-shared data — analyzed with this repo's own statistics code** (`scripts/experiment/stats_utils.py`). This is a secondary analysis of a *related* paradigm, **not** the user's pre-registered study (the Cognitive Sovereignty Scale and the fortified-gate conditions are not measured here). Raw data are fetched at runtime from the authors' repository and are **not** redistributed in this repo.

**Source.** Hu, X., Luo, L., & Fleming, S. M. (2019). A role for metamemory in cognitive offloading. *Cognition, 193*, 104012. Data/code: https://github.com/XiaoHuPsy/HuLuoFleming

## A. Offloading is metacognitively calibrated (analog of *calibrated offloading*)

**A1 — people offload (ask for help) more for difficult items:**

```
experiment  ask_difficult  ask_easy     t   dz        p_raw  n
      Exp1          0.453     0.084  8.98 1.73 1.900508e-09 27
     Exp2a          0.406     0.110  8.56 1.65 4.841019e-09 27
     Exp2b          0.530     0.126 11.19 1.77 9.709699e-14 40
      Exp3          0.567     0.293  8.74 1.38 9.980182e-11 40
```

**A2 — confidence is lower on offloaded than on self-answered items:**

```
experiment  conf_answer  conf_offloaded     t   dz        p_raw  n
     Exp2a        0.860           0.366  9.45 1.82 6.746948e-10 27
     Exp2b        0.881           0.405 15.39 2.43 3.675872e-18 40
      Exp3        0.881           0.398 17.13 2.78 3.562495e-19 38
```

Holm-corrected across the calibration family: all tests remain significant (p_holm < .05).

## B. Offloading vs unaided memory (analog of H1b) — secondary / observational

```
experiment  recall_saved  recall_unsaved  saved_beta_adj     t  p_raw  d_uncontrolled  n_trials
      Exp1         0.516           0.861          -0.145 -5.73    0.0           -0.82      1607
     Exp2a         0.504           0.889          -0.247 -9.23    0.0           -0.94      1596
     Exp2b         0.468           0.857          -0.189 -8.49    0.0           -0.94      2369
```

*Caveat:* saving was largely participant-chosen (self-selection by difficulty), so B is observational; the `saved_beta_adj` controls for item difficulty but not for unmeasured confounds, and trial-level SEs ignore within-subject clustering. Treat B as descriptive.

## How this maps to the thesis

- **Supported, in real data:** offloading is *governed by metacognitive signals* (difficulty, confidence) — the central mechanism the thesis builds on.

- **Not testable here:** cognitive *sovereignty* as a distinct construct, the fortified-gate intervention, and delayed transfer — these require the purpose-built study in `docs/preregistration_template.md` + `experiment_app/`.

## Figure
- `figures/real_data/offloading_calibration.png`
