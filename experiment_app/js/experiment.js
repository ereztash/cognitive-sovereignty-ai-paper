// Session 1 timeline: consent -> covariates -> task (condition-dependent) ->
// AI-error detection (AI arms) -> state CSS -> save. Random/balanced assignment
// to one of the three conditions. Pre-scripted AI (see js/stimuli.js).

const PARAMS = new URLSearchParams(location.search);
const PARTICIPANT_ID = PARAMS.get("id") || ("anon_" + Math.random().toString(36).slice(2, 10));
const TASK = TASKS[0]; // uses the first task in the bank by default

const jsPsych = initJsPsych({
  on_finish: () => {
    // Pilot mode (no DataPipe ID): download the data locally.
    if (!CONFIG.DATAPIPE_EXPERIMENT_ID) {
      jsPsych.data.get().localSave("csv", PARTICIPANT_ID + "_S1.csv");
    }
  },
});

// ---- builders ---------------------------------------------------------------
function likertBlock(items, preamble) {
  return {
    type: jsPsychSurveyLikert,
    preamble: preamble || "",
    randomize_question_order: false,
    questions: items.map((it) => ({
      prompt: it.prompt, labels: CONFIG.LIKERT5, required: true, name: it.name,
    })),
  };
}

function multiChoiceBlock(items, preamble) {
  return {
    type: jsPsychSurveyMultiChoice,
    preamble: preamble || "",
    questions: items.map((it) => ({
      prompt: it.prompt, options: it.options, required: true, name: it.name,
    })),
  };
}

function writeAnswer(name, prompt) {
  return {
    type: jsPsychSurveyText,
    questions: [{ prompt: prompt, name: name, rows: 7, columns: 70, required: true }],
  };
}

function aiDraftHtml(task) {
  const claims = task.ai_answer_claims
    .map((c) => `<p class="cs-claim">• ${c.text}</p>`).join("");
  return `<div class="cs-ai-box"><span class="cs-ai-tag">AI assistant draft</span>${claims}</div>`;
}

const cont = (html) => ({ type: jsPsychHtmlButtonResponse, stimulus: html, choices: ["Continue"] });

// ---- task block per condition ----------------------------------------------
function taskBlock(condition, task) {
  const promptHtml = `<div class="cs-passage">${task.prompt}</div>`;

  if (condition === "No AI") {
    return [cont(promptHtml + "<p>Work on this yourself. Click continue when ready to write.</p>"),
            writeAnswer("answer", "Write your answer (4–6 sentences):")];
  }

  if (condition === "Uncalibrated AI") {
    return [
      cont(promptHtml + "<p>An AI assistant has drafted an answer for you.</p>"),
      cont(aiDraftHtml(task) + "<p>You may use this however you like.</p>"),
      writeAnswer("answer", "Write your answer (4–6 sentences). Use the AI draft as you see fit:"),
    ];
  }

  // Fortified AI: metacognitive gates around the AI draft.
  return [
    cont(promptHtml),
    writeAnswer("gate_hypothesis",
      "<div class='cs-gate'><b>Before any help:</b> jot your own initial answer or approach (2–3 sentences).</div>"),
    {
      type: jsPsychSurveyLikert,
      questions: [{ prompt: "How confident are you in your initial answer?",
        labels: ["Not at all", "Slightly", "Moderately", "Very", "Extremely"],
        required: true, name: "gate_confidence_pre" }],
    },
    cont(aiDraftHtml(task) + "<div class='cs-gate'>Read the AI draft critically — it may contain mistakes.</div>"),
    writeAnswer("gate_critique",
      "<div class='cs-gate'><b>Critique:</b> what, if anything, is wrong or weak in the AI draft?</div>"),
    writeAnswer("gate_counterargument",
      "<div class='cs-gate'><b>Counter-argument:</b> give one concrete reason the AI could be wrong.</div>"),
    writeAnswer("answer", "Now write your own final answer (4–6 sentences):"),
  ];
}

// ---- assemble & run ---------------------------------------------------------
async function assignCondition() {
  const forced = PARAMS.get("condition");
  if (forced && CONFIG.CONDITIONS.includes(forced)) return forced;
  if (CONFIG.DATAPIPE_EXPERIMENT_ID && typeof jsPsychPipe !== "undefined") {
    try {
      const idx = await jsPsychPipe.getCondition(CONFIG.DATAPIPE_EXPERIMENT_ID);
      return CONFIG.CONDITIONS[idx % CONFIG.CONDITIONS.length];
    } catch (e) { /* fall back to random */ }
  }
  return CONFIG.CONDITIONS[Math.floor(Math.random() * CONFIG.CONDITIONS.length)];
}

async function run() {
  const condition = await assignCondition();
  jsPsych.data.addProperties({
    participant_id: PARTICIPANT_ID, condition: condition, study_session: "S1",
  });

  const timeline = [];

  timeline.push({
    type: jsPsychHtmlButtonResponse,
    stimulus: `<h3>Research consent</h3>
      <p style="text-align:left">You are invited to take part in a study on how people
      work with information and AI tools. It takes about 20 minutes. Participation is
      voluntary and anonymous; you may stop at any time. Data are used for research only.</p>`,
    choices: ["I agree to participate", "I do not agree"],
    on_finish: (d) => { if (d.response === 1) jsPsych.abortExperiment("Thank you. You may close this tab."); },
  });

  timeline.push({
    type: jsPsychInstructions,
    pages: [
      "<h3>Welcome</h3><p>First, a few short questionnaires. Please answer honestly — there are no right or wrong answers.</p>",
    ],
    show_clickable_nav: true,
  });

  timeline.push(likertBlock(NFC_ITEMS, "How well does each statement describe you?"));
  timeline.push(likertBlock(AI_LITERACY_ITEMS, "About AI tools:"));
  timeline.push(likertBlock(TRUST_ITEMS, "About AI tools:"));
  timeline.push(multiChoiceBlock([{ ...ATTENTION_MC }], "")); // attention check
  timeline.push(multiChoiceBlock(KNOWLEDGE_ITEMS, "A few quick reasoning questions:"));

  timeline.push({
    type: jsPsychInstructions,
    pages: [`<h3>Your task</h3><p>You'll now read a short brief and write a recommendation.
      ${condition === "No AI" ? "You will work on your own." :
        condition === "Uncalibrated AI" ? "An AI assistant will offer a draft." :
        "An AI assistant will help, with a few reflection steps along the way."}</p>`],
    show_clickable_nav: true,
  });

  timeline.push(...taskBlock(condition, TASK));

  // AI-error detection (only where an AI draft was shown)
  if (condition !== "No AI") {
    timeline.push({
      type: jsPsychSurveyMultiSelect,
      questions: [{
        prompt: "Looking back at the AI draft: which claims were INCORRECT? Select all that apply (it is fine to select none).",
        options: TASK.ai_answer_claims.map((c) => c.text),
        required: false, name: "errors_flagged",
      }],
    });
  }

  timeline.push({
    type: jsPsychSurveyLikert,
    questions: [{ prompt: "How confident are you that your final answer is correct?",
      labels: ["Not at all", "Slightly", "Moderately", "Very", "Extremely"],
      required: true, name: "answer_confidence" }],
  });

  // State Cognitive Sovereignty Scale (+ an embedded attention item)
  const cssQuestions = CSS_STATE_ITEMS.map((it) => ({
    prompt: it.prompt, labels: CONFIG.LIKERT5, required: true, name: it.name,
  }));
  cssQuestions.splice(10, 0, {
    prompt: ATTENTION_LIKERT.prompt, labels: CONFIG.LIKERT5, required: true, name: ATTENTION_LIKERT.name,
  });
  timeline.push({
    type: jsPsychSurveyLikert,
    preamble: "Thinking about the task you just completed, how much do you agree?",
    randomize_question_order: false,
    questions: cssQuestions,
  });

  // Save to OSF/DataPipe (skipped in pilot mode; on_finish downloads instead)
  if (CONFIG.DATAPIPE_EXPERIMENT_ID) {
    timeline.push({
      type: jsPsychPipe, action: "save",
      experiment_id: CONFIG.DATAPIPE_EXPERIMENT_ID,
      filename: PARTICIPANT_ID + "_S1.csv",
      data_string: () => jsPsych.data.get().csv(),
    });
  }

  timeline.push({
    type: jsPsychHtmlButtonResponse,
    stimulus: `<h3>Thank you!</h3><p>Your completion code is <b>${CONFIG.COMPLETION_CODE}</b>.</p>
      <p class="cs-note">In about a week you will be invited to a short (~10 min) second session.
      Please keep your participant ID: <b>${PARTICIPANT_ID}</b></p>`,
    choices: ["Finish"],
  });

  jsPsych.run(timeline);
}

run();
