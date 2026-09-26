"""Throwaway: where does 'Translation' appear in the pages flagged by the byte scan?"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HTML = ROOT / "source" / "_build" / "html"

for name in ["classification1.html", "regression1.html", "reading.html", "index.html"]:
    t = (HTML / name).read_text(encoding="utf-8", errors="replace")
    print(f"### {name}")
    for m in list(re.finditer(r"Translation", t))[:10]:
        s = max(0, m.start() - 80)
        print("   ", repr(t[s:m.end() + 80]))
    print()