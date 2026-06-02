# Experiment results — SYNTHETIC DATA (dry run)

> **These are NOT empirical findings.** Data were generated under the pre-registered assumptions in `docs/preregistration_template.md` to exercise the analysis pipeline end-to-end. The hypotheses appear supported here *by construction*. To obtain real results, replace `results/experiment/synthetic_participants.csv` with real data of the same schema and re-run `python scripts/experiment/run_experiment.py`.

## Scale reliability (CSS)

```
         scale  k_items  cronbach_alpha
     CSS total       20           0.958
 F1_monitoring        4           0.806
 F2_evaluation        4           0.808
     F3_agency        4           0.832
F4_internalize        4           0.846
F5_calibration        4           0.818
```

## Convergent / discriminant validity

```
             construct     expected  r_with_CSS
    Need for Cognition   convergent       0.456
           AI literacy discriminant       0.027
           Trust in AI discriminant      -0.088
Foundational knowledge discriminant      -0.033
```

## Descriptives by condition

```
      condition  n  performance  sovereignty  retention  transfer  reconstruction  miscalibration ai_error_detection
          No AI 86       -0.004        3.115      0.247    -0.045          -0.028          -0.036                  —
Uncalibrated AI 85        0.348        2.515     -0.409    -0.483          -0.561           0.454              0.502
   Fortified AI 85        0.822        3.136     -0.142     0.070           0.194          -0.083              0.579
```

## Omnibus ANOVA

```
       outcome       F      p  eta2_partial
   performance 13.5148 0.0000        0.0965
   sovereignty 16.1929 0.0000        0.1135
     retention  6.7303 0.0015        0.0572
      transfer  6.3972 0.0020        0.0545
reconstruction 11.1739 0.0000        0.0915
miscalibration  6.9101 0.0012        0.0518
```

## Confirmatory tests (Holm-corrected)

```
                                  test hypothesis  estimate           ci95      d  stat     df  p_raw  p_holm  decision
                H1a perf: Uncal > NoAI         H1     0.352   [0.04, 0.67]  0.337  2.20  169.0 0.0145  0.0289 supported
                 H1b sov: Uncal < NoAI         H1    -0.600 [-0.83, -0.37] -0.776 -5.07  168.9 0.0000  0.0000 supported
                 H3a sov: Fort > Uncal         H3     0.622   [0.37, 0.87]   0.75  4.89  165.7 0.0000  0.0000 supported
                H3b comp: Fort > Uncal         H3     0.580   [0.37, 0.79]  0.849  5.54  165.5 0.0000  0.0000 supported
H2: offload x calibration -> retention         H2     0.487              —      —  2.43      — 0.0158  0.0289 supported
   H4: knowledge -> AI-error detection         H4     0.087              —      —  4.04      — 0.0001  0.0002 supported
```

## Figures

- `figures/experiment/performance_sovereignty_gap.png`
- `figures/experiment/condition_means.png`
- `figures/experiment/scale_scree.png`