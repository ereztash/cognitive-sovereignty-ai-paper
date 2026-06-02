from pathlib import Path
import re
import math
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "source_text.txt"
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

PLACEHOLDER = """
Metacognition enables task decomposition. Algorithmization externalizes parts of thinking.
Cognitive offloading can increase performance, but uncalibrated offloading may reduce critical thinking.
Fortified AI requires calibration, reflection, and human evaluation.
"""

LEXICONS = {
    "metacognition": ["מטא-קוגניציה", "מטא קוגניציה", "metacognition", "metacognitive", "סדר גבוה", "רפלקציה", "ניטור", "וויסות", "calibration", "reflection"],
    "algorithmization": ["אלגוריתם", "אלגוריתמיזציה", "חישוב", "computational", "algorithm", "code", "if-then", "machine"],
    "offloading": ["מיקור חוץ", "פריקת עומס", "offloading", "extended mind", "external", "delegation", "דלגציה"],
    "tacit_limits": ["ידע סמוי", "פולאני", "דרייפוס", "tacit", "embodied", "Polanyi", "Dreyfus", "אינטואיציה"],
    "cognitive_risk": ["תודעה חלולה", "מלכודת הריבונות", "ניוון", "תלות", "risk", "dependency", "critical thinking", "sovereignty"],
    "fortified_solution": ["תודעה מבוצרת", "כיול", "חשיבה חישובית", "fortified", "calibrated", "debugging", "explainability"],
}

def load_text():
    return DATA.read_text(encoding="utf-8", errors="ignore") if DATA.exists() else PLACEHOLDER

def chunk_text(text, chunk_size=700):
    clean = re.sub(r"\s+", " ", text).strip()
    return [clean[i:i + chunk_size].strip() for i in range(0, len(clean), chunk_size) if len(clean[i:i + chunk_size].strip()) > 50]

def count_terms(chunk, terms):
    total, hits = 0, []
    for term in terms:
        count = len(re.findall(re.escape(term), chunk, flags=re.IGNORECASE))
        if count:
            total += count
            hits.append(term)
    return total, sorted(set(hits))

def main():
    chunks = chunk_text(load_text())
    rows = []
    for idx, chunk in enumerate(chunks, start=1):
        row = {"chunk": idx, "chars": len(chunk)}
        for category, terms in LEXICONS.items():
            total, hits = count_terms(chunk, terms)
            row[category] = total
            row[f"{category}_hits"] = ", ".join(hits[:8])
        rows.append(row)
    df = pd.DataFrame(rows)
    category_cols = list(LEXICONS.keys())
    summary = pd.DataFrame({
        "category": category_cols,
        "total_mentions": [int(df[c].sum()) for c in category_cols],
        "chunks_with_category": [int((df[c] > 0).sum()) for c in category_cols],
        "coverage_rate": [round(float((df[c] > 0).mean()), 3) for c in category_cols],
    }).sort_values("total_mentions", ascending=False)
    cooc = pd.DataFrame(index=category_cols, columns=category_cols, dtype=int)
    for a in category_cols:
        for b in category_cols:
            cooc.loc[a, b] = int(((df[a] > 0) & (df[b] > 0)).sum())
    n = len(df)
    pmi_rows = []
    for i, a in enumerate(category_cols):
        for b in category_cols[i + 1:]:
            pab = (((df[a] > 0) & (df[b] > 0)).sum() + 0.5) / (n + 1)
            pa = ((df[a] > 0).sum() + 0.5) / (n + 1)
            pb = ((df[b] > 0).sum() + 0.5) / (n + 1)
            pmi_rows.append({"pair": f"{a} <-> {b}", "cooccurring_chunks": int(((df[a] > 0) & (df[b] > 0)).sum()), "pmi_smooth": round(math.log2(pab / (pa * pb)), 3)})
    summary.to_csv(RESULTS / "category_summary.csv", index=False, encoding="utf-8-sig")
    cooc.to_csv(RESULTS / "cooccurrence_matrix.csv", encoding="utf-8-sig")
    pd.DataFrame(pmi_rows).sort_values(["cooccurring_chunks", "pmi_smooth"], ascending=False).to_csv(RESULTS / "pairwise_associations.csv", index=False, encoding="utf-8-sig")
    df.to_csv(RESULTS / "chunk_level_coding.csv", index=False, encoding="utf-8-sig")
    print(summary.to_string(index=False))

if __name__ == "__main__":
    main()
