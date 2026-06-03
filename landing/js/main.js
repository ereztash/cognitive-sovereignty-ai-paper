// Landing-page interactions: wire CTA links and the email-capture form.
(function () {
  // point CTAs at the deployed self-check / study paths
  document.querySelectorAll("[data-selfcheck]").forEach((a) => { a.href = LANDING.SELFCHECK_URL; });
  document.querySelectorAll("[data-study]").forEach((a) => { a.href = LANDING.STUDY_URL; });
  document.querySelectorAll("[data-repo]").forEach((a) => { a.href = LANDING.REPO_URL; });

  function toast(msg) {
    const t = document.createElement("div");
    t.className = "toast"; t.textContent = msg; document.body.appendChild(t);
    setTimeout(() => t.remove(), 2800);
  }

  const form = document.getElementById("notify");
  if (!form) return;
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = form.querySelector('input[type=email]').value.trim();
    if (!email) return;
    if (LANDING.FORMSPREE_ID) {
      try {
        const r = await fetch("https://formspree.io/f/" + LANDING.FORMSPREE_ID, {
          method: "POST", headers: { "Accept": "application/json" },
          body: new FormData(form),
        });
        toast(r.ok ? "Thanks — you're on the list." : "Something went wrong, try again.");
        if (r.ok) form.reset();
      } catch (err) { toast("Network error — try again later."); }
    } else if (LANDING.CONTACT_EMAIL) {
      location.href = `mailto:${LANDING.CONTACT_EMAIL}?subject=Notify%20me:%20Fortified%20AI&body=Please%20notify%20me.%20My%20email:%20${encodeURIComponent(email)}`;
    } else {
      toast("Thanks! (Set FORMSPREE_ID in config.js to collect sign-ups.)");
      form.reset();
    }
  });
})();
