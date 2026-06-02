"""Automated checks for the analysis code and the experiment app.

Run with:  python tests/test_pipeline.py      (no pytest required)
       or:  pytest tests/

Covers: statistics helpers (against known values), config integrity, CSS
reverse-scoring, synthetic-data schema, an end-to-end pipeline recovery check,
and static consistency checks on the jsPsych app (plugins loaded, reverse items
match the analysis config).
"""
import re
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "experiment"))

import config as C
import stats_utils as su
from generate_synthetic_data import build
from analyze_scale import score_items
from analyze_experiment import prepare, confirmatory

APP = ROOT / "experiment_app"


# ---- stats_utils (known values / properties) --------------------------------
def test_zscore():
    z = su.zscore(np.arange(1, 101))
    assert abs(np.nanmean(z)) < 1e-9 and abs(np.nanstd(z, ddof=1) - 1) < 1e-2


def test_cohen_d_known():
    rng = np.random.default_rng(0)
    a, b = rng.normal(0.8, 1, 20000), rng.normal(0.0, 1, 20000)
    assert abs(su.cohen_d(a, b) - 0.8) < 0.05


def test_welch_one_sided_direction():
    rng = np.random.default_rng(1)
    a, b = rng.normal(1.0, 1, 500), rng.normal(0.0, 1, 500)
    assert su.welch_test(a, b, +1)["p"] < 1e-3      # correct direction -> tiny p
    assert su.welch_test(a, b, -1)["p"] > 0.999     # wrong direction -> ~1


def test_anova_eta2_handcomputed():
    r = su.one_way_anova([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    assert abs(r["eta2_partial"] - 54.0 / 60.0) < 1e-6   # SS_b=54, SS_w=6


def test_ols_recovers_known_betas():
    rng = np.random.default_rng(2)
    x1, x2 = rng.normal(size=2000), rng.normal(size=2000)
    y = 2.0 + 3.0 * x1 - 1.5 * x2                         # noiseless
    out = su.ols(y, np.column_stack([np.ones(2000), x1, x2]), ["b0", "b1", "b2"])
    assert abs(out["b0"]["beta"] - 2.0) < 1e-6
    assert abs(out["b1"]["beta"] - 3.0) < 1e-6
    assert abs(out["b2"]["beta"] + 1.5) < 1e-6


def test_holm_known():
    adj = su.holm([0.01, 0.04, 0.03])                    # -> [0.03, 0.06, 0.06]
    assert abs(adj[0] - 0.03) < 1e-9
    assert abs(adj[1] - 0.06) < 1e-9
    assert abs(adj[2] - 0.06) < 1e-9


def test_cronbach_bounds():
    rng = np.random.default_rng(3)
    latent = rng.normal(size=(500, 1))
    correlated = latent + rng.normal(scale=0.3, size=(500, 8))
    independent = rng.normal(size=(500, 8))
    assert su.cronbach_alpha(correlated) > 0.85
    assert su.cronbach_alpha(independent) < 0.2


# ---- config integrity -------------------------------------------------------
def test_facets_partition_items():
    covered = [it for items in C.FACETS.values() for it in items]
    assert sorted(covered) == sorted(C.CSS_ITEMS)
    assert len(covered) == len(set(covered)) == 20
    assert C.REVERSE_ITEMS.issubset(set(C.CSS_ITEMS))


# ---- scoring ----------------------------------------------------------------
def test_reverse_scoring():
    df = build(seed=5, n_per_group=10)
    scored = score_items(df)
    rev = sorted(C.REVERSE_ITEMS)[0]
    assert (scored[rev] == 6 - df[rev]).all()
    nonrev = [i for i in C.CSS_ITEMS if i not in C.REVERSE_ITEMS][0]
    assert (scored[nonrev] == df[nonrev]).all()


# ---- synthetic-data schema --------------------------------------------------
def test_generate_schema():
    df = build(seed=7, n_per_group=50)
    assert len(df) == 150
    assert df["condition"].value_counts().to_dict() == {c: 50 for c in C.CONDITIONS}
    for it in C.CSS_ITEMS:
        assert df[it].between(1, 5).all()
    assert df.loc[df.condition == "No AI", "ai_error_detection"].isna().all()
    assert df.loc[df.condition != "No AI", "ai_error_detection"].between(0, 1).all()


# ---- end-to-end recovery ----------------------------------------------------
def test_pipeline_recovers_effects():
    res = confirmatory(prepare(build(seed=123, n_per_group=200))).set_index("test")
    assert res.loc["H1b sov: Uncal < NoAI", "estimate"] < 0
    assert res.loc["H1b sov: Uncal < NoAI", "decision"] == "supported"
    assert res.loc["H3a sov: Fort > Uncal", "estimate"] > 0
    assert res.loc["H3a sov: Fort > Uncal", "decision"] == "supported"
    assert res.loc["H1a perf: Uncal > NoAI", "estimate"] > 0
    assert float(res.loc["H2: offload x calibration -> retention", "estimate"]) > 0
    assert float(res.loc["H4: knowledge -> AI-error detection", "estimate"]) > 0


def test_css_reliability_high():
    assert su.cronbach_alpha(score_items(build(seed=11, n_per_group=200)).values) > 0.85


# ---- experiment app static checks -------------------------------------------
PLUGIN_OF = {
    "jsPsychHtmlButtonResponse": "plugin-html-button-response",
    "jsPsychInstructions": "plugin-instructions",
    "jsPsychSurveyLikert": "plugin-survey-likert",
    "jsPsychSurveyMultiChoice": "plugin-survey-multi-choice",
    "jsPsychSurveyMultiSelect": "plugin-survey-multi-select",
    "jsPsychSurveyText": "plugin-survey-text",
    "jsPsychPipe": "plugin-pipe",
}


def _check_plugins(html, js):
    loaded = set(re.findall(r"plugin-[a-z-]+", (APP / html).read_text()))
    used = set(re.findall(r"jsPsych[A-Z][A-Za-z]+", (APP / "js" / js).read_text()))
    for g in used:
        if g in PLUGIN_OF:
            assert PLUGIN_OF[g] in loaded, f"{g} used in {js} but {PLUGIN_OF[g]} not in {html}"


def test_app_session1_plugins_present():
    _check_plugins("index.html", "experiment.js")


def test_app_session2_plugins_present():
    _check_plugins("session2.html", "session2.js")


def test_app_reverse_items_match_config():
    marked = set()
    for line in (APP / "js" / "scales.js").read_text().splitlines():
        m = re.search(r'name:\s*"(css_\d\d)"', line)
        if m and "(R)" in line:
            marked.add(m.group(1))
    assert marked == set(C.REVERSE_ITEMS), f"app (R) items {marked} != config {set(C.REVERSE_ITEMS)}"


def test_app_defines_three_conditions():
    cfg = (APP / "js" / "config.js").read_text()
    for c in C.CONDITIONS:
        assert c in cfg


# ---- runner -----------------------------------------------------------------
def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed, failed = 0, []
    for t in tests:
        try:
            t()
            passed += 1
            print(f"PASS  {t.__name__}")
        except Exception as e:
            failed.append(t.__name__)
            print(f"FAIL  {t.__name__}: {e}")
    print(f"\n{passed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
