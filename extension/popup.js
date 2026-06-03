const cb = document.getElementById("enabled");
const stats = document.getElementById("stats");

chrome.storage.sync.get({ enabled: true, predicts: 0, critiques: 0 }, (s) => {
  cb.checked = s.enabled;
  stats.textContent = `${s.predicts} predicts · ${s.critiques} critiques logged`;
});

cb.addEventListener("change", () => chrome.storage.sync.set({ enabled: cb.checked }));
