#!/usr/bin/env python3
"""Apply cross-chapter terminology unification, touching prose only.

Replacements never reach inside fenced code, inline code spans, MyST roles, math,
URLs or HTML tags, because those are structural and must stay byte-identical.

Usage:
    python term_fix.py --map "凹陷度=凹度" "光滑度=平滑度" [--apply] [--context 1]
    python term_fix.py --map-file .translation/tools/term_fix_map.txt --apply
    python term_fix.py --show "k-means"        # inspect occurrences without changing
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")

# Spans that must never be edited (order matters: multi-char forms first)
#
# The URL rule cannot use `\S+`: Chinese prose has no spaces, so `\S+` would run from the
# URL straight through the rest of the sentence up to the next space — masking whole
# sentences and silently vetoing every spacing fix after any link. A URL ends where CJK
# begins, which is exactly what the character class below encodes.
_CJK_RANGE = r"\u3000-\u303f\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff00-\uffef"
PROTECTED = [
    re.compile(r"\{[a-z]+(?::[a-z]+)?\}`[^`]*`"),   # MyST roles
    re.compile(r"``[^`]*``|`[^`\n]+`"),              # inline code
    re.compile(r"\$\$[^$]*\$\$|\$[^$\n]*\$"),        # math
    re.compile(r"!\[[^\]]*\]\([^)]*\)"),             # images
    re.compile(r"\[[^\]]*\]\([^)\s]+[^)]*\)"),       # links
    re.compile(r"<[^>]+>"),                          # html tags
    re.compile(rf"https?://[^\s{_CJK_RANGE}]+"),     # bare urls (stop at CJK)
]

CHAPTERS = [
    "index", "preface-text", "foreword-text", "acknowledgements", "authors",
    "intro", "reading", "wrangling", "viz", "classification1", "classification2",
    "regression1", "regression2", "clustering", "inference", "jupyter",
    "version-control", "setup",
]


def protected_mask(line: str) -> list[bool]:
    """True where the character is inside a protected span."""
    mask = [False] * len(line)
    for rx in PROTECTED:
        for m in rx.finditer(line):
            for i in range(m.start(), m.end()):
                mask[i] = True
    return mask


CJK_IDEO = r"\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff"
CJK_SPACE_RE = re.compile(rf"([{CJK_IDEO}])[ \t]+([{CJK_IDEO}])")


def collapse_cjk_space(line: str) -> str:
    """Delete spaces between two Chinese characters (never correct in Chinese)."""
    mask = protected_mask(line)
    out: list[str] = []
    i = 0
    while True:
        m = CJK_SPACE_RE.search(line, i)
        if not m:
            out.append(line[i:])
            break
        if any(mask[m.start():m.end()]):
            out.append(line[i:m.end()])
            i = m.end()
            continue
        out.append(line[i:m.start()])
        out.append(m.group(1) + m.group(2))
        i = m.end()
    return "".join(out)


def restore(line: str, shields: list[tuple[str, str]]) -> str:
    for ph, span in shields:
        line = line.replace(ph, span)
    return line


def fix_line(line: str, mapping: list[tuple[str, str]]) -> tuple[str, list[tuple[str, str]]]:
    mask = protected_mask(line)
    hits: list[tuple[str, str]] = []
    for old, new in mapping:
        if old not in line:
            continue
        out = []
        i = 0
        while True:
            j = line.find(old, i)
            if j < 0:
                out.append(line[i:])
                break
            if any(mask[j:j + len(old)]):
                out.append(line[i:j + len(old)])
                i = j + len(old)
                continue
            out.append(line[i:j])
            out.append(new)
            hits.append((old, new))
            i = j + len(old)
        line = "".join(out)
    return line, hits


def process(path: Path, mapping: list[tuple[str, str]], apply: bool,
            context: int, protect: list[str] | None = None, collapse: bool = False) -> int:
    protect = protect or []
    raw = path.read_text(encoding="utf-8")
    newline = "\r\n" if raw.count("\r\n") > raw.count("\n") / 2 else "\n"
    lines = raw.replace("\r\n", "\n").split("\n")
    total = 0
    in_fence = False
    fence_char = ""
    for i, line in enumerate(lines):
        # Shield spans that must survive the mapping untouched (e.g. an English
        # gloss inside parentheses). Placeholders are restored after fixing.
        shields: list[tuple[str, str]] = []
        for k, span in enumerate(protect):
            if span and span in line:
                ph = f"\x01{k}\x01"
                line = line.replace(span, ph)
                shields.append((ph, span))

        m = FENCE_RE.match(line)
        if m:
            if not in_fence:
                in_fence, fence_char = True, m.group(2)[0]
            elif m.group(2)[0] == fence_char:
                in_fence = False
            lines[i] = restore(line, shields)
            continue
        if in_fence:
            lines[i] = restore(line, shields)
            continue
        fixed, hits = fix_line(line, mapping)
        if collapse:
            collapsed = collapse_cjk_space(fixed)
            if collapsed != fixed:
                hits = hits + [(" ", "")]
                fixed = collapsed
        fixed = restore(fixed, shields)
        lines[i] = fixed
        if hits:
            total += len(hits)
            print(f"  {path.name}:{i + 1}  " + ", ".join(f"{a}->{b}" for a, b in hits))
            for c in range(max(0, i - context), min(len(lines), i + context + 1)):
                mark = ">>" if c == i else "  "
                print(f"     {mark} {lines[c][:150]}")
            lines[i] = fixed
    if apply and total:
        path.write_bytes(("\n".join(lines)).replace("\n", newline).encode("utf-8"))
    return total


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", nargs="*", default=[], help='"old=new" pairs')
    ap.add_argument("--map-file", type=Path, default=None)
    ap.add_argument("--show", default=None, help="just report occurrences of a string")
    ap.add_argument("--protect", nargs="*", default=[],
                    help="literal spans to leave untouched (e.g. an English gloss)")
    ap.add_argument("--collapse-cjk-space", action="store_true",
                    help="also delete spaces between two Chinese characters")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--context", type=int, default=0)
    ap.add_argument("chapters", nargs="*", default=None)
    args = ap.parse_args()

    pairs: list[tuple[str, str]] = []
    if args.map_file and args.map_file.exists():
        for line in args.map_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                a, b = line.split("=", 1)
                pairs.append((a.strip(), b.strip()))
    for spec in args.map:
        a, b = spec.split("=", 1)
        pairs.append((a, b))
    if args.show:
        pairs = [(args.show, "«SHOW»")]

    chapters = args.chapters or CHAPTERS
    grand = 0
    for ch in chapters:
        p = ROOT / "source" / f"{ch}.md"
        if not p.exists():
            continue
        n = process(p, pairs, args.apply, args.context, args.protect, args.collapse_cjk_space)
        if n:
            print(f"[{ch}] {n} occurrence(s)")
            grand += n
    verb = "replaced" if args.apply else "would replace"
    print(f"\n{verb} {grand} occurrence(s) across {len(chapters)} chapter(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())