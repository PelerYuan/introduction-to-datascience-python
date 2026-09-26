"""Throwaway: show raw (repr) context around each [A-Za-z]:\\ match to tell JS escapes from paths."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HTML = ROOT / "source" / "_build" / "html"
RX = re.compile(r"[A-Za-z]:\\")

for p in sorted(HTML.glob("*.html")):
    t = p.read_text(encoding="utf-8", errors="replace")
    ms = list(RX.finditer(t))
    if not ms:
        continue
    print(f"### {p.name}: {len(ms)}")
    for m in ms:
        s = max(0, m.start() - 25)
        print("   ", repr(t[s:m.end() + 45]))