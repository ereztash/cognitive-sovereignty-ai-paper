"""Run this repo's analysis logic on a REAL, published cognitive-offloading dataset.

DATASET (third-party, fetched at runtime -- NOT redistributed in this repo):
  Hu, X., Luo, L., & Fleming, S. M. (2019). A role for metamemory in cognitive
  offloading. Cognition, 193, 104012. https://doi.org/10.1016/j.cognition.2019.104012
  Data + code: https://github.com/XiaoHuPsy/HuLuoFleming  (no explicit license;
  used here for non-commercial secondary analysis with citation; only aggregate
  results are written to this repo).

WHY THIS DATASET. No public dataset measures the exact pre-registered design
(the Cognitive Sovereignty Scale + the three "fortified-gate" conditions do not
exist in any released data -- that is the gap the proposed study fills). This is
the closest REAL analog: participants study word pairs and may OFFLOAD them to an
external store / ask for help, with memory and confidence recorded. It lets us
test real-world analogs of the thesis's core claims:

  A. Offloading is metacognitively calibrated  (analog of "calibrated offloading"):
     people offload (ask for help) MORE for difficult items, and report LOWER
     confidence on offloaded than on self-answered items.
  B. Offloading vs unaided memory (analog of H1b): in the forced-recall test
     (no external help), recall for previously-saved vs unsaved items, with
     difficulty controlled.  [secondary / observational -- see caveats]

This is a real secondary analysis -- it is NOT the user's pre-registered study.
"""
import io
import sys
import tarfile
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "experiment"))
from stats_utils import cohen_d, ols, holm  # this repo's own statistics code

DATA_DIR = ROOT / "data" / "external" / "HuLuoFleming-master"
RESULTS = ROOT / "results" / "real_data"
FIGURES = ROOT / "figures" / "real_data"
RESULTS.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)
TARBALL = "https://codeload.github.com/XiaoHuPsy/HuLuoFleming/tar.gz/refs/heads/master"
EXPERIMENTS = {"Exp1": "rawData_Experiment1.mat", "Exp2a": "rawData_Experiment2a.mat",
               "Exp2b": "rawData_Experiment2b.mat", "Exp3": "rawData_Experiment3.mat"}


def _safe_extractall(tar, dest):
    """Extract only members that stay within `dest` (guards against path traversal)."""
    dest = Path(dest).resolve()
    for member in tar.getmembers():
        target = (dest / member.name).resolve()
        if target != dest and dest not in target.parents:
            raise ValueError(f"Blocked unsafe tar member: {member.name}")
    try:
        tar.extractall(dest, filter="data")      # extra hardening on Python 3.12+
    except TypeError:
        tar.extractall(dest)


def ensure_data():
    if DATA_DIR.exists():
        return
    print("Downloading real dataset (Hu, Luo & Fleming 2019) ...")
    raw = urllib.request.urlopen(TARBALL, timeout=120).read()
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        _safe_extractall(tar, DATA_DIR.parent)
    print(f"  extracted to {DATA_DIR}")


def _num(x):
    if isinstance(x, np.ndarray):
        return float(x) if x.size == 1 else np.nan
    try:
        return float(x)
    except (TypeError, ValueError):
        return np.nan


def load_retrieval(matfile):
    import scipy.io as sio
    retr = sio.loadmat(str(DATA_DIR / "rawData" / matfile),
                       squeeze_me=True, struct_as_record=False)["rawData"].retrieval
    retr = retr if hasattr(retr, "__len__") else [retr]
    rows = []
    for subj in range(len(retr)):
        for t in np.atleast_2d(retr[subj]):
            # Exp1 has 9 columns (no confidence); Exp2a/2b/3 have 11.
            rows.append({"subj": subj, "test_type": t[3], "recall": _num(t[4]),
                         "ask": _num(t[6]), "difficulty": t[7],
                         "save": t[8] if len(t) > 8 else np.nan,
                         "confidence": _num(t[10]) if len(t) > 10 else np.nan})
    return pd.DataFrame(rows)


def paired(a, b):
    """Paired t-test on subject-level vectors a vs b (drop rows with NaN in either)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = ~np.isnan(a) & ~np.isnan(b)
    a, b = a[ok], b[ok]
    t, p = stats.ttest_rel(a, b)
    diff = a - b
    dz = diff.mean() / diff.std(ddof=1)
    return {"mean_a": a.mean(), "mean_b": b.mean(), "t": t, "p": p, "dz": dz, "n": len(a)}


def main():
    ensure_data()
    calib_diff, calib_conf, mem_rows = [], [], []

    for exp, matfile in EXPERIMENTS.items():
        df = load_retrieval(matfile)
        free = df[df["test_type"] == "free"].copy()
        forced = df[df["test_type"] == "forced"].copy()

        # A1: ask-for-help proportion, difficult vs easy (per-subject paired)
        ap = free.groupby(["subj", "difficulty"])["ask"].mean().unstack()
        if {"easy", "difficult"}.issubset(ap.columns):
            r = paired(ap["difficult"], ap["easy"])
            calib_diff.append({"experiment": exp, "ask_difficult": round(r["mean_a"], 3),
                               "ask_easy": round(r["mean_b"], 3),
                               "t": round(r["t"], 2), "dz": round(r["dz"], 2),
                               "p_raw": r["p"], "n": r["n"]})

        # A2: confidence on self-answered (ask=0) vs offloaded (ask=1) trials
        cf = free.dropna(subset=["confidence", "ask"])
        cc = cf.groupby(["subj", "ask"])["confidence"].mean().unstack()
        if {0.0, 1.0}.issubset(cc.columns) and cc[0.0].notna().sum() > 5:
            r = paired(cc[0.0], cc[1.0])
            calib_conf.append({"experiment": exp, "conf_answer": round(r["mean_a"], 3),
                               "conf_offloaded": round(r["mean_b"], 3),
                               "t": round(r["t"], 2), "dz": round(r["dz"], 2),
                               "p_raw": r["p"], "n": r["n"]})

        # B: forced-recall ~ saved + difficulty (trial-level OLS; clustering caveat)
        fb = forced[forced["save"].isin(["saved", "unsaved"])].dropna(subset=["recall"]).copy()
        saved = (fb["save"] == "saved").astype(float).values
        hard = (fb["difficulty"] == "difficult").astype(float).values
        if len(fb) > 30 and saved.min() != saved.max():
            cols, names = [np.ones(len(fb)), saved], ["intercept", "saved"]
            if hard.min() != hard.max():           # add difficulty control only if it varies
                cols.append(hard); names.append("difficult")
            out = ols(fb["recall"].values, np.column_stack(cols), names)["saved"]
            d = cohen_d(fb.loc[fb.save == "saved", "recall"], fb.loc[fb.save == "unsaved", "recall"])
            mem_rows.append({"experiment": exp,
                             "recall_saved": round(fb.loc[fb.save == "saved", "recall"].mean(), 3),
                             "recall_unsaved": round(fb.loc[fb.save == "unsaved", "recall"].mean(), 3),
                             "saved_beta_adj": round(out["beta"], 3), "t": round(out["t"], 2),
                             "p_raw": round(out["p"], 4), "d_uncontrolled": round(d, 2),
                             "n_trials": len(fb)})

    calib_diff = pd.DataFrame(calib_diff)
    calib_conf = pd.DataFrame(calib_conf)
    mem = pd.DataFrame(mem_rows)

    # Holm across the primary calibration family (A1 + A2 across experiments)
    fam = pd.concat([calib_diff.assign(test="A1 ask: difficult>easy"),
                     calib_conf.assign(test="A2 conf: answer>offloaded")], ignore_index=True)
    fam["p_holm"] = holm(fam["p_raw"].values).round(4)
    fam["p_raw"] = fam["p_raw"].round(4)
    calib_diff.round(4).to_csv(RESULTS / "offloading_by_difficulty.csv", index=False)
    calib_conf.round(4).to_csv(RESULTS / "confidence_by_choice.csv", index=False)
    mem.to_csv(RESULTS / "memory_saved_vs_unsaved.csv", index=False)

    # Figure: calibration of offloading (Exp2a as the illustrative example)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
    if not calib_diff.empty:
        x = np.arange(len(calib_diff))
        ax[0].bar(x - 0.2, calib_diff["ask_easy"], 0.4, label="easy items")
        ax[0].bar(x + 0.2, calib_diff["ask_difficult"], 0.4, label="difficult items")
        ax[0].set_xticks(x); ax[0].set_xticklabels(calib_diff["experiment"])
        ax[0].set_ylabel("P(ask for help / offload)")
        ax[0].set_title("Offloading tracks difficulty"); ax[0].legend()
    if not calib_conf.empty:
        x = np.arange(len(calib_conf))
        ax[1].bar(x - 0.2, calib_conf["conf_answer"], 0.4, label="self-answered")
        ax[1].bar(x + 0.2, calib_conf["conf_offloaded"], 0.4, label="offloaded")
        ax[1].set_xticks(x); ax[1].set_xticklabels(calib_conf["experiment"])
        ax[1].set_ylabel("mean confidence")
        ax[1].set_title("Lower confidence -> offload"); ax[1].legend()
    fig.suptitle("Real data (Hu, Luo & Fleming 2019): offloading is metacognitively calibrated")
    fig.tight_layout()
    fig.savefig(FIGURES / "offloading_calibration.png", dpi=160)
    plt.close(fig)

    write_report(calib_diff, calib_conf, mem, fam)
    print("A1 (ask: difficult vs easy):\n", calib_diff.to_string(index=False))
    print("\nA2 (confidence: answer vs offloaded):\n", calib_conf.to_string(index=False))
    print("\nB (forced recall: saved vs unsaved, difficulty-adjusted):\n", mem.to_string(index=False))


def block(df):
    return "```\n" + df.to_string(index=False) + "\n```"


def write_report(calib_diff, calib_conf, mem, fam):
    holm_ok = (fam["p_holm"] < 0.05).all()
    out = [
        "# Real-data analysis — cognitive offloading (Hu, Luo & Fleming 2019)\n",
        "> **Real, published, openly-shared data — analyzed with this repo's own "
        "statistics code** (`scripts/experiment/stats_utils.py`). This is a secondary "
        "analysis of a *related* paradigm, **not** the user's pre-registered study "
        "(the Cognitive Sovereignty Scale and the fortified-gate conditions are not "
        "measured here). Raw data are fetched at runtime from the authors' repository "
        "and are **not** redistributed in this repo.\n",
        "**Source.** Hu, X., Luo, L., & Fleming, S. M. (2019). A role for metamemory "
        "in cognitive offloading. *Cognition, 193*, 104012. "
        "Data/code: https://github.com/XiaoHuPsy/HuLuoFleming\n",
        "## A. Offloading is metacognitively calibrated (analog of *calibrated offloading*)\n",
        "**A1 — people offload (ask for help) more for difficult items:**\n",
        block(calib_diff),
        "\n**A2 — confidence is lower on offloaded than on self-answered items:**\n",
        block(calib_conf),
        f"\nHolm-corrected across the calibration family: "
        f"{'all tests remain significant (p_holm < .05).' if holm_ok else 'see p_holm column.'}\n",
        "## B. Offloading vs unaided memory (analog of H1b) — secondary / observational\n",
        block(mem),
        "\n*Caveat:* saving was largely participant-chosen (self-selection by "
        "difficulty), so B is observational; the `saved_beta_adj` controls for item "
        "difficulty but not for unmeasured confounds, and trial-level SEs ignore "
        "within-subject clustering. Treat B as descriptive.\n",
        "## How this maps to the thesis\n",
        "- **Supported, in real data:** offloading is *governed by metacognitive "
        "signals* (difficulty, confidence) — the central mechanism the thesis builds on.\n",
        "- **Not testable here:** cognitive *sovereignty* as a distinct construct, the "
        "fortified-gate intervention, and delayed transfer — these require the "
        "purpose-built study in `docs/preregistration_template.md` + `experiment_app/`.\n",
        "## Figure\n- `figures/real_data/offloading_calibration.png`\n",
    ]
    (RESULTS / "REAL_DATA_REPORT.md").write_text("\n".join(out), encoding="utf-8")


if __name__ == "__main__":
    main()
