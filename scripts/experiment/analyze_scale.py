"""SYNTHETIC scale-validation demo (MPU-1): reliability, factor check, validity."""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import config as C
from stats_utils import cronbach_alpha


def score_items(df):
    """Return CSS items reverse-scored into the sovereignty direction."""
    scored = df[C.CSS_ITEMS].copy()
    for it in C.REVERSE_ITEMS:
        scored[it] = 6 - scored[it]
    return scored


def main():
    df = pd.read_csv(C.DATA)
    scored = score_items(df)
    css_total = scored.mean(axis=1)

    rel = [{"scale": "CSS total", "k_items": len(C.CSS_ITEMS),
            "cronbach_alpha": round(cronbach_alpha(scored.values), 3)}]
    for facet, items in C.FACETS.items():
        rel.append({"scale": facet, "k_items": len(items),
                    "cronbach_alpha": round(cronbach_alpha(scored[items].values), 3)})
    rel = pd.DataFrame(rel)
    rel.to_csv(C.RESULTS / "scale_reliability.csv", index=False)

    item_rows = []
    for it in C.CSS_ITEMS:
        rest = scored.drop(columns=[it]).mean(axis=1)
        item_rows.append({"item": it, "reverse_keyed": it in C.REVERSE_ITEMS,
                          "corrected_item_total_r": round(np.corrcoef(scored[it], rest)[0, 1], 3)})
    pd.DataFrame(item_rows).to_csv(C.RESULTS / "scale_item_stats.csv", index=False)

    corr = np.corrcoef(scored.values, rowvar=False)
    eigvals, eigvecs = np.linalg.eigh(corr)
    eigvals, eigvecs = eigvals[::-1], eigvecs[:, ::-1]
    pc1 = eigvecs[:, 0]
    if pc1.mean() < 0:
        pc1 = -pc1
    pd.DataFrame({"item": C.CSS_ITEMS, "pc1_loading": np.round(pc1, 3)}).to_csv(
        C.RESULTS / "scale_factor_loadings.csv", index=False)

    val = []
    for name, col, kind in [("Need for Cognition", "nfc_z", "convergent"),
                            ("AI literacy", "ai_literacy_z", "discriminant"),
                            ("Trust in AI", "trust_z", "discriminant"),
                            ("Foundational knowledge", "knowledge_z", "discriminant")]:
        val.append({"construct": name, "expected": kind,
                    "r_with_CSS": round(np.corrcoef(css_total, df[col])[0, 1], 3)})
    pd.DataFrame(val).to_csv(C.RESULTS / "scale_validity.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.plot(range(1, len(eigvals) + 1), eigvals, marker="o")
    plt.axhline(1.0, linestyle="--", color="gray")
    plt.xlabel("Component"); plt.ylabel("Eigenvalue")
    plt.title("CSS scree plot (SYNTHETIC data)")
    plt.tight_layout(); plt.savefig(C.FIGURES / "scale_scree.png", dpi=160); plt.close()

    print("Scale reliability (SYNTHETIC):")
    print(rel.to_string(index=False))
    print(f"PC1 variance explained: {eigvals[0] / eigvals.sum():.1%}")


if __name__ == "__main__":
    main()
