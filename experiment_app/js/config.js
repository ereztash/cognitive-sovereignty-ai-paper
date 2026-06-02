// Global configuration for the Cognitive Sovereignty experiment.
// Edit the values in this file to configure a deployment.

const CONFIG = {
  // To save data to OSF for free: create a DataPipe experiment at
  // https://pipe.jspsych.org (linked to an OSF component) and paste its ID here.
  // If left empty, the experiment runs in PILOT MODE and downloads a local CSV
  // at the end instead of uploading. (Great for testing; no setup needed.)
  DATAPIPE_EXPERIMENT_ID: "",

  CONDITIONS: ["No AI", "Uncalibrated AI", "Fortified AI"],

  // 5-point Likert anchors used by all attitude scales.
  LIKERT5: [
    "Strongly disagree", "Disagree", "Neither", "Agree", "Strongly agree",
  ],

  // Completion code shown at the end (e.g. for a recruitment platform).
  COMPLETION_CODE: "CS-DONE",
};
