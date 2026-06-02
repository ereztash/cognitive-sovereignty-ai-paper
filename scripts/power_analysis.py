"""
Simulation-based power analysis for the Cognitive Sovereignty experiment.

This repurposes the project's modeling approach: instead of *illustrating*
predictions, it estimates the per-group sample size needed to detect the
pre-registered effects with adequate power. Closed-form formulas do not cleanly
cover a three-arm design with several joint outcomes, so we simulate the planned
analysis many times under assumed effect sizes and count how often it succeeds.

Design (see docs/preregistration_template.md): between-subjects, three arms
(No AI, Uncalibrated AI, Fortified AI). Primary standardized outcomes (SD = 1):
performance (immediate quality) and sovereignty (state CSS + behavioral
composite). Composite = mean(performance, sovereignty).

ALL effect sizes below are ASSUMPTIONS to revise from pilot data / literature;
they are standardized mean differences (Cohen's d) relative to the No AI group.
Defaults are rough reads of current findings (e.g. Gerlich 2025; Fan et al.
2025) and must not be treated as established truths.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

# ---- Assumptions (edit these) -------------------------------------------
ALPHA = 0.05                  # per primary contrast, one-sided (directional H)
N_SIM = 2000                  # simulated studies per candidate sample size
N_GRID = range(20, 211, 10)   # candidate n PER GROUP
RHO = 0.0                     # within-person corr between the two outcomes
SD = 1.0
SEED = 42

# Standardized group means (d vs No AI): AI lifts performance; uncalibrated AI
# lowers sovereignty; fortified AI roughly preserves it.
MEANS = {
    "performance": {"No AI": 0.0, "Uncalibrated AI": 0.50, "Fortified AI": 0.60},
    "sovereignty": {"No AI": 0.0, "Uncalibrated AI": -0.60, "Fortified AI": 0.10},
}
CONDITIONS = ["No AI", "Uncalibrated AI", "Fortified AI"]
# -------------------------------------------------------------------------

rng = np.random.default_rng(SEED)


def simulate_group(condition, n):
    """Draw correlated (performance, sovereignty) scores for one group."""
    mean = [MEANS["performance"][condition], MEANS["sovereignty"][condition]]
    off = RHO * SD * SD
    cov = [[SD ** 2, off], [off, SD ** 2]]
    draws = rng.multivariate_normal(mean, cov, size=n)
    return draws[:, 0], draws[:, 1]


def one_sided_p(a, b, direction):
    """One-sided Welch t-test p-value for mean(a) - mean(b) in `direction` (+1/-1)."""
    _, p_two = stats.ttest_ind(a, b, equal_var=False)
    favorable = direction * (np.mean(a) - np.mean(b)) > 0
    return p_two / 2 if favorable else 1 - p_two / 2


def run_power(n):
    hits = {"H1a_perf": 0, "H1b_sov": 0, "H1_joint": 0, "H3a_sov": 0, "H3b_comp": 0}
    for _ in range(N_SIM):
        perf = {c: None for c in CONDITIONS}
        sov = {c: None for c in CONDITIONS}
        for c in CONDITIONS:
            perf[c], sov[c] = simulate_group(c, n)
        comp = {c: (perf[c] + sov[c]) / 2 for c in CONDITIONS}
        # H1: Uncalibrated vs No AI -> performance up AND sovereignty down
        p1a = one_sided_p(perf["Uncalibrated AI"], perf["No AI"], +1)
        p1b = one_sided_p(sov["Uncalibrated AI"], sov["No AI"], -1)
        # H3: Fortified vs Uncalibrated -> sovereignty up AND composite up
        p3a = one_sided_p(sov["Fortified AI"], sov["Uncalibrated AI"], +1)
        p3b = one_sided_p(comp["Fortified AI"], comp["Uncalibrated AI"], +1)
        hits["H1a_perf"] += p1a < ALPHA
        hits["H1b_sov"] += p1b < ALPHA
        hits["H1_joint"] += (p1a < ALPHA) and (p1b < ALPHA)
        hits["H3a_sov"] += p3a < ALPHA
        hits["H3b_comp"] += p3b < ALPHA
    return {k: v / N_SIM for k, v in hits.items()}


def main():
    tests = ["H1a_perf", "H1b_sov", "H1_joint", "H3a_sov", "H3b_comp"]
    rows = []
    for n in N_GRID:
        power = run_power(n)
        power["n_per_group"] = n
        power["N_total"] = n * len(CONDITIONS)
        rows.append(power)
    df = pd.DataFrame(rows)[["n_per_group", "N_total"] + tests]
    df.to_csv(RESULTS / "power_analysis.csv", index=False)

    plt.figure(figsize=(9, 5))
    for t in tests:
        plt.plot(df["n_per_group"], df[t], marker="o", label=t)
    plt.axhline(0.80, linestyle="--", linewidth=1, color="gray")
    plt.axhline(0.90, linestyle=":", linewidth=1, color="gray")
    plt.xlabel("Sample size per group (3 groups)")
    plt.ylabel("Estimated power")
    plt.title("Simulation-based power by sample size (assumed effects)")
    plt.ylim(0, 1.02)
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "power_curve.png", format="png", dpi=160)
    plt.close()

    print("Minimum n PER GROUP for target power (under assumed effects):")
    for t in tests:
        n80 = df.loc[df[t] >= 0.80, "n_per_group"].min()
        n90 = df.loc[df[t] >= 0.90, "n_per_group"].min()
        s80 = "n/a" if pd.isna(n80) else str(int(n80))
        s90 = "n/a" if pd.isna(n90) else str(int(n90))
        print(f"  {t:10s}  80% -> {s80:>5}   90% -> {s90:>5}   (x3 groups)")
    print(f"\nWrote {RESULTS / 'power_analysis.csv'} and {FIGURES / 'power_curve.png'}")


if __name__ == "__main__":
    main()
