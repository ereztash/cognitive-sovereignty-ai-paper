# Pre-registration — Cognitive Sovereignty Experiment

> Working draft to be finalized and time-stamped on **OSF** (osf.io) or
> **AsPredicted** (aspredicted.org) *before* data collection. Sections follow
> the OSF "Preregistration" template. Fill brackets `[…]` before submitting.

## 1. Title & authors
- Title: From Cognitive Offloading to Cognitive Sovereignty — a controlled test of fortified AI
- Authors: Erez Tal-Shir [+ collaborators]
- Date: [YYYY-MM-DD]

## 2. Study type
Confirmatory, between-subjects randomized experiment with a delayed follow-up session.

## 3. Hypotheses (directional)
- **H1.** Uncalibrated AI vs No AI: **higher** immediate performance **and lower** cognitive sovereignty (a performance–sovereignty gap).
- **H2.** The negative effect of AI offloading on critical-thinking retention is **moderated by metacognitive calibration** (weaker/absent under fortified AI).
- **H3.** Fortified AI vs Uncalibrated AI: **better joint outcome** (performance + retention + sovereignty).
- **H4.** Foundational knowledge **buffers** over-dependence (better error detection / evaluation), i.e. a knowledge × condition interaction.

## 4. Design
- Three arms, random assignment: **No AI**, **Uncalibrated AI**, **Fortified AI**.
- Two sessions: **T1** (task + immediate measures), **T2** after **[7] days** (retention, transfer, independent reconstruction).
- Randomization: [tool / seed]. Allocation concealment: yes.

## 5. Conditions (manipulation)
- **No AI** — task completed without any AI assistance.
- **Uncalibrated AI** — frictionless assistant; answers on demand, no prompts to reflect.
- **Fortified AI** — same model, with **metacognitive gates** (cognitive forcing functions): pre-answer prediction, confidence rating, user hypothesis before reveal, AI-output review, counterargument generation, and delayed independent reconstruction.
- Manipulation check: [e.g., self-reported effort; gate-completion logs].

## 6. Participants
- Population: [adults / students / domain]; recruitment: [convenience / snowball / course].
- Inclusion: [fluent in task language; ≥18].
- **Sample size & justification:** target **n = [from `scripts/power_analysis.py`]** per group (total **[N]**) for **[80/90]%** power at α = .05 (one-sided primary contrasts) under the assumed effects documented in that script.
- **Stopping rule:** stop at target N (or pre-registered sequential rule); no peeking otherwise.

## 7. Materials / measures
- **Task:** a complex writing / synthesis / reasoning task with a known-good rubric.
- **Cognitive sovereignty:** state version of the CSS (`docs/cognitive_sovereignty_scale_v0.md`) + behavioral composite.
- **Covariates (T1):** Need for Cognition; metacognitive awareness; AI literacy; trust in AI; foundational-knowledge pretest (for H4); social desirability.
- **Behavioral outcomes:** AI-error detection rate; override of incorrect AI advice; confidence calibration.

## 8. Procedure
T1: consent → covariates → task (by condition) → immediate performance + state CSS + calibration. T2 (+[7]d): delayed retention quiz → **independent reconstruction** (no AI) → transfer task.

## 9. Outcome measures (operationalized)
| Construct | Measure | When |
|-----------|---------|------|
| Immediate performance | Rubric score (blind raters; report IRR) | T1 |
| Delayed retention | Quiz on task content | T2 |
| Transfer | Performance on a novel related task | T2 |
| Independent reconstruction | Quality of unaided redo | T2 |
| AI-error detection | % planted errors caught | T1 |
| Confidence calibration | |confidence − accuracy| | T1 |
| Cognitive sovereignty | State CSS + behavioral composite | T1/T2 |

## 10. Analysis plan
- **Primary:** one-way ANOVA per outcome + **pre-registered contrasts** — H1 (Uncalibrated vs No AI on performance and on sovereignty), H3 (Fortified vs Uncalibrated on sovereignty and composite). One-sided in the hypothesized direction.
- **H2/H4:** moderation via regression (condition × calibration; condition × knowledge), covariate-adjusted (ANCOVA / mixed models for T1–T2).
- **Multiple comparisons:** Holm correction across the primary contrast family.
- **Composite:** mean of standardized (z) performance and sovereignty (pre-specified weights).
- Effect sizes (d, η²) with 95% CIs reported throughout.

## 11. Data quality & exclusions
Attention checks ([n]); exclude for failed checks / impossibly fast completion / non-completion of T2. Report N excluded per rule.

## 12. Confirmatory vs exploratory
Everything above is confirmatory. Anything else is labeled exploratory.

## 13. Ethics & transparency
Informed consent; anonymized data; right to withdraw; [IRB/ethics status or independent-researcher ethics statement]. **Open by default:** de-identified data, materials, analysis code, and this pre-registration posted to OSF / this repository.
