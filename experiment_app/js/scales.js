// Measurement scales: covariates (Session 1 pre-task) and the state Cognitive
// Sovereignty Scale (post-task). Item names match the analysis schema
// (css_01..css_20, nfc_*, etc.). REVERSE-keyed items are noted; reverse-scoring
// is done at analysis time (see scripts/experiment/analyze_scale.py), not here.

// --- State Cognitive Sovereignty Scale (administered AFTER the task) ----------
// State version of docs/cognitive_sovereignty_scale_v0.md. Reverse items:
// css_03, css_04, css_07, css_11, css_15, css_19.
const CSS_STATE_ITEMS = [
  { name: "css_01", prompt: "I noticed when I was accepting information without really understanding it." },
  { name: "css_02", prompt: "I could tell the difference between actually reasoning and just feeling like I had." },
  { name: "css_03", prompt: "Afterwards, I can't really say which ideas were my own. (R)" },
  { name: "css_04", prompt: "I'm not sure how much of the work was genuinely mine. (R)" },
  { name: "css_05", prompt: "I checked the information against my own reasoning or what I already knew." },
  { name: "css_06", prompt: "I actively looked for errors or weak points in the material." },
  { name: "css_07", prompt: "I mostly just accepted what was presented to me. (R)" },
  { name: "css_08", prompt: "I questioned the assumptions behind the material." },
  { name: "css_09", prompt: "When something conflicted with my judgment, I went with my judgment." },
  { name: "css_10", prompt: "I treated the available material as a draft to revise, not a final answer." },
  { name: "css_11", prompt: "I found it hard to disagree even when something felt off. (R)" },
  { name: "css_12", prompt: "I deliberately decided what to keep and what to discard." },
  { name: "css_13", prompt: "I could reproduce or explain my answer on my own now." },
  { name: "css_14", prompt: "I made sure I actually learned from the task, not just finished it." },
  { name: "css_15", prompt: "If I had to redo this with no help at all, I would struggle. (R)" },
  { name: "css_16", prompt: "I could rebuild my solution from scratch if I needed to." },
  { name: "css_17", prompt: "I adjusted how much I relied on help based on how much the task mattered." },
  { name: "css_18", prompt: "I was more careful to verify the parts that mattered most." },
  { name: "css_19", prompt: "I relied on whatever was given by default, without thinking about it. (R)" },
  { name: "css_20", prompt: "I made a point of doing parts on my own to keep my skills sharp." },
];

// --- Covariates (administered BEFORE the task) --------------------------------
const NFC_ITEMS = [
  { name: "nfc_1", prompt: "I would prefer a complex problem to a simple one." },
  { name: "nfc_2", prompt: "I like having the responsibility of handling a situation that needs a lot of thinking." },
  { name: "nfc_3", prompt: "Thinking hard is not my idea of fun. (R)" },
  { name: "nfc_4", prompt: "I try to avoid situations where I have to think in depth about something. (R)" },
  { name: "nfc_5", prompt: "I find satisfaction in deliberating hard and for long hours." },
  { name: "nfc_6", prompt: "I really enjoy a task that involves coming up with new solutions." },
];

const AI_LITERACY_ITEMS = [
  { name: "ailit_1", prompt: "I understand, in general terms, how AI chatbots produce their answers." },
  { name: "ailit_2", prompt: "I know that AI tools can produce confident but incorrect information." },
  { name: "ailit_3", prompt: "I can usually tell when an AI answer might be unreliable." },
  { name: "ailit_4", prompt: "I know how to question or re-prompt an AI tool to get a better result." },
];

const TRUST_ITEMS = [
  { name: "trust_1", prompt: "I generally trust the answers AI tools give me." },
  { name: "trust_2", prompt: "I tend to rely on AI tools even for important decisions." },
  { name: "trust_3", prompt: "I am skeptical of information that comes from AI tools. (R)" },
  { name: "trust_4", prompt: "AI tools are usually more accurate than I am." },
];

// Foundational-knowledge pretest (domain = scientific/statistical reasoning).
// Auto-scored against `correct`.
const KNOWLEDGE_ITEMS = [
  {
    name: "know_1",
    prompt: "A study finds people who drink more coffee live longer. This best shows:",
    options: [
      "A correlation that may have other explanations",   // correct
      "That coffee causes longer life",
      "That longer life causes coffee drinking",
      "Nothing at all",
    ],
    correct: "A correlation that may have other explanations",
  },
  {
    name: "know_2",
    prompt: "Which design best supports a causal claim?",
    options: [
      "A randomized controlled trial",   // correct
      "A survey of volunteers",
      "Comparing two self-selected groups",
      "A single case study",
    ],
    correct: "A randomized controlled trial",
  },
  {
    name: "know_3",
    prompt: "A treatment 'doubles your risk', from 1 in 10,000 to 2 in 10,000. This is:",
    options: [
      "A large relative but small absolute increase",   // correct
      "A huge increase you should fear",
      "Impossible to interpret",
      "A decrease in risk",
    ],
    correct: "A large relative but small absolute increase",
  },
  {
    name: "know_4",
    prompt: "Self-reported data is most problematic because it can be affected by:",
    options: [
      "Bias and inaccurate memory",   // correct
      "Random number generators",
      "The phase of the moon",
      "Sample size alone",
    ],
    correct: "Bias and inaccurate memory",
  },
  {
    name: "know_5",
    prompt: "A bigger sample mainly improves:",
    options: [
      "The precision of an estimate",   // correct
      "Whether the study is causal",
      "Whether the measure is valid",
      "The honesty of participants",
    ],
    correct: "The precision of an estimate",
  },
];

// Attention checks (one Likert, one multi-choice). Used as pre-registered
// exclusion criteria.
const ATTENTION_LIKERT = {
  name: "attn_likert",
  prompt: "This is an attention check. Please select 'Disagree' for this item.",
  correct_index: 1, // 0-based -> "Disagree"
};

const ATTENTION_MC = {
  name: "attn_mc",
  prompt: "Attention check: please choose 'Green'.",
  options: ["Red", "Blue", "Green", "Yellow"],
  correct: "Green",
};
