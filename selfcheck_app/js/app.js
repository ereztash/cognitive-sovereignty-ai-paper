// Cognitive Sovereignty Self-Check — vanilla single-page app.
// Flow: intro/consent -> optional demographics -> paged Likert items -> results.

const APP = document.getElementById("app");
const PARAMS = new URLSearchParams(location.search);
const GROUP = PARAMS.get("group") || "";          // ?group=NAME tags responses
const UID = "u_" + Math.random().toString(36).slice(2, 10) + Date.now().toString(36);

const responses = {};   // item id -> 1..5 (raw, not reverse-applied)
const demo = {};        // demographic id -> value
const PAGES = [];
for (let i = 0; i < ITEMS.length; i += CONFIG.ITEMS_PER_PAGE) {
  PAGES.push(ITEMS.slice(i, i + CONFIG.ITEMS_PER_PAGE));
}
let screen = "intro";   // 'intro' | 'demo' | 0..PAGES.length-1 | 'results'

// ---- scoring ----------------------------------------------------------------
function applied(it) {
  const v = responses[it.id];
  return it.reverse ? 6 - v : v;
}
function score() {
  const sums = {}, counts = {};
  let total = 0;
  for (const it of ITEMS) {
    const v = applied(it);
    total += v;
    sums[it.facet] = (sums[it.facet] || 0) + v;
    counts[it.facet] = (counts[it.facet] || 0) + 1;
  }
  const facetScores = {};
  for (const f in sums) facetScores[f] = ((sums[f] / counts[f]) - 1) / 4 * 100;
  return { total: ((total / ITEMS.length) - 1) / 4 * 100, facetScores };
}
function band(total) {
  return BANDS.find((b) => total >= b.min) || BANDS[BANDS.length - 1];
}

// ---- data save (DataPipe -> OSF; optional) ----------------------------------
function toCSV(scored) {
  const fields = ["uid", "timestamp", "group", ...OPTIONAL_DEMOGRAPHICS.map((d) => d.id),
    ...ITEMS.map((i) => i.id), ...Object.keys(FACETS).map((f) => "facet_" + f), "total"];
  const row = [UID, new Date().toISOString(), GROUP,
    ...OPTIONAL_DEMOGRAPHICS.map((d) => demo[d.id] || ""),
    ...ITEMS.map((i) => responses[i.id]),
    ...Object.keys(FACETS).map((f) => Math.round(scored.facetScores[f])),
    Math.round(scored.total)];
  const esc = (v) => `"${String(v).replace(/"/g, '""')}"`;
  return fields.join(",") + "\n" + row.map(esc).join(",") + "\n";
}
async function saveData(scored) {
  if (!CONFIG.DATAPIPE_ID) return;
  try {
    await fetch("https://pipe.jspsych.org/api/data/", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "*/*" },
      body: JSON.stringify({ experimentID: CONFIG.DATAPIPE_ID, filename: UID + ".csv", data: toCSV(scored) }),
    });
  } catch (e) { /* fail silently; the user still gets their result */ }
}

// ---- sharing ----------------------------------------------------------------
async function share(total) {
  const url = CONFIG.SHARE_URL || (location.origin + location.pathname);
  const text = `I scored ${Math.round(total)}/100 on the Cognitive Sovereignty Self-Check — how calibrated is your AI use?`;
  if (navigator.share) { try { await navigator.share({ title: "Cognitive Sovereignty Self-Check", text, url }); return; } catch (e) {} }
  try { await navigator.clipboard.writeText(text + " " + url); toast("Link copied to clipboard"); }
  catch (e) { toast(url); }
}
function toast(msg) {
  const t = document.createElement("div");
  t.className = "toast"; t.textContent = msg; document.body.appendChild(t);
  setTimeout(() => t.remove(), 2600);
}

// ---- rendering --------------------------------------------------------------
function progressPct() {
  return Math.round(Object.keys(responses).length / ITEMS.length * 100);
}

function render() {
  if (screen === "intro") return renderIntro();
  if (screen === "demo") return renderDemo();
  if (screen === "results") return renderResults();
  return renderPage(screen);
}

function renderIntro() {
  APP.innerHTML = `
    <div class="card">
      <h1>Cognitive Sovereignty Self-Check</h1>
      <p class="lead">A 3-minute reflection on how you think <em>with</em> AI — whether you
      use it as an amplifier or a bypass. ${ITEMS.length} statements, no right answers.</p>
      <div class="note">
        <b>Honest note:</b> this is an early self-assessment, not a validated or
        diagnostic test. Your anonymous answers help validate the underlying scale
        (research). No account, no personal details required.
      </div>
      <label class="consent"><input type="checkbox" id="consent" />
        I'm 18+ and agree to take part anonymously.</label>
      <button id="start" class="btn" disabled>Start</button>
      ${GROUP ? `<p class="muted">Group: ${GROUP}</p>` : ""}
    </div>`;
  const cb = document.getElementById("consent");
  const start = document.getElementById("start");
  cb.addEventListener("change", () => { start.disabled = !cb.checked; });
  start.addEventListener("click", () => { screen = "demo"; render(); });
}

function renderDemo() {
  APP.innerHTML = `
    <div class="card">
      <h2>Two quick optional questions</h2>
      ${OPTIONAL_DEMOGRAPHICS.map((d) => `
        <label class="field">${d.label}
          <select id="${d.id}">${d.options.map((o) => `<option value="${o}">${o || "Prefer not to say"}</option>`).join("")}</select>
        </label>`).join("")}
      <button id="toItems" class="btn">Continue</button>
    </div>`;
  document.getElementById("toItems").addEventListener("click", () => {
    for (const d of OPTIONAL_DEMOGRAPHICS) demo[d.id] = document.getElementById(d.id).value;
    screen = 0; render();
  });
}

function renderPage(idx) {
  const items = PAGES[idx];
  APP.innerHTML = `
    <div class="card">
      <div class="progress"><div class="bar" style="width:${progressPct()}%"></div></div>
      <p class="muted">Part ${idx + 1} of ${PAGES.length}</p>
      ${items.map((it) => `
        <fieldset class="item" data-id="${it.id}">
          <legend>${it.text}</legend>
          <div class="likert">
            ${LIKERT.map((lab, i) => `
              <label class="${responses[it.id] === i + 1 ? "sel" : ""}">
                <input type="radio" name="${it.id}" value="${i + 1}" ${responses[it.id] === i + 1 ? "checked" : ""}/>
                <span>${lab}</span>
              </label>`).join("")}
          </div>
        </fieldset>`).join("")}
      <div class="nav">
        <button id="back" class="btn ghost">${idx === 0 ? "Back" : "Back"}</button>
        <button id="next" class="btn" disabled>${idx === PAGES.length - 1 ? "See my result" : "Next"}</button>
      </div>
    </div>`;

  const next = document.getElementById("next");
  const check = () => { next.disabled = !items.every((it) => responses[it.id]); };
  APP.querySelectorAll(".item").forEach((fs) => {
    fs.querySelectorAll('input[type=radio]').forEach((r) => {
      r.addEventListener("change", () => {
        responses[fs.dataset.id] = Number(r.value);
        fs.querySelectorAll("label").forEach((l) => l.classList.remove("sel"));
        r.closest("label").classList.add("sel");
        check();
      });
    });
  });
  check();
  document.getElementById("back").addEventListener("click", () => {
    screen = idx === 0 ? "demo" : idx - 1; render(); window.scrollTo(0, 0);
  });
  next.addEventListener("click", () => {
    if (idx === PAGES.length - 1) { screen = "results"; render(); }
    else { screen = idx + 1; render(); }
    window.scrollTo(0, 0);
  });
}

function renderResults() {
  const s = score();
  const b = band(s.total);
  saveData(s);
  APP.innerHTML = `
    <div class="card">
      <div class="scorewrap">
        <div class="score">${Math.round(s.total)}<span>/100</span></div>
        <div class="bandlabel">${b.label}</div>
      </div>
      <p class="lead">${b.text}</p>
      <h3>Your profile</h3>
      ${Object.keys(FACETS).map((f) => `
        <div class="facet">
          <div class="facet-top"><span>${FACETS[f].label}</span><span class="muted">${FACETS[f].blurb}</span></div>
          <div class="fbar"><div style="width:${Math.round(s.facetScores[f])}%"></div></div>
        </div>`).join("")}
      <button id="share" class="btn">Share my result</button>
      <button id="again" class="btn ghost">Retake</button>

      <div class="note teams">
        <b>For teams, classes & researchers:</b> add <code>?group=YOURNAME</code> to the
        link to tag a cohort's responses, and use the open scale and analysis code in the
        project repository. A validated version of the instrument is in development.
      </div>
      <p class="muted small">This is a reflective self-assessment, not a validated or
      diagnostic measure. Your anonymous responses support ongoing scale validation.</p>
    </div>`;
  document.getElementById("share").addEventListener("click", () => share(s.total));
  document.getElementById("again").addEventListener("click", () => {
    for (const k in responses) delete responses[k];
    screen = "intro"; render(); window.scrollTo(0, 0);
  });
}

render();
