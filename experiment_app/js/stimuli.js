// Task stimulus bank.
//
// Each task carries: the prompt, a CANNED AI draft split into claims (some
// deliberately wrong -> "error: true"), a Session-2 retention quiz, a transfer
// prompt, and a human-scoring rubric. Canned AI output is intentional: every
// participant in a condition sees an identical stimulus, which is what makes
// AI-error detection cleanly measurable. Add more objects to TASKS to expand
// the bank; the experiment uses TASKS[0] by default (see js/experiment.js).

const TASKS = [
  {
    id: "study_interpretation",
    domain: "scientific/statistical reasoning",
    prompt: `
      <p><b>Brief.</b> A city ran a 6-week pilot: 200 office workers were given a
      standing desk; their self-reported productivity was compared with 200
      workers who kept sitting desks. The standing-desk group reported 12% higher
      productivity. Workers were <i>not</i> randomly assigned — people chose which
      desk they wanted.</p>
      <p><b>Your task (write 4–6 sentences):</b> Should the city conclude that
      standing desks <i>cause</i> higher productivity, and roll them out to all
      10,000 employees? Justify your recommendation.</p>`,

    // Canned AI draft. Each claim is shown; "error: true" claims are the planted
    // errors used to score AI-error detection.
    ai_answer_claims: [
      { text: "The pilot shows standing desks cause a 12% productivity gain.", error: true },
      { text: "Because workers chose their own desk, the two groups may differ in motivation or job type, so this is a correlation, not proven causation.", error: false },
      { text: "Self-reported productivity can be biased and is not the same as measured output.", error: false },
      { text: "Since 200 people is a very large sample, the result is definitely statistically significant.", error: true },
      { text: "A stronger test would randomly assign workers to standing vs sitting desks before rolling out city-wide.", error: false },
    ],

    // Session 2 — retention quiz (auto-scored).
    retention: [
      {
        name: "ret_1",
        prompt: "In the desk study, why can't we conclude the desks caused higher productivity?",
        options: [
          "Workers were not randomly assigned to desk type",   // correct
          "The sample was too small to matter",
          "Standing desks are known to reduce productivity",
          "Productivity was measured with a stopwatch",
        ],
        correct: "Workers were not randomly assigned to desk type",
      },
      {
        name: "ret_2",
        prompt: "What was the main weakness of the productivity measure?",
        options: [
          "It was self-reported, not objectively measured",   // correct
          "It was measured only once",
          "It was measured by managers",
          "It used the wrong units",
        ],
        correct: "It was self-reported, not objectively measured",
      },
    ],

    // Session 2 — transfer task (novel but related; human-scored).
    transfer: {
      prompt: `
        <p>A different department reports that employees who attended an optional
        lunchtime workshop later got higher performance reviews, and proposes
        making the workshop mandatory for everyone.</p>
        <p><b>Write 3–5 sentences:</b> What is the main flaw in this reasoning,
        and what evidence would you want before making the workshop mandatory?</p>`,
    },

    rubric: `Human scoring (0–10): +points for (a) identifying self-selection /
      lack of randomization, (b) correlation != causation, (c) self-report bias,
      (d) proposing a randomized/controlled test, (e) calibrated, non-overconfident
      recommendation. The model AI draft contains 2 planted errors (claims 1 and 4).`,
  },
];
