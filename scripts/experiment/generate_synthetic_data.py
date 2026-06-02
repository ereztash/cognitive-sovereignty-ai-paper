"""Generate a SYNTHETIC participant dataset under the pre-registered assumptions.

This is simulated data for exercising the analysis pipeline -- not real people.
Schema matches what a real study (docs/preregistration_template.md) would yield,
so the same analysis scripts run unchanged on real data.
"""
import numpy as np
import pandas as pd
import config as C


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def main():
    rng = np.random.default_rng(C.SEED)
    rows = []
    pid = 0
    for cond in C.CONDITIONS:
        n = C.N_PER_GROUP
        nfc = rng.standard_normal(n)
        knowledge = rng.standard_normal(n)
        ai_lit = rng.standard_normal(n)
        trust = rng.standard_normal(n)
        calibration = rng.standard_normal(n)

        trait_sov = C.NFC_SOV_PATH * nfc + np.sqrt(1 - C.NFC_SOV_PATH ** 2) * rng.standard_normal(n)
        state_sov = trait_sov + C.SOV_STATE[cond] + 0.5 * rng.standard_normal(n)

        items = {}
        for it in C.CSS_ITEMS:
            lat = C.ITEM_LOADING * state_sov + np.sqrt(1 - C.ITEM_LOADING ** 2) * rng.standard_normal(n)
            resp = np.clip(np.round(3 + 1.1 * lat), 1, 5).astype(int)
            if it in C.REVERSE_ITEMS:           # store raw (reverse-keyed) responses
                resp = 6 - resp
            items[it] = resp

        performance = C.PERF_MEAN[cond] + rng.standard_normal(n)
        transfer = C.TRANSFER_MEAN[cond] + rng.standard_normal(n)
        reconstruction = C.RECON_MEAN[cond] + 0.2 * calibration + rng.standard_normal(n)
        miscalibration = C.MISCALIB_MEAN[cond] + rng.standard_normal(n)
        offload = C.OFFLOAD[cond]
        retention = (-C.RET_OFFLOAD_PENALTY * offload
                     + C.RET_CALIB_BUFFER * offload * calibration
                     + C.RET_KNOWLEDGE * knowledge
                     + rng.standard_normal(n))

        if cond == "No AI":                     # no AI errors to detect without AI
            err_det = np.full(n, np.nan)
        else:
            fort = 1.0 if cond == "Fortified AI" else 0.0
            lin = (C.ERR_KNOWLEDGE * knowledge + C.ERR_FORTIFIED * fort
                   + C.ERR_KNOWLEDGE_X_FORT * knowledge * fort + 0.5 * rng.standard_normal(n))
            err_det = rng.binomial(C.N_PLANTED_ERRORS, sigmoid(lin)) / C.N_PLANTED_ERRORS

        t2 = rng.random(n) > C.ATTRITION_T2
        attn = rng.random(n) > C.ATTN_FAIL

        for i in range(n):
            row = {
                "participant_id": pid, "condition": cond,
                "nfc_z": nfc[i], "knowledge_z": knowledge[i], "ai_literacy_z": ai_lit[i],
                "trust_z": trust[i], "calibration_z": calibration[i],
                "performance": performance[i],
                "ai_error_detection": err_det[i],
                "miscalibration": miscalibration[i],
                "retention": retention[i] if t2[i] else np.nan,
                "transfer": transfer[i] if t2[i] else np.nan,
                "reconstruction": reconstruction[i] if t2[i] else np.nan,
                "t2_complete": bool(t2[i]), "attn_pass": bool(attn[i]),
            }
            for it in C.CSS_ITEMS:
                row[it] = int(items[it][i])
            rows.append(row)
            pid += 1

    df = pd.DataFrame(rows)
    df.to_csv(C.DATA, index=False)
    print(f"Wrote {C.DATA}")
    print(f"  {len(df)} SYNTHETIC participants across {df['condition'].nunique()} arms; "
          f"T2 retained = {df['t2_complete'].mean():.0%}, attention-pass = {df['attn_pass'].mean():.0%}")


if __name__ == "__main__":
    main()
