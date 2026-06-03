# Fortified AI — browser extension (prototype MVP)

A Manifest V3 Chrome/Edge extension that adds two **metacognitive gates** to your
AI chats — the intervention from this project's thesis, as a real tool:

- **Predict first** — when you send a message, an overlay asks you to commit to
  your own answer + confidence *before* the AI's response is revealed.
- **Critique before you accept** — when a reply arrives, a non-blocking banner
  asks you to name one thing that might be wrong.

It targets ChatGPT (`chatgpt.com`, `chat.openai.com`). Everything is **local**:
only counters are stored (`chrome.storage`), never your text — nothing is sent
anywhere.

## Install (load unpacked)
1. Chrome/Edge → `chrome://extensions` → enable **Developer mode**.
2. **Load unpacked** → select this `extension/` folder.
3. Open ChatGPT, send a message → the predict gate appears; after the reply, the
   critique nudge appears. Toggle on/off from the toolbar popup.

## Files
```
manifest.json   MV3 manifest (permissions: storage; hosts: ChatGPT)
content.js      the gates (DOM observation; no internals intercepted)
content.css     overlay / banner / button styles
popup.html/js   on-off toggle + counters
```

## Caveats (it's a prototype)
- ChatGPT's HTML changes often. The gates rely on the
  `[data-message-author-role]` attribute; if it changes, update the selector in
  `content.js`. The floating 🛡 button always opens the predict gate manually.
- This is an MVP to demonstrate the mechanism and gather usage signal — not a
  polished product. **Test in your browser before depending on it.**
- No icons are bundled (Chrome uses a default); add `icons` to the manifest for a
  store listing.

## How it maps to the project
This is product direction **A** (the "fortified AI" tool). Its efficacy claim —
that gates preserve cognitive sovereignty — is exactly what the controlled study
in `../experiment_app/` + `../docs/preregistration_template.md` is designed to
test. Ship the gate, measure the effect, then make the claim.
