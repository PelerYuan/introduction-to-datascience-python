"""Throwaway: full (unescaped) machine-local paths found in the executed notebooks."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXEC = ROOT / "source" / "_build" / "jupyter_execute"

RX = re.compile(r"(?:[A-Za-z]:\\)[^\s\"'<>|:*?\r\n]*")

def walk(o, out):
    if isinstance(o, str):
        for m in RX.finditer(o):
            out.add(m.group(0))
    elif isinstance(o, list):
        for i in o:
            walk(i, out)
    elif isinstance(o, dict):
        for v in o.values():
            walk(v, out)

for p in sorted(EXEC.glob("*.ipynb")):
    try:
        nb = json.loads(p.read_text(encoding="utf-8", errors="replace"))
    except Exception as exc:
        print(f"### {p.name}: unreadable {exc}")
        continue
    out: set[str] = set()
    walk(nb, out)
    out = {s for s in out if re.search(r"AppData|venv-build|jupyter_execute|Translation|site-packages", s)}
    if out:
        print(f"### {p.name}: {len(out)} distinct")
        for s in sorted(out):
            print("   ", s)