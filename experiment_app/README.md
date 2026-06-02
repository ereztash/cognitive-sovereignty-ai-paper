# Experiment apparatus (browser-based, free to run)

A static [jsPsych](https://www.jspsych.org) experiment implementing the
pre-registered study (`docs/preregistration_template.md`): three arms
(**No AI / Uncalibrated AI / Fortified AI**), covariates, the state Cognitive
Sovereignty Scale, AI-error detection, and a delayed Session 2 (retention,
independent reconstruction, transfer).

No server, no API keys, no cost. The in-experiment "AI" uses **pre-scripted
drafts with planted errors** (`js/stimuli.js`) — a deliberate choice so every
participant in a condition sees an identical stimulus, which is what makes
error-detection measurable.

## Files

```
index.html        Session 1 (consent -> covariates -> task -> CSS -> save)
session2.html     Session 2 (delayed: retention, reconstruction, transfer)
js/config.js      settings: DataPipe ID, completion code, Likert anchors
js/scales.js      CSS (state), Need for Cognition, AI literacy, trust, knowledge, attention checks
js/stimuli.js     task bank: prompt + canned AI draft (planted errors) + quiz + transfer + rubric
js/experiment.js  Session 1 timeline + condition assignment + Fortified gates
js/session2.js    Session 2 timeline
css/style.css     styling
```

## 1. Pilot it locally (zero setup)

Open `index.html` in a browser (double-click, or `python -m http.server` then
visit `http://localhost:8000`). With no DataPipe ID set, the experiment runs in
**pilot mode** and downloads a CSV of the data at the end. Force a condition for
testing with `index.html?condition=Fortified%20AI`.

## 2. Collect real data for free (GitHub Pages + OSF)

1. **Host:** push this repo to GitHub → *Settings → Pages* → deploy from the
   branch. Your experiment will be at
   `https://<user>.github.io/<repo>/experiment_app/`.
2. **Storage:** make a free [OSF](https://osf.io) account and a project component.
3. **Pipe:** at [pipe.jspsych.org](https://pipe.jspsych.org), create an
   experiment linked to that OSF component, enable data collection, and copy the
   **experiment ID** into `DATAPIPE_EXPERIMENT_ID` in `js/config.js`.
   DataPipe then also gives you **balanced condition assignment** automatically.
4. **Recruit:** share `…/experiment_app/?id=SUBJECT123` (one ID per participant).
   After ~1 week, email each participant `…/experiment_app/session2.html?id=SUBJECT123`.

## 3. Data → analysis pipeline

Saved CSVs hold one row per trial; survey answers are JSON in the `response`
column, with `participant_id`, `condition`, and `study_session` on every row.
You will need to:

- **Score the writing** (`answer`, `reconstruction`, `transfer`) with the rubric
  in `js/stimuli.js`, ideally by two blind raters (report inter-rater reliability).
- **Auto-score** AI-error detection (`errors_flagged` vs the `error: true` claims),
  the knowledge pretest, and the retention quiz against the keys in the JS files.
- **Reverse-score** CSS items css_03/04/07/11/15/19, then average to the CSS total.
- Reshape to one row per participant matching the schema in
  `../results/experiment/synthetic_participants.csv`, then run
  `python ../scripts/experiment/run_experiment.py` (it analyzes whatever is in
  that CSV — swap synthetic for real).

## Customize

- **Add tasks:** append objects to `TASKS` in `js/stimuli.js` (the app uses
  `TASKS[0]`; loop over more for a multi-item study).
- **Edit the Fortified gates:** `taskBlock()` in `js/experiment.js`.
- **Edit items/consent:** `js/scales.js` and the consent text in `js/experiment.js`.

## Notes & caveats

- **Test in a browser before fielding.** This was written without a live browser;
  pin exact jsPsych/plugin versions and pilot end-to-end first.
- The state CSS references "the task"; for No-AI participants some items are less
  applicable — check measurement invariance across conditions during validation.
- **Ethics:** the consent text is a minimal placeholder. Adapt it, and add an
  ethics/IRB statement (or an independent-researcher ethics note) before launch.
