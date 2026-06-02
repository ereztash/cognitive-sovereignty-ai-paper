import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
for script in [ROOT / "scripts" / "analyze_text_structure.py", ROOT / "scripts" / "simulate_cognitive_sovereignty.py"]:
    print(f"Running {script.name}...")
    subprocess.run([sys.executable, str(script)], check=True)
print("Done.")
