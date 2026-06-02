// Session 2 (delayed, ~1 week later): retention quiz -> independent
// reconstruction (NO help) -> transfer task -> save. Linked to Session 1 by the
// participant ID passed in the URL (?id=...).

const S2_PARAMS = new URLSearchParams(location.search);
const S2_ID = S2_PARAMS.get("id") || ("anon_" + Math.random().toString(36).slice(2, 10));
const S2_TASK = TASKS[0];

const jsPsych = initJsPsych({
  on_finish: () => {
    if (!CONFIG.DATAPIPE_EXPERIMENT_ID) {
      jsPsych.data.get().localSave("csv", S2_ID + "_S2.csv");
    }
  },
});

jsPsych.data.addProperties({ participant_id: S2_ID, study_session: "S2" });

const timeline = [];

timeline.push({
  type: jsPsychInstructions,
  pages: [`<h3>Welcome back</h3><p>This short follow-up has three parts. Please do it
    <b>without</b> any external help or AI tools — we are interested in what you took away.</p>`],
  show_clickable_nav: true,
});

// Retention quiz (auto-scorable against the keys in stimuli.js)
timeline.push({
  type: jsPsychSurveyMultiChoice,
  preamble: "Part 1 — a couple of questions about the task from last time.",
  questions: S2_TASK.retention.map((q) => ({
    prompt: q.prompt, options: q.options, required: true, name: q.name,
  })),
});

// Independent reconstruction — redo the original task from scratch, unaided
timeline.push({
  type: jsPsychSurveyText,
  preamble: "Part 2 — independent reconstruction.",
  questions: [{
    prompt: `From memory and on your own, write your best answer to the original brief:
      <div class="cs-passage">${S2_TASK.prompt}</div>`,
    name: "reconstruction", rows: 8, columns: 70, required: true,
  }],
});

// Transfer — a novel but related problem
timeline.push({
  type: jsPsychSurveyText,
  preamble: "Part 3 — a new but related problem.",
  questions: [{ prompt: S2_TASK.transfer.prompt, name: "transfer", rows: 7, columns: 70, required: true }],
});

if (CONFIG.DATAPIPE_EXPERIMENT_ID) {
  timeline.push({
    type: jsPsychPipe, action: "save",
    experiment_id: CONFIG.DATAPIPE_EXPERIMENT_ID,
    filename: S2_ID + "_S2.csv",
    data_string: () => jsPsych.data.get().csv(),
  });
}

timeline.push({
  type: jsPsychHtmlButtonResponse,
  stimulus: "<h3>All done — thank you!</h3><p>Your participation is complete.</p>",
  choices: ["Finish"],
});

jsPsych.run(timeline);
