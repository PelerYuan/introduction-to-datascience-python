#!/usr/bin/env python3
"""Locate the exact block where an English chapter and its translation differ in
paragraph count, using the SAME paragraph logic as verify_structure.py.

Usage:
    python diff_paragraphs.py --en .translation/source_en/X.md --zh source/X.md
"""
from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_structure as vs  # noqa: E402


def paras(path: Path) -> list[str]:
    return vs.structure(path.read_text(encoding="utf-8"))["paragraph_list"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--en", type=Path, required=True)
    ap.add_argument("--zh", type=Path, required=True)
    ap.add_argument("--context", type=int, default=2)
    args = ap.parse_args()

    a, b = paras(args.en), paras(args.zh)
    print(f"EN paragraphs {len(a)} | ZH paragraphs {len(b)}  (delta {len(b) - len(a):+d})")
    if len(a) == len(b):
        return 0

    # Align on a normalised key so re-wrapped/re-worded paragraphs still match.
    sm = difflib.SequenceMatcher(a=[p[:30] for p in a], b=[p[:30] for p in b], autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        print(f"\n=== {tag}: EN[{i1}:{i2}] -> ZH[{j1}:{j2}] ===")
        for k in range(max(0, i1 - args.context), min(len(a), i2 + args.context)):
            mark = "  " if i1 <= k < i2 else "  "
            print(f" {mark}EN[{k:>3}] {a[k][:130]!r}")
        print("  ----")
        for k in range(max(0, j1 - args.context), min(len(b), j2 + args.context)):
            print(f"   ZH[{k:>3}] {b[k][:130]!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())