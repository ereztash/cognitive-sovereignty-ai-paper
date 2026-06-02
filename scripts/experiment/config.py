"""Shared configuration for the (SYNTHETIC) Cognitive Sovereignty experiment.

Everything this pipeline produces is generated under the pre-registered
assumptions in docs/preregistration_template.md. It is a DRY RUN of the analysis
on simulated data -- NOT empirical evidence. To obtain real findings, replace
results/experiment/synthetic_participants.csv with real data of the same schema
and re-run the analysis scripts.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results" / "experiment"
FIGURES = ROOT / "figures" / "experiment"
DATA = RESULTS / "synthetic_participants.csv"
RESULTS.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)

SEED = 20260602
N_PER_GROUP = 90                 # demo n for clean recovery of injected effects;
                                 # a real study's minimum is ~60/group for 80%
                                 # power on H1 (see scripts/power_analysis.py),
                                 # but moderation tests (H2/H4) need more.
CONDITIONS = ["No AI", "Uncalibrated AI", "Fortified AI"]
ALPHA = 0.05
N_PLANTED_ERRORS = 10

# CSS items mirror docs/cognitive_sovereignty_scale_v0.md
CSS_ITEMS = [f"css_{i:02d}" for i in range(1, 21)]
REVERSE_ITEMS = {"css_03", "css_04", "css_07", "css_11", "css_15", "css_19"}
FACETS = {
    "F1_monitoring":  ["css_01", "css_02", "css_03", "css_04"],
    "F2_evaluation":  ["css_05", "css_06", "css_07", "css_08"],
    "F3_agency":      ["css_09", "css_10", "css_11", "css_12"],
    "F4_internalize": ["css_13", "css_14", "css_15", "css_16"],
    "F5_calibration": ["css_17", "css_18", "css_19", "css_20"],
}
ITEM_LOADING = 0.70

# ---- Assumed effects (standardized vs No AI) -- edit to match pilot/lit ----
PERF_MEAN = {"No AI": 0.0, "Uncalibrated AI": 0.50, "Fortified AI": 0.60}
SOV_STATE = {"No AI": 0.0, "Uncalibrated AI": -0.60, "Fortified AI": 0.10}
TRANSFER_MEAN = {"No AI": 0.0, "Uncalibrated AI": -0.45, "Fortified AI": 0.00}
RECON_MEAN = {"No AI": 0.0, "Uncalibrated AI": -0.55, "Fortified AI": 0.05}
OFFLOAD = {"No AI": 0.0, "Uncalibrated AI": 0.85, "Fortified AI": 0.55}
MISCALIB_MEAN = {"No AI": 0.0, "Uncalibrated AI": 0.40, "Fortified AI": -0.10}

# H2 (retention): offloading hurts retention, buffered by metacog calibration.
RET_OFFLOAD_PENALTY = 0.70
RET_CALIB_BUFFER = 0.60           # offload x calibration interaction
RET_KNOWLEDGE = 0.10

# H4 (AI-error detection, AI arms only): knowledge buffers; gates substitute.
ERR_KNOWLEDGE = 0.45
ERR_FORTIFIED = 0.30
ERR_KNOWLEDGE_X_FORT = -0.20

NFC_SOV_PATH = 0.40               # convergent validity: trait sovereignty ~ NfC
ATTRITION_T2 = 0.12
ATTN_FAIL = 0.05
