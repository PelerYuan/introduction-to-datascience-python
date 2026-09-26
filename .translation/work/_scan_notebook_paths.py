"""Throwaway: inventory of machine-local path strings inside the executed notebooks.

The notebooks under _build/jupyter_execute are what the *next* rebuild turns into HTML,
so they are the best evidence of what the sanitizer must be able to rewrite.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXEC = ROOT / "source" / "_build" / "jupyter_execute"

PATH_RX = re.compile(
    r"(?:[A-Za-z]:[\\/][^\s\"'<>|:*?\r\n]*)"          # windows absolute
    r"|(?:/(?:tmp|home|opt|Users)/[^\s\"'<>|:*?\r\n]*)",  # posix absolute
)
seen: dict[str, set[str]] = {}
for p in sorted(EXEC.glob("*.ipynb")):
    t = p.read_text(encoding="utf-8", errors="replace")
    found = set()
    for m in PATH_RX.finditer(t):
        found.add(m.group(0))
    if found:
        seen[p.name] = found

for name, found in seen.items():
    print(f"### {name}")
    # collapse the noise: show only paths that mention machine-local markers
    for f in sorted(found):
        print("   ", f[:160])