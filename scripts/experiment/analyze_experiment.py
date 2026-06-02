"""SYNTHETIC confirmatory analysis (MPU-2) of the pre-registered hypotheses.

Runs the exact analysis plan from docs/preregistration_template.md:
  H1  Uncalibrated vs No AI: performance up AND sovereignty down
  H2  offloading x metacognitive calibration -> retention (moderation)
  H3  Fortified vs Uncalibrated: sovereignty up AND composite up
  H4  foundational knowledge -> AI-error detection (buffering)
Primary contrast family is Holm-corrected. Results are SYNTHETIC.
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import config as C
from stats_utils import welch_test, one_way_anova, ols, holm, zscore
from analyze_scale import score_items

OUTS = ["performance", "sovereignty", "retention", "transfer", "reconstruction"]


def main():
    df = pd.read_csv(C.DATA)
    df = df[df["attn_pass"]].copy()                       # pre-registered exclusion
    df["sovereignty"] = score_items(df).mean(axis=1)
    for col in OUTS:
        df[col + "_z"] = zscore(df[col])
    df["composite"] = (df["performance_z"] + df["sovereignty_z"]) / 2

    def arm(c, col):
        return df.loc[df["condition"] == c, col]

    desc = df.groupby("condition").agg(
        n=("participant_id", "count"),
        performance=("performance", "mean"), sovereignty=("sovereignty", "mean"),
        retention=("retention", "mean"), transfer=("transfer", "mean"),
        reconstruction=("reconstruction", "mean"), miscalibration=("miscalibration", "mean"),
        ai_error_detection=("ai_error_detection", "mean"),
    ).round(3).reindex(C.CONDITIONS)
    desc.to_csv(C.RESULTS / "descriptives_by_condition.csv")

    tests = []

    def add(name, hyp, res):
        tests.append({"test": name, "hypothesis": hyp, "estimate": round(res["diff"], 3),
                      "ci95": f"[{res['ci_low']:.2f}, {res['ci_high']:.2f}]",
                      "d": round(res["d"], 3), "stat": round(res["t"], 2),
                      "df": round(res["df"], 1), "p_raw": res["p"]})

    add("H1a perf: Uncal > NoAI", "H1",
        welch_test(arm("Uncalibrated AI", "performance"), arm("No AI", "performance"), +1))
    add("H1b sov: Uncal < NoAI", "H1",
        welch_test(arm("Uncalibrated AI", "sovereignty"), arm("No AI", "sovereignty"), -1))
    add("H3a sov: Fort > Uncal", "H3",
        welch_test(arm("Fortified AI", "sovereignty"), arm("Uncalibrated AI", "sovereignty"), +1))
    add("H3b comp: Fort > Uncal", "H3",
        welch_test(arm("Fortified AI", "composite"), arm("Uncalibrated AI", "composite"), +1))

    # H2: retention ~ offload * calibration (interaction)
    d2 = df.dropna(subset=["retention"]).copy()
    d2["offload"] = d2["condition"].map(C.OFFLOAD)
    oc = d2["offload"] - d2["offload"].mean()
    cc = d2["calibration_z"] - d2["calibration_z"].mean()
    X2 = np.column_stack([np.ones(len(d2)), oc, cc, oc * cc])
    h2 = ols(d2["retention"].values, X2,
             ["intercept", "offload", "calibration", "offload x calibration"])["offload x calibration"]

    # H4: AI-error detection ~ knowledge (AI arms only), with knowledge x fortified
    d4 = df[df["condition"] != "No AI"].dropna(subset=["ai_error_detection"]).copy()
    fort = (d4["condition"] == "Fortified AI").astype(float)
    kc = d4["knowledge_z"] - d4["knowledge_z"].mean()
    X4 = np.column_stack([np.ones(len(d4)), kc, fort, kc * fort])
    h4 = ols(d4["ai_error_detection"].values, X4,
             ["intercept", "knowledge", "fortified", "knowledge x fortified"])["knowledge"]

    res = pd.DataFrame(tests)
    res = pd.concat([res, pd.DataFrame([
        {"test": "H2: offload x calibration -> retention", "hypothesis": "H2",
         "estimate": round(h2["beta"], 3), "ci95": "", "d": "", "stat": round(h2["t"], 2),
         "df": "", "p_raw": h2["p"]},
        {"test": "H4: knowledge -> AI-error detection", "hypothesis": "H4",
         "estimate": round(h4["beta"], 3), "ci95": "", "d": "", "stat": round(h4["t"], 2),
         "df": "", "p_raw": h4["p"]},
    ])], ignore_index=True)
    res["p_holm"] = holm(res["p_raw"].values).round(4)
    res["p_raw"] = res["p_raw"].round(4)
    res["decision"] = np.where(res["p_holm"] < C.ALPHA, "supported", "n.s.")
    res.to_csv(C.RESULTS / "confirmatory_results.csv", index=False)

    anova = [dict(outcome=col, **{k: round(v, 4) for k, v in
             one_way_anova([df.loc[df.condition == c, col] for c in C.CONDITIONS]).items()})
             for col in OUTS + ["miscalibration"]]
    pd.DataFrame(anova).to_csv(C.RESULTS / "anova_omnibus.csv", index=False)

    gm = df.groupby("condition")
    x = np.arange(len(C.CONDITIONS))
    w = 0.35
    plt.figure(figsize=(8, 5))
    plt.bar(x - w / 2, gm["performance_z"].mean().reindex(C.CONDITIONS), w, label="performance (z)")
    plt.bar(x + w / 2, gm["sovereignty_z"].mean().reindex(C.CONDITIONS), w, label="sovereignty (z)")
    plt.axhline(0, color="gray", lw=0.8)
    plt.xticks(x, C.CONDITIONS); plt.ylabel("standardized mean")
    plt.title("Performance-sovereignty gap (SYNTHETIC data)"); plt.legend()
    plt.tight_layout(); plt.savefig(C.FIGURES / "performance_sovereignty_gap.png", dpi=160); plt.close()

    plt.figure(figsize=(9, 5))
    for c in C.CONDITIONS:
        plt.plot(OUTS, [gm.get_group(c)[o + "_z"].mean() for o in OUTS], marker="o", label=c)
    plt.axhline(0, color="gray", lw=0.8); plt.ylabel("standardized mean (z)")
    plt.title("Outcomes by condition (SYNTHETIC data)"); plt.legend(); plt.xticks(rotation=15)
    plt.tight_layout(); plt.savefig(C.FIGURES / "condition_means.png", dpi=160); plt.close()

    print("Confirmatory results (SYNTHETIC):")
    print(res[["test", "estimate", "p_raw", "p_holm", "decision"]].to_string(index=False))


if __name__ == "__main__":
    main()
