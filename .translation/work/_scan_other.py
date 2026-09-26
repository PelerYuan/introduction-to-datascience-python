"""Throwaway: what local-path strings live in the published non-HTML artifacts?"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HTML = ROOT / "source" / "_build" / "html"

PATS = {
    "appdata": re.compile(r"AppData", re.I),
    "win_drive": re.compile(r"[A-Za-z]:\\[^\\\s\"'<>|:*?]+(?:\\[^\\\s\"'<>|:*?]+)+"),
    "users_mac": re.compile(r"(?i:/Users/[^/\s\"'<>]+/)"),
    "venv": re.compile(r"\.venv-build", re.I),
    "jexec": re.compile(r"jupyter_execute", re.I),
    "repo_root": re.compile(re.escape(str(ROOT)), re.I),
    "temp": re.compile(r"(?i)Temp[\\/]"),
}

for name in ["searchindex.js", "objects.inv", ".buildinfo"]:
    p = HTML / name
    if not p.exists():
        continue
    t = p.read_text(encoding="utf-8", errors="replace")
    print(f"### {name}  ({p.stat().st_size} bytes)")
    for k, rx in PATS.items():
        for m in list(rx.finditer(t))[:4]:
            s = max(0, m.start() - 90)
            print(f"   [{k}] {t[s:m.end() + 90]!r}")

print("### _sources")
for p in sorted((HTML / "_sources").iterdir()):
    print("   ", p.name, p.stat().st_size)