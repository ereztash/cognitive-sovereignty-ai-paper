# Cognitive Sovereignty Self-Check (public web app)

A polished, shareable, mobile-friendly **self-assessment** built on the
Cognitive Sovereignty Scale. It is the *wedge*, not the product: it gives each
visitor an instant score + profile (audience / B2C funnel) **and** collects
consented, anonymous responses that feed scale validation (research). Vanilla
HTML/CSS/JS — no framework, no build step, free to host.

```
index.html        single-page app
js/config.js       DataPipe ID + settings
js/items.js        the 20 CSS items, facets, reverse keys, score bands
js/app.js          flow: consent -> demographics -> items -> score/share/save
css/style.css      styling
```

## Try it locally
Open `index.html` (or `python -m http.server` then visit `localhost:8000`).
With no DataPipe ID set it scores and shares but does not upload.

## Deploy free (GitHub Pages)
Push the repo and enable Pages → the app is at
`https://<user>.github.io/<repo>/selfcheck_app/`.

## Collect data (free, optional)
Create a DataPipe experiment (https://pipe.jspsych.org) linked to an OSF
component, paste its ID into `js/config.js` → each completion POSTs one anonymous
CSV row to OSF. Reverse-score items css_03/04/07/11/15/19, then this is exactly
the data the EFA/CFA validation in the project needs.

## For teams, classes & researchers
Append `?group=NAME` to the link to tag a cohort's responses (the `group` column
ends up in the data). The open scale and analysis code live in the project repo.

## Scoring
Each item is 1–5; reverse items are flipped; the mean is rescaled to 0–100, with
per-facet sub-scores (Noticing, Questioning, Independence, Learning, Calibration).

## Integrity / honest framing (please keep)
- The app states clearly it is an **early, non-diagnostic** self-assessment and
  that responses support **ongoing validation** — do **not** market the score as
  a validated measure until the validation study (see `../docs/`) is done.
- Anonymous by design: no name/email; demographics are optional.
- Get consent (the checkbox) before launch and adapt wording to your context.

## How this fits the bigger plan
Self-check (this app) → validates the scale + builds audience/credibility →
which substantiates the eventual product (the "fortified AI" tool in
`../experiment_app/` lineage) and any B2B measurement offering.
