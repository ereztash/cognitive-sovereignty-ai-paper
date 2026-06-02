// Fortified AI — content script (prototype).
// Two metacognitive gates over ChatGPT, using DOM observation (robust-ish) rather
// than intercepting internals:
//   * predict gate  : when YOU send a new message, commit to a prediction before
//                     the answer is revealed (opaque overlay).
//   * critique nudge: when a new assistant message arrives, a non-blocking banner
//                     asks you to spot one possible flaw before accepting it.
// Everything stays local (chrome.storage); only counters are kept, not your text.
// NOTE: ChatGPT's markup changes often — the [data-message-author-role] selector
// may need updating. Browser-test before relying on it.
(function () {
  "use strict";
  const PROCESSED = new Set();
  let enabled = true;
  let gateOpen = false;

  try {
    chrome.storage.sync.get({ enabled: true }, (s) => { enabled = s.enabled; });
    chrome.storage.onChanged.addListener((c) => { if (c.enabled) enabled = c.enabled.newValue; });
  } catch (e) { /* not in extension context */ }

  function bump(key) {
    try {
      chrome.storage.sync.get({ [key]: 0 }, (s) =>
        chrome.storage.sync.set({ [key]: (s[key] || 0) + 1 }));
    } catch (e) {}
  }

  function el(tag, cls, html) {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }

  function predictGate() {
    if (gateOpen) return;
    gateOpen = true;
    const ov = el("div", "faf-overlay", `
      <div class="faf-modal">
        <div class="faf-tag">🛡 Predict first</div>
        <p>Before you read the AI's answer, commit to your own take:</p>
        <textarea class="faf-input" rows="3" placeholder="In a sentence: your best guess / what you expect…"></textarea>
        <label class="faf-conf">Confidence
          <input type="range" min="0" max="100" value="50" class="faf-range" />
          <span class="faf-val">50%</span>
        </label>
        <div class="faf-row">
          <button class="faf-skip">Skip</button>
          <button class="faf-go">I've committed — reveal</button>
        </div>
      </div>`);
    document.body.appendChild(ov);
    const range = ov.querySelector(".faf-range");
    range.addEventListener("input", () => { ov.querySelector(".faf-val").textContent = range.value + "%"; });
    const close = (logged) => { ov.remove(); gateOpen = false; if (logged) bump("predicts"); };
    ov.querySelector(".faf-go").addEventListener("click", () => close(true));
    ov.querySelector(".faf-skip").addEventListener("click", () => close(false));
  }

  function critiqueNudge() {
    if (document.querySelector(".faf-nudge")) return;
    const n = el("div", "faf-nudge", `
      <span>🛡 Before you accept this — what's one thing that could be wrong?</span>
      <input class="faf-nudge-in" placeholder="one possible flaw…" />
      <button class="faf-nudge-go">Log</button>
      <button class="faf-nudge-x" aria-label="dismiss">✕</button>`);
    document.body.appendChild(n);
    const done = (logged) => { n.remove(); if (logged) bump("critiques"); };
    n.querySelector(".faf-nudge-go").addEventListener("click", () => done(true));
    n.querySelector(".faf-nudge-x").addEventListener("click", () => done(false));
    setTimeout(() => { if (document.body.contains(n)) n.remove(); }, 25000);
  }

  function scan() {
    if (!enabled) return;
    document.querySelectorAll("[data-message-author-role]").forEach((m) => {
      let id = m.getAttribute("data-message-id");
      if (!id) { if (!m.dataset.fafId) m.dataset.fafId = "f" + Math.random().toString(36).slice(2); id = m.dataset.fafId; }
      if (PROCESSED.has(id)) return;
      PROCESSED.add(id);
      const role = m.getAttribute("data-message-author-role");
      if (role === "user") predictGate();
      else if (role === "assistant") setTimeout(critiqueNudge, 1500);
    });
  }

  function fab() {
    const b = el("button", "faf-fab", "🛡");
    b.title = "Fortified AI — predict before you ask";
    b.addEventListener("click", predictGate);
    document.body.appendChild(b);
  }

  function init() {
    if (!document.body) return setTimeout(init, 400);
    // Mark existing (historical) messages as processed so we only gate NEW ones.
    document.querySelectorAll("[data-message-author-role]").forEach((m) => {
      const id = m.getAttribute("data-message-id") || (m.dataset.fafId = "f" + Math.random().toString(36).slice(2));
      PROCESSED.add(id);
    });
    fab();
    new MutationObserver(() => { try { scan(); } catch (e) {} })
      .observe(document.body, { childList: true, subtree: true });
  }
  init();
})();
