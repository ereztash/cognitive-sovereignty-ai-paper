// Configuration for the public Cognitive Sovereignty Self-Check.
const CONFIG = {
  // Paste a DataPipe experiment ID (https://pipe.jspsych.org, linked to OSF) to
  // collect consented, anonymous responses for scale validation. If empty, the
  // app runs in LOCAL mode: it scores and shares but does not upload.
  DATAPIPE_ID: "",

  ITEMS_PER_PAGE: 5,
  // Optional canonical URL used in share links (defaults to the current page).
  SHARE_URL: "",
};
