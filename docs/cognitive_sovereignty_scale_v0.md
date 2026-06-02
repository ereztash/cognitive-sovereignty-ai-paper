# Cognitive Sovereignty Scale (CSS) — Draft v0

> **Status: pre-validation DRAFT.** This is an item pool for content review and
> piloting, *not* a validated instrument. Do not report scores as a validated
> measure until the validation steps below are completed. The contribution this
> project can make is precisely a *validated, reusable* measure — the construct
> itself is already articulated in the literature (e.g. Konigsberg, *Cognitive
> Sovereignty: The Authorship Problem in AI-Assisted Thought*), so the novelty
> here must come from a usable instrument plus criterion (behavioral) validity.

## Construct definition

**Cognitive sovereignty** is a user's retained capacity to inspect, challenge,
revise, and internalize AI-mediated reasoning — i.e., to use external cognition
without becoming epistemically dependent on it. It is hypothesized to be related
to, but distinct from, critical-thinking disposition, metacognition, trust
calibration, and AI literacy.

## Proposed facets

| # | Facet | What it captures |
|---|-------|------------------|
| F1 | Displacement monitoring | Noticing when one's thinking is being outsourced / replaced |
| F2 | Evaluation & challenge | Actively checking and questioning AI output |
| F3 | Override & agency | Willingness to revise/reject AI output and decide independently |
| F4 | Internalization & reconstruction | Learning from, and being able to reproduce, AI-assisted work |
| F5 | Calibrated reliance | Adjusting reliance to task stakes/uncertainty; protecting skills |

## Item pool (trait version)

Response scale: **1 = Strongly disagree … 5 = Strongly agree.**
Items marked **(R)** are reverse-keyed. Stem context: "When I use AI tools
(e.g., chatbots, assistants) for thinking, writing, or problem-solving…"

**F1 — Displacement monitoring**
1. I notice when I'm accepting an AI's answer without really understanding it.
2. I can tell the difference between actually reasoning through a problem and just feeling like I did because the AI explained it.
3. Afterwards I often can't say which ideas were mine and which were the tool's. (R)
4. I'm usually unaware of how much of a task I "did" was actually done by the AI. (R)

**F2 — Evaluation & challenge**
5. I check AI outputs against my own reasoning or other sources before relying on them.
6. I actively look for errors or weak points in what an AI gives me.
7. If an AI sounds confident and fluent, I tend to just accept it. (R)
8. I question the assumptions behind an AI's answer.

**F3 — Override & agency**
9. When an AI's answer conflicts with my own judgment, I'm willing to go with my judgment.
10. I treat AI output as a draft to revise, not a final answer.
11. I find it hard to disagree with the AI even when something feels off. (R)
12. I deliberately decide what to keep and what to discard from an AI's response.

**F4 — Internalization & reconstruction**
13. After using AI on a task, I could reproduce or explain the result on my own.
14. I make sure I actually learn from AI-assisted work, not just complete it.
15. If the AI were unavailable tomorrow, I'd struggle to do tasks I've been using it for. (R)
16. I can rebuild an AI-assisted solution from scratch if I need to.

**F5 — Calibrated reliance**
17. I adjust how much I rely on AI depending on how important or uncertain the task is.
18. I'm more careful to verify AI output on high-stakes tasks.
19. I use AI for almost everything by default, without thinking about whether I should. (R)
20. I deliberately do some tasks without AI to keep my own skills sharp.

> A **state/task version** can be derived by rewording to a specific session
> ("In the task I just completed…"), which is what the experiment (H1–H4) needs.

## Scoring

1. Reverse-score (R) items: `score = 6 - raw` (for a 1–5 scale).
2. Facet score = mean of its items.
3. Total CSS = mean of all items. Higher = greater cognitive sovereignty.

## Discriminant / convergent validity targets

To show CSS is a *distinct* construct (the make-or-break test), administer
alongside and report correlations with:

- **Need for Cognition** (Cacioppo & Petty, short form) — convergent, expect moderate positive.
- **Metacognitive Awareness Inventory** (Schraw & Dennison) — convergent, moderate positive.
- **Trust in Automation / AI** (e.g., Jian et al.) — expect negative with *blind* trust.
- **AI literacy** scale — small/moderate positive.
- **Social desirability** (Marlowe–Crowne short) — should be near zero (bias check).

Target: no single existing scale correlates so highly (e.g., |r| > ~0.7) that
CSS is redundant.

## Validation roadmap (lean / solo)

- [ ] **Content validity** — 3–5 knowledgeable reviewers rate each item's relevance; keep items with high agreement.
- [ ] **Cognitive interviews** — 5–8 think-aloud pretests to fix ambiguous wording.
- [ ] **Round 1 (n ≈ 150–200)** — EFA for factor structure; drop weak/cross-loading items; reliability (α / ω).
- [ ] **Round 2 (new n ≈ 150–200)** — CFA to confirm structure; convergent/discriminant correlations; test–retest on a subset.
- [ ] **Criterion / behavioral validity** — show CSS predicts behavior: AI-error detection, override of wrong AI advice, delayed independent reconstruction. *This is what makes the scale useful, not just internally consistent.*

Free tooling: **formr.org** (surveys + scheduled retest), **jsPsych + DataPipe/OSF**
(behavioral task + free data collection), **R** (`psych`, `lavaan`) or **Python**
(`factor_analyzer`, `semopy`, `pingouin`) for analysis, **OSF** for pre-reg and open data.
