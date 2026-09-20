#!/usr/bin/env python3
"""Quality gate on the *rendered* book, not the Markdown source.

The Markdown linter can only see the source. What a reader actually sees is the HTML,
and Markdown soft line breaks become spaces there. This script reads the built pages
and reports typographic defects that only exist after rendering:

  RENDERED_CJK_SPACE  a space between two Chinese characters or after Chinese
                      punctuation — the classic symptom of hard-wrapped Chinese prose
  RENDERED_LATIN_GAP  a missing space between Chinese and Latin script
  RAW_NUMREF          an unresolved {numref} that leaked into the page as literal text
  RAW_ROLE            an unresolved {glue}/{cite} role left as literal text
  LEAKED_MARKUP       a literal `{code-cell}`/`:::`/`+++` that should have been consumed

Usage:
    python html_qa.py [--dir source/_build/html] [--json out.json] [--max-show 8]
Exit code 0 = clean.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

# The report quotes Chinese text; force UTF-8 so a cp1252 console cannot turn a
# successful scan into a UnicodeEncodeError.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # pragma: no cover
        pass

ROOT = Path(__file__).resolve().parents[2]

PARA_RE = re.compile(r"<p\b[^>]*>(.*?)</p>", re.DOTALL | re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]+>")
CJK = r"\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff"
CJK_PUNCT = r"\u3000-\u303f\uff01-\uff0f\uff1a-\uff20\uff3b-\uff40\uff5b-\uff65\uffe0-\uffe6"
CJK_ANY = CJK + CJK_PUNCT

# A space between CJK characters, or a space *after* CJK punctuation followed by CJK.
CJK_SPACE_RE = re.compile(rf"[{CJK_ANY}][ \t]+[{CJK}]|[{CJK_PUNCT}][ \t]+[{CJK}]")
LATIN_GAP_RE = re.compile(rf"[{CJK}][A-Za-z0-9]|[A-Za-z0-9][{CJK}]")
RAW_NUMREF_RE = re.compile(r"\{numref\}`[^`]*`")
RAW_ROLE_RE = re.compile(r"\{(?:glue|cite|ref|eq|term|doc)[^}]*\}`[^`]*`")
LEAKED_MARKUP_RE = re.compile(r"\{code-cell\}|^:::$|\+\+\+", re.MULTILINE)


def para_texts(page: Path) -> list[str]:
    raw = page.read_text(encoding="utf-8", errors="replace")
    out = []
    for m in PARA_RE.finditer(raw):
        inner = m.group(1)
        inner = TAG_RE.sub("", inner)
        text = html.unescape(inner)
        # HTML authors wrap source lines; collapse every whitespace run to one space so
        # we measure what the browser renders, not how the file is laid out.
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            out.append(text)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", type=Path, default=ROOT / "source" / "_build" / "html")
    ap.add_argument("--json", type=Path, default=None)
    ap.add_argument("--max-show", type=int, default=8)
    args = ap.parse_args()

    if not args.dir.exists():
        print(f"no built HTML at {args.dir} - run tools/build_book.ps1 first")
        return 2

    pages = sorted(p for p in args.dir.glob("*.html")
                   if not p.name.startswith(("genindex", "search", "py-modindex")))
    findings: dict[str, list[dict]] = {}
    n_paras = 0

    for page in pages:
        for text in para_texts(page):
            n_paras += 1
            checks = [
                ("RENDERED_CJK_SPACE", CJK_SPACE_RE),
                ("RENDERED_LATIN_GAP", LATIN_GAP_RE),
                ("RAW_NUMREF", RAW_NUMREF_RE),
                ("RAW_ROLE", RAW_ROLE_RE),
                ("LEAKED_MARKUP", LEAKED_MARKUP_RE),
            ]
            for code, rx in checks:
                for m in rx.finditer(text):
                    s = max(0, m.start() - 45)
                    findings.setdefault(code, []).append({
                        "page": page.name,
                        "match": m.group(0),
                        "context": text[s:m.end() + 45],
                    })

    print(f"scanned {len(pages)} pages / {n_paras} rendered paragraphs")
    if not findings:
        print("OK   rendered book is clean")
        return 0

    total = sum(len(v) for v in findings.values())
    print(f"WARN {total} finding(s): "
          f"{ {k: len(v) for k, v in sorted(findings.items())} }")
    for code, items in sorted(findings.items()):
        print(f"\n[{code}] {len(items)}")
        for it in items[: args.max_show]:
            print(f"   {it['page']}: {it['match']!r}")
            print(f"      …{it['context']}…")
        if len(items) > args.max_show:
            print(f"   … and {len(items) - args.max_show} more")

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(
            {"pages": len(pages), "paragraphs": n_paras, "findings": findings},
            ensure_ascii=False, indent=2), encoding="utf-8")
    return 1


if __name__ == "__main__":
    sys.exit(main())