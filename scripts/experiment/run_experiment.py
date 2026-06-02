"""Run the full (SYNTHETIC) experiment pipeline and assemble a report.

generate -> validate scale -> confirmatory analysis -> REPORT.md
Replace results/experiment/synthetic_participants.csv with real data of the same
schema and re-run to analyze a real study.
"""
import subprocess
import sys
from pathlib import Path
import pandas as pd
import config as C

HERE = Path(__file__).resolve().parent


def run(script):
    print(f"\n=== {script} ===")
    subprocess.run([sys.executable, str(HERE / script)], check=True)


def block(df):
    return "```\n" + df.to_string(index=False) + "\n```"


def build_report():
    desc = pd.read_csv(C.RESULTS / "descriptives_by_condition.csv").fillna("—")
    conf = pd.read_csv(C.RESULTS / "confirmatory_results.csv").fillna("—")
    rel = pd.read_csv(C.RESULTS / "scale_reliability.csv")
    val = pd.read_csv(C.RESULTS / "scale_validity.csv")
    anova = pd.read_csv(C.RESULTS / "anova_omnibus.csv")

    out = [
        "# Experiment results — SYNTHETIC DATA (dry run)\n",
        "> **These are NOT empirical findings.** Data were generated under the "
        "pre-registered assumptions in `docs/preregistration_template.md` to exercise "
        "the analysis pipeline end-to-end. The hypotheses appear supported here *by "
        "construction*. To obtain real results, replace "
        "`results/experiment/synthetic_participants.csv` with real data of the same "
        "schema and re-run `python scripts/experiment/run_experiment.py`.\n",
        "## Scale reliability (CSS)\n", block(rel),
        "\n## Convergent / discriminant validity\n", block(val),
        "\n## Descriptives by condition\n", block(desc),
        "\n## Omnibus ANOVA\n", block(anova),
        "\n## Confirmatory tests (Holm-corrected)\n", block(conf),
        "\n## Figures\n",
        "- `figures/experiment/performance_sovereignty_gap.png`",
        "- `figures/experiment/condition_means.png`",
        "- `figures/experiment/scale_scree.png`",
    ]
    (C.RESULTS / "REPORT.md").write_text("\n".join(out), encoding="utf-8")
    print(f"\nWrote {C.RESULTS / 'REPORT.md'}")


def main():
    run("generate_synthetic_data.py")
    run("analyze_scale.py")
    run("analyze_experiment.py")
    build_report()
    print("\nDone (SYNTHETIC pipeline).")


if __name__ == "__main__":
    main()
