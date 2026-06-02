"""Summarise Cognitive Sovereignty Self-Check responses by group.

Input: a responses CSV exported from DataPipe/OSF (the schema produced by
selfcheck_app), with a `group` column and raw item columns css_01..css_20.
Usage:
    python scripts/selfcheck/summarize_groups.py [responses.csv]

If no file is given (or it is missing), a clearly-labelled DEMO dataset is
synthesised so the script is runnable end-to-end. Scores are recomputed from raw
items (reverse-keying css_03/04/07/11/15/19) for robustness, using the same
config as the rest of the repo.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "experiment"))
import config as C
from stats_utils import one_way_anova

RESULTS = ROOT / "results" / "selfcheck"
FIGURES = ROOT / "figures" / "selfcheck"
RESULTS.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)
DEFAULT_INPUT = RESULTS / "responses.csv"


def synth_demo(path):
    rng = np.random.default_rng(7)
    groups = {"Class A": (0.3, 45), "Class B": (-0.2, 38), "Team X": (0.6, 41)}
    rows = []
    for g, (shift, n) in groups.items():
        latent = rng.normal(shift, 1, n)
        for i in range(n):
            row = {"uid": f"{g[:1]}{i}", "group": g, "age_band": "", "ai_use": ""}
            for it in C.CSS_ITEMS:
                v = int(np.clip(round(3 + 1.1 * (0.7 * latent[i] + rng.normal(0, 0.7))), 1, 5))
                row[it] = 6 - v if it in C.REVERSE_ITEMS else v   # store raw as the app does
            rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    return df


def score(df):
    scored = df[C.CSS_ITEMS].copy()
    for it in C.REVERSE_ITEMS:
        scored[it] = 6 - scored[it]
    df = df.copy()
    df["total"] = (scored.mean(axis=1) - 1) / 4 * 100
    for facet, items in C.FACETS.items():
        df[facet] = (scored[items].mean(axis=1) - 1) / 4 * 100
    return df


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    is_demo = not path.exists()
    if is_demo:
        print(f"No input at {path} -- synthesising a DEMO dataset (not real responses).")
        df = synth_demo(path)
    else:
        df = pd.read_csv(path)
    df = score(df)

    facets = list(C.FACETS.keys())
    summary = df.groupby("group").agg(
        n=("total", "count"), total_mean=("total", "mean"), total_sd=("total", "std"),
        **{f: (f, "mean") for f in facets}).round(1)
    summary.to_csv(RESULTS / "group_summary.csv")

    lines = ["# Cognitive Sovereignty — group summary\n"]
    if is_demo:
        lines.append("> **DEMO synthetic data** — illustrative only. Replace with a real "
                     "DataPipe/OSF export to get real group results.\n")
    lines += [f"Source: `{path.name}`  ·  groups: {df['group'].nunique()}  ·  N = {len(df)}\n",
              "```\n" + summary.to_string() + "\n```\n"]
    if df["group"].nunique() > 1:
        a = one_way_anova([df.loc[df.group == g, "total"] for g in summary.index])
        lines.append(f"**Between-group difference in total score:** "
                     f"F = {a['F']:.2f}, p = {a['p']:.4f}, partial eta^2 = {a['eta2_partial']:.3f}\n")
    (RESULTS / "GROUP_REPORT.md").write_text("\n".join(lines), encoding="utf-8")

    # figure: total by group (mean +/- SD) and facet profile
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))
    ax[0].bar(summary.index, summary["total_mean"], yerr=summary["total_sd"].fillna(0), capsize=5)
    ax[0].set_ylabel("Cognitive sovereignty (0-100)"); ax[0].set_ylim(0, 100)
    ax[0].set_title("Total score by group")
    for g in summary.index:
        ax[1].plot(facets, summary.loc[g, facets], marker="o", label=g)
    ax[1].set_ylim(0, 100); ax[1].set_title("Facet profile by group")
    ax[1].set_xticks(range(len(facets)))
    ax[1].set_xticklabels(facets, rotation=30, ha="right"); ax[1].legend(fontsize=8)
    if is_demo:
        fig.suptitle("DEMO synthetic data — illustrative only")
    fig.tight_layout(); fig.savefig(FIGURES / "group_profile.png", dpi=160); plt.close(fig)

    print(summary.to_string())
    print(f"\nWrote {RESULTS/'group_summary.csv'}, {RESULTS/'GROUP_REPORT.md'}, {FIGURES/'group_profile.png'}")


if __name__ == "__main__":
    main()
