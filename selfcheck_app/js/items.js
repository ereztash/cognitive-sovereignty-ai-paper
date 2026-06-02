// Cognitive Sovereignty Scale — trait/self-check version (pre-validation).
// Mirrors docs/cognitive_sovereignty_scale_v0.md. reverse:true items are scored
// 6 - response. Facets group items for the profile breakdown.

const FACETS = {
  noticing:     { label: "Noticing",     blurb: "spotting when you're coasting on AI" },
  questioning:  { label: "Questioning",  blurb: "checking and challenging AI output" },
  independence: { label: "Independence", blurb: "deciding for yourself, overriding AI" },
  learning:     { label: "Learning",     blurb: "internalising, not just finishing" },
  calibration:  { label: "Calibration",  blurb: "matching reliance to the stakes" },
};

const ITEMS = [
  { id: "css_01", facet: "noticing",     reverse: false, text: "I notice when I'm accepting an AI's answer without really understanding it." },
  { id: "css_02", facet: "noticing",     reverse: false, text: "I can tell the difference between truly reasoning through a problem and just feeling like I did because the AI explained it." },
  { id: "css_03", facet: "noticing",     reverse: true,  text: "After using AI, I often can't say which ideas were mine and which were the tool's." },
  { id: "css_04", facet: "noticing",     reverse: true,  text: "I'm usually unaware of how much of a task I “did” was actually done by the AI." },
  { id: "css_05", facet: "questioning",  reverse: false, text: "I check AI outputs against my own reasoning or other sources before relying on them." },
  { id: "css_06", facet: "questioning",  reverse: false, text: "I actively look for errors or weak points in what an AI gives me." },
  { id: "css_07", facet: "questioning",  reverse: true,  text: "If an AI sounds confident and fluent, I tend to just accept it." },
  { id: "css_08", facet: "questioning",  reverse: false, text: "I question the assumptions behind an AI's answer." },
  { id: "css_09", facet: "independence", reverse: false, text: "When an AI's answer conflicts with my own judgment, I'm willing to go with my judgment." },
  { id: "css_10", facet: "independence", reverse: false, text: "I treat AI output as a draft to revise, not a final answer." },
  { id: "css_11", facet: "independence", reverse: true,  text: "I find it hard to disagree with the AI even when something feels off." },
  { id: "css_12", facet: "independence", reverse: false, text: "I deliberately decide what to keep and what to discard from an AI's response." },
  { id: "css_13", facet: "learning",     reverse: false, text: "After using AI on a task, I could reproduce or explain the result on my own." },
  { id: "css_14", facet: "learning",     reverse: false, text: "I make sure I actually learn from AI-assisted work, not just complete it." },
  { id: "css_15", facet: "learning",     reverse: true,  text: "If AI tools were unavailable tomorrow, I'd struggle with tasks I've been using them for." },
  { id: "css_16", facet: "learning",     reverse: false, text: "I could rebuild an AI-assisted solution from scratch if I needed to." },
  { id: "css_17", facet: "calibration",  reverse: false, text: "I adjust how much I rely on AI depending on how important or uncertain the task is." },
  { id: "css_18", facet: "calibration",  reverse: false, text: "I'm more careful to verify AI output on high-stakes tasks." },
  { id: "css_19", facet: "calibration",  reverse: true,  text: "I use AI for almost everything by default, without thinking about whether I should." },
  { id: "css_20", facet: "calibration",  reverse: false, text: "I deliberately do some tasks without AI to keep my own skills sharp." },
];

const LIKERT = ["Strongly disagree", "Disagree", "Neither", "Agree", "Strongly agree"];

// Reflective (NOT diagnostic) interpretation bands for the 0–100 total.
const BANDS = [
  { min: 70, label: "Amplifier", text: "You tend to use AI as an amplifier: you verify, override, and internalise rather than outsource. Keep protecting the habits that make AI sharpen your thinking instead of replacing it." },
  { min: 45, label: "Mixed", text: "You use AI deliberately some of the time and on autopilot other times. The biggest gains come from adding small checks on high-stakes tasks — predict before you peek, and reconstruct afterwards." },
  { min: 0,  label: "At-risk of bypass", text: "Your answers suggest a lot of frictionless offloading. That can boost output now but quietly erode the skills underneath. Try doing the first pass yourself, then using AI to critique it." },
];

const OPTIONAL_DEMOGRAPHICS = [
  { id: "age_band", label: "Age", options: ["", "under 18", "18–24", "25–34", "35–44", "45–54", "55+"] },
  { id: "ai_use", label: "How often do you use AI tools?", options: ["", "Rarely", "Weekly", "Daily", "Many times a day"] },
];
