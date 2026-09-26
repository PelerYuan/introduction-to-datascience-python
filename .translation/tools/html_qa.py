#!/usr/bin/env python3
r"""Quality gate on the *rendered* book, not the Markdown source.

The Markdown linter can only see the source. What a reader actually sees is the HTML,
and Markdown soft line breaks become spaces there. This script reads the built pages
and reports typographic defects that only exist after rendering:

  RENDERED_CJK_SPACE  a space between two Chinese characters or after Chinese
                      punctuation — the classic symptom of hard-wrapped Chinese prose
  RENDERED_LATIN_GAP  a missing space between Chinese and Latin script
  RAW_NUMREF          an unresolved {numref} that leaked into the page as literal text
  RAW_ROLE            an unresolved {glue}/{cite} role left as literal text
  LEAKED_MARKUP       a literal `{code-cell}`/`:::`/`+++` that should have been consumed
  RENDERED_IMPORTERROR  an ImportError/ModuleNotFoundError pasted into the page, which is
                      how a missing dependency (pyarrow, ibis sqlite) hides: the chart
                      simply does not render and an error output takes its place
  RENDERED_WARNING    a pandas/numpy warning from a library newer than the book's
  RENDERED_PATH       the builder's own filesystem (C:\Users\..., /home/jovyan, ipykernel_N)
  RENDERED_EMPHASIS   a `*`/`_` that failed to close and shows up literally in the prose
  MISSING_CHARTS      fewer than VEGA_MIN rendered Altair charts book-wide

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
# Chart output carries kilobytes of JavaScript (vega and plotly both embed their runtime),
# and that code is full of `_`-prefixed identifiers such as `n._width`. Once charts render
# it lands inside the paragraph scan and produced 25,594 bogus emphasis findings, so script
# and style bodies are removed before paragraphs are collected. `MISSING_CHARTS` still
# counts the chart calls: it reads the raw page, not this reduced copy.
SCRIPT_STYLE_RE = re.compile(r"<(script|style)\b.*?</\1\s*>", re.DOTALL | re.IGNORECASE)
INLINE_CODE_RE = re.compile(r"<code\b[^>]*>.*?</code\s*>", re.DOTALL | re.IGNORECASE)
RENDERED_MATH_RE = re.compile(r"\\\(.*?\\\)|\\\[.*?\\\]|\$\$.*?\$\$", re.DOTALL)
CJK = r"\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff"
CJK_PUNCT = r"\u3000-\u303f\uff01-\uff0f\uff1a-\uff20\uff3b-\uff40\uff5b-\uff65\uffe0-\uffe6"
CJK_ANY = CJK + CJK_PUNCT

# A space between CJK characters, or a space *after* CJK punctuation followed by CJK.
CJK_SPACE_RE = re.compile(rf"[{CJK_ANY}][ \t]+[{CJK}]|[{CJK_PUNCT}][ \t]+[{CJK}]")
LATIN_GAP_RE = re.compile(rf"[{CJK}][A-Za-z0-9]|[A-Za-z0-9][{CJK}]")
RAW_NUMREF_RE = re.compile(r"\{numref\}`[^`]*`")
RAW_ROLE_RE = re.compile(r"\{(?:glue|cite|ref|eq|term|doc)[^}]*\}`[^`]*`")
LEAKED_MARKUP_RE = re.compile(r"\{code-cell\}|^:::$|\+\+\+", re.MULTILINE)

# --- Rendering checks ---------------------------------------------------------------
# The checks above only look at prose and references. A page can pass every one of them
# while every single chart is missing, because a chart that fails to execute renders as
# an *error output* rather than as prose. These four close that gap; each one is the
# direct rendered symptom of a class of build failure this book actually suffered.
#
# The dependency failures (missing pyarrow, missing ibis sqlite) surfaced as ImportError
# tracebacks pasted into the page, so that is what we look for rather than a chart count.
RENDERED_IMPORTERROR_RE = re.compile(r"(?:ImportError|ModuleNotFoundError)\b")
# pandas/numpy warnings brought in by library versions newer than the book's.
#
# Matched only in the form a leaked warning actually takes — `.../1234.py:2: FutureWarning:`
# — because the book *names* some of these warnings on purpose ("如果你看到
# SettingWithCopyWarning，只要……"), and a bare name match flags that prose forever.
RENDERED_WARNING_RE = re.compile(
    r"\.py:\d+:\s*(?:Future|Deprecation|SettingWithCopy|Parser|User|Runtime)Warning\b")
# The builder's own filesystem, leaked through a warning or a traceback.
#
# Deliberately narrow. `/home/jovyan/work` and `C:\Users\...` are paths the book tells the
# reader to type into the Docker dialog, so only the builder's temp execution directory and
# the notebook server's own filenames count as leaks.
RENDERED_PATH_RE = re.compile(r"ipykernel_\d+|[A-Za-z]:\\+Users\\+[^\s]*\\+AppData\\+|"
                              r"_build[\\/]+jupyter_execute")
# Leaked emphasis, measured on the rendered text. A run only counts as leaked when a word
# character follows it: leaked emphasis is always followed by the text it failed to wrap
# (`**汇总：**计算`), whereas the book also *names* the underscore character in prose
# (`下划线（_）`), where punctuation follows and nothing is wrong. `*args`/`**kwargs` are real
# Python syntax that appears in prose, so they are excluded rather than reported forever.
RENDERED_EMPHASIS_RE = re.compile(
    r"(?<![\w\\])(\*{1,3}|_{1,3})(?=\w)(?!\s*(?:args|kwargs)\b)")

# A rendered Altair chart leaves a `vegaEmbed(` call behind; a failed one leaves nothing.
VEGA_RE = re.compile(r"vegaEmbed\(")
# The English book renders 84 of them, so anything far below that is a regression.
VEGA_MIN = 80

# Plotly is rendered through its own mime type, and myst-nb has no handler for
# `application/vnd.plotly.v1+json` at all — plotly only reaches the page because the
# notebook renderer *also* emits a `text/html` bundle holding the plotly.js bootstrap.
# Plotly 7 drops that fallback, so the three 3-D scatter plots silently vanished while
# every text-based check still passed.
PLOTLY_RE = re.compile(r"Plotly\.newPlot|plotly-graph-div|cdn\.plot\.ly/plotly-[\d.]")
PLOTLY_MIN = 3


def para_texts(page: Path) -> list[str]:
    raw = page.read_text(encoding="utf-8", errors="replace")
    raw = SCRIPT_STYLE_RE.sub(" ", raw)
    out = []
    for m in PARA_RE.finditer(raw):
        inner = m.group(1)
        # Inline code and math are replaced by a single latin sentinel, not by a space and
        # not by nothing:
        #   * deleting them leaves `使用 在` where the page says `使用 sklearn 在`, which
        #     matches the CJK-space rule and invented 1440 findings;
        #   * blanking them with a space does the same thing.
        # A latin sentinel is also the honest representation: inline code IS latin content,
        # so the CJK/latin spacing rules should still see something between the characters.
        inner = INLINE_CODE_RE.sub("X", inner)
        inner = TAG_RE.sub("", inner)
        text = html.unescape(inner)
        # Math reaches the page as MathJax delimiters (`\(\hat{y}_i\)`); its subscripts are
        # not emphasis and its spacing is not the book's typography.
        text = RENDERED_MATH_RE.sub("X", text)
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
    vega_total = 0
    vega_pages: dict[str, int] = {}
    plotly_total = 0

    for page in pages:
        blob = page.read_text(encoding="utf-8", errors="replace")
        n_vega = len(VEGA_RE.findall(blob))
        vega_total += n_vega
        if n_vega:
            vega_pages[page.name] = n_vega
        plotly_total += len(PLOTLY_RE.findall(blob))
        for text in para_texts(page):
            n_paras += 1
            checks = [
                ("RENDERED_CJK_SPACE", CJK_SPACE_RE),
                ("RENDERED_LATIN_GAP", LATIN_GAP_RE),
                ("RAW_NUMREF", RAW_NUMREF_RE),
                ("RAW_ROLE", RAW_ROLE_RE),
                ("LEAKED_MARKUP", LEAKED_MARKUP_RE),
                ("RENDERED_IMPORTERROR", RENDERED_IMPORTERROR_RE),
                ("RENDERED_WARNING", RENDERED_WARNING_RE),
                ("RENDERED_PATH", RENDERED_PATH_RE),
                ("RENDERED_EMPHASIS", RENDERED_EMPHASIS_RE),
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
    print(f"rendered Altair charts (vegaEmbed calls): {vega_total} on {len(vega_pages)} pages")
    print(f"rendered Plotly charts: {plotly_total}")
    # A chart that never rendered is invisible to every text-based check, so these counts
    # are asserted rather than merely reported.
    if vega_total < VEGA_MIN:
        findings.setdefault("MISSING_CHARTS", []).append({
            "page": "(book-wide)",
            "match": f"{vega_total} vegaEmbed calls",
            "context": f"expected at least {VEGA_MIN} rendered Altair charts",
        })
    if plotly_total < PLOTLY_MIN:
        findings.setdefault("MISSING_CHARTS", []).append({
            "page": "(book-wide)",
            "match": f"{plotly_total} plotly embeds",
            "context": f"expected at least {PLOTLY_MIN} rendered Plotly charts",
        })

    # The report is written before any early return. Writing it only when findings exist
    # would leave the *previous* run's report on disk after a clean run, so the artifact
    # would claim defects that are no longer there — a stale green light is worse than
    # no report at all.
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(
            {"pages": len(pages), "paragraphs": n_paras, "vega_embed_total": vega_total,
             "plotly_total": plotly_total,
             "vega_embed_pages": vega_pages, "findings": findings},
            ensure_ascii=False, indent=2), encoding="utf-8")

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
    return 1


if __name__ == "__main__":
    sys.exit(main())