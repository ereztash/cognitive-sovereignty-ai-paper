"""Robustness study: how reliably does the design recover each hypothesis?

Re-runs the full SYNTHETIC pipeline across many random datasets and reports the
recovery rate (fraction of datasets where each pre-registered test is supported
after Holm correction) at several per-group sample sizes. This empirically
cross-checks scripts/power_analysis.py. SYNTHETIC -- this is a property of the
design under the assumed effects, not evidence about the world.
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import config as C
from generate_synthetic_data import build
from analyze_experiment import prepare, confirmatory

K = 100                      # synthetic datasets per sample size
N_GRID = [40, 60, 90]


def recovery_rate(n_per_group, k=K):
    counts = None
    for s in range(k):
        res = confirmatory(prepare(build(seed=10_000 + s, n_per_group=n_per_group)))
        supported = res.set_index("test")["decision"].eq("supported").astype(int)
        counts = supported if counts is None else counts + supported
    return counts / k


def main():
    rows = [{"n_per_group": n, **recovery_rate(n).to_dict()} for n in N_GRID]
    df = pd.DataFrame(rows)
    df.to_csv(C.RESULTS / "robustness_summary.csv", index=False)

    plt.figure(figsize=(9, 5))
    for test in [c for c in df.columns if c != "n_per_group"]:
        plt.plot(df["n_per_group"], df[test], marker="o", label=test)
    plt.axhline(0.80, ls="--", color="gray")
    plt.ylim(0, 1.02); plt.xlabel("n per group"); plt.ylabel("recovery rate")
    plt.title(f"Hypothesis recovery across {K} synthetic datasets (Holm-corrected)")
    plt.legend(fontsize=8, loc="lower right"); plt.tight_layout()
    plt.savefig(C.FIGURES / "robustness_recovery.png", dpi=160); plt.close()

    print(f"Recovery rate over {K} synthetic datasets per n (Holm-corrected):")
    print(df.round(2).to_string(index=False))
    print(f"\nWrote {C.RESULTS / 'robustness_summary.csv'} and "
          f"{C.FIGURES / 'robustness_recovery.png'}")


if __name__ == "__main__":
    main()
