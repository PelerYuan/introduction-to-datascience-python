"""Throwaway: which build artifacts hold the leaked strings at 8-bit level?"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "source" / "_build"

NEEDLES = [b"AppData", b"ipykernel_54168", b"xle6s8", b"oziGhf", b"ipykernel_38652",
           b"peler", b"site-packages", b"Translation", b"jupyter_execute"]

for p in sorted(BUILD.rglob("*")):
    if not p.is_file():
        continue
    try:
        b = p.read_bytes()
    except OSError:
        continue
    hits = {n.decode(): b.count(n) for n in NEEDLES if n in b}
    if hits:
        print(f"{p.relative_to(BUILD)}  {hits}")