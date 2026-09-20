#!/usr/bin/env python3
"""Normalise Chinese typographic spacing in the Markdown sources.

Translators mirrored English spacing habits around emphasis, which is invisible in the
source but very visible once rendered:

    称为 **训练集**           -> renders as  称为 训练集
    （binary classification） 情形  -> renders as  （binary classification） 情形

Chinese needs no space between two Chinese characters, nor after Chinese punctuation,
so those spaces are removed. The pass is **markup-aware**: `**`/`*` emphasis markers are
treated as transparent when deciding whether two characters are adjacent, so
`称为 **训练集**` collapses to `称为**训练集**` while `使用 pandas 读取` keeps its space
(there a space is required).

Never touches fenced code, inline code, MyST roles, math, links, URLs or HTML tags.

Usage:
    python fix_spacing.py                 # report only
    python fix_spacing.py --apply
    python fix_spacing.py --chapters viz wrangling --apply
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from term_fix import protected_mask  # noqa: E402
from unwrap_cjk import _KINDS, fence_kind, label_kinds, numref_edges  # noqa: E402

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # pragma: no cover
        pass

FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")

IDEO = r"\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff"
CJK_PUNCT = r"\u3000-\u303f\uff01-\uff0f\uff1a-\uff20\uff3b-\uff40\uff5b-\uff65\uffe0-\uffe6"
CJK_ANY = IDEO + CJK_PUNCT
EMPH = r"(?:\*\*|\*|__|_)"

# CJK (＋optional emphasis marker) + spaces + (optional emphasis marker) + CJK ideograph
TIGHTEN_RE = re.compile(rf"([{CJK_ANY}])({EMPH}?)[ \t]+({EMPH}?)([{IDEO}])")

# A list marker that may prefix a run-in bold heading.
LIST_MARKER_RE = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)")
# `_config.yml` sets numfig_format figure: "图 %s", so a bare `{numref}`fig:...`` already
# renders as "图 8.1". Wording like "如图 {numref}`fig:8-1`" would render "如图 图 8.1".
# Custom-text numrefs (`{numref}`第 %s 章``) are left alone by the lookahead.
NUMREF_DUP_RE = re.compile(r"[图表](?=[ \t]*\{numref\}`(?:fig|tab):)")

# A Markdown link is one opaque token, so `参与 [《Data Science…》](url) 编写工作` hides its
# own Chinese boundaries: the link text is Chinese on both ends, and the spaces around it
# are spurious. The link text's first/last character decides, so a link whose text is
# English (`见 [pandas 文档](url)`) keeps its spaces.
LINK_TEXT = r"\[[^\]\n]*\]\([^)\n]*\)"
LINK_SPACE_BEFORE_RE = re.compile(rf"([{CJK_ANY}])[ \t]+(?=\[([{CJK_ANY}])[^\]\n]*\]\([^)\n]*\))")
LINK_SPACE_AFTER_RE = re.compile(
    rf"(?P<link>\[[^\]\n]*[{CJK_ANY}]\]\([^)\n]*\))[ \t]+(?=[{CJK_ANY}])"
)

# `{numref}` renders Chinese when its output starts with 图/表 or with the role's own
# custom text ("第 3 章", "5.8 节"), and a bare number when the custom text starts with
# `%s`. Which side needs tightening therefore depends on the individual role — see
# numref_edges() below.
NUMREF_ANY_RE = re.compile(r"\{numref\}`([^`]*)`")

# The opposite direction: a *missing* space between Chinese and Latin that is hidden by
# an emphasis marker. `使用**pandas**` renders "使用pandas" and `*运行 JupyterLab*的说明`
# renders "运行 JupyterLab的说明" — both violate the style guide's CJK↔Latin spacing rule.
# The space goes *outside* the span in each case: before an opening marker, after a
# closing one, so the emphasis covers only the intended characters.
#
# Only ideographs count as the Chinese side: full-width punctuation must stay tight, so
# `（*Data Science…*）` — an italic English title inside Chinese brackets — keeps its
# shape instead of becoming `（* Data Science…* ）`.
CJK_EMPH_LATIN_RE = re.compile(rf"([{IDEO}])({EMPH})([A-Za-z0-9])")
LATIN_EMPH_CJK_RE = re.compile(rf"([A-Za-z0-9])({EMPH})([{IDEO}])")
# A bare `{numref}`fig:x`` renders "图 5.1" and therefore ends in a digit, so it needs
# the CJK↔Latin space before following Chinese: "图 5.1中" -> "图 5.1 中". Only an
# ideograph triggers this — full-width punctuation must stay tight, so "（{numref}`x`）"
# must not become "（图 5.1 ）".
BARE_NUMREF_TIGHT_RE = re.compile(
    rf"(\{{numref\}}`(?![^`]*%s)[^`]*`)([{IDEO}])"
)
# A whole emphasis span, e.g. `**安装**` — the shape of a run-in bold heading.
RUN_IN_RE = re.compile(r"(?:\*\*[^*\n]+\*\*|\*[^*\n]+\*|__[^_\n]+__|_[^_\n]+_)")


def is_run_in_heading(line: str, m: re.Match) -> bool:
    """Deprecated: the space after a run-in bold label is *also* removed.

    Keeping it was tried and reverted. A Chinese run-in label is already delimited by its
    bold formatting, so `**安装** 要在 Windows 上安装 Docker` reads with a spurious gap;
    `**安装**要在 Windows 上安装 Docker` is the correct rendering, and the label's own
    colon (when present) is punctuation, which the join preserves.
    """
    return False

CHAPTERS = [
    "index", "preface-text", "foreword-text", "acknowledgements", "authors",
    "intro", "reading", "wrangling", "viz", "classification1", "classification2",
    "regression1", "regression2", "clustering", "inference", "jupyter",
    "version-control", "setup",
]


def tighten_line(line: str) -> tuple[str, list[str]]:
    mask = protected_mask(line)
    out: list[str] = []
    hits: list[str] = []
    i = 0
    while True:
        m = TIGHTEN_RE.search(line, i)
        if not m:
            out.append(line[i:])
            break
        if any(mask[m.start():m.end()]):
            out.append(line[i:m.end()])
            i = m.end()
            continue
        if is_run_in_heading(line, m):
            out.append(line[i:m.end()])
            i = m.end()
            continue
        out.append(line[i:m.start()])
        out.append(m.group(1) + m.group(2) + m.group(3) + m.group(4))
        hits.append(line[m.start():m.end()])
        i = m.end()
    return "".join(out), hits


def tighten_link_spacing(line: str) -> tuple[str, list[str]]:
    """Drop spaces hugging a Markdown link whose text is Chinese on that side."""
    mask = protected_mask(line)
    hits: list[str] = []

    def sub(rx: re.Pattern, template: str, text: str) -> str:
        out, i = [], 0
        while True:
            m = rx.search(text, i)
            if not m:
                out.append(text[i:])
                break
            out.append(text[i:m.start()])
            # The spaces we edit sit outside the link, so only they must be unprotected.
            # For LINK_SPACE_AFTER_RE the match *starts* with the (protected) link, so
            # testing group 0 would veto every repair; test the trailing gap instead.
            span = (m.end("link"), m.end()) if "link" in (m.groupdict() or {}) \
                else (m.start(), m.end())
            if any(mask[span[0]:span[1]]):
                out.append(m.group(0))
            else:
                hits.append(m.group(0))
                out.append(m.expand(template))
            i = m.end()
        return "".join(out)

    line = sub(LINK_SPACE_BEFORE_RE, r"\1", line)
    line = sub(LINK_SPACE_AFTER_RE, r"\g<link>", line)
    return line, hits


def tighten_numref_spacing(line: str) -> tuple[str, list[str]]:
    """Normalise the spaces on both sides of every `{numref}`, per side.

    Each side has two possible defects, and which one applies depends on what that side
    of the role renders:

    * CJK edge  -> a space there is spurious, so remove any that is present.
    * digit edge -> CJK↔Latin, so a space is *required*; insert one if missing
      (`第 5 章和6` -> `第 5 章和 6`).

    Only ideographs count on the far side, so `（{numref}`x`）` keeps tight punctuation.
    """
    hits: list[str] = []
    # Matches must be applied right-to-left: the loop rewrites `line` as it goes, so
    # spans computed on the original string would be stale for any match to the *right*
    # of an edit — which silently deletes whatever happened to sit at those indices.
    # Going backwards keeps every not-yet-processed span (they are all further left)
    # valid.
    for m in reversed(list(NUMREF_ANY_RE.finditer(line))):
        start, end = m.span()
        head_cjk, tail_cjk = numref_edges(m.group(1))

        # ---- before the role -------------------------------------------------
        j = start
        while j > 0 and line[j - 1] in " \t":
            j -= 1
        gap = start - j
        prev = line[j - 1] if j > 0 else ""
        if prev and re.match(f"[{CJK_ANY}]", prev):
            if head_cjk and gap:
                hits.append(line[j:start])
                line = line[:j] + line[start:]
                end -= gap
                start = j
            elif not head_cjk and not gap and re.match(f"[{IDEO}]", prev):
                hits.append(prev + " ")
                line = line[:j] + " " + line[j:]
                start += 1
                end += 1

        # ---- after the role --------------------------------------------------
        k = end
        while k < len(line) and line[k] in " \t":
            k += 1
        gap = k - end
        nxt = line[k] if k < len(line) else ""
        if nxt and re.match(f"[{IDEO}]", nxt):
            if tail_cjk and gap:
                hits.append(line[end:k])
                line = line[:end] + line[k:]
            elif not tail_cjk and not gap:
                hits.append(" " + nxt)
                line = line[:end] + " " + line[end:]

    return line, hits


def add_cjk_latin_spaces(line: str) -> tuple[str, list[str]]:
    """Insert the CJK↔Latin space that an emphasis marker is currently hiding."""
    mask = protected_mask(line)
    hits: list[str] = []

    def sub(rx: re.Pattern, template: str, text: str, protect_group: int = 0) -> str:
        out, i = [], 0
        while True:
            m = rx.search(text, i)
            if not m:
                out.append(text[i:])
                break
            out.append(text[i:m.start()])
            # BARE_NUMREF_TIGHT_RE starts with the (protected) role, so only the CJK
            # character it captured is tested — otherwise the repair never fires.
            ps, pe = m.span(protect_group) if protect_group else (m.start(), m.end())
            if any(mask[ps:pe]):
                out.append(m.group(0))
            else:
                hits.append(m.group(0))
                out.append(m.expand(template))
            i = m.end()
        return "".join(out)

    line = sub(CJK_EMPH_LATIN_RE, r"\1 \2\3", line)
    line = sub(LATIN_EMPH_CJK_RE, r"\1\2 \3", line)
    return line, hits


def drop_duplicate_numref_prefix(line: str) -> tuple[str, list[str]]:
    """Remove a literal 图/表 that would double the one `numfig_format` already adds."""
    mask = protected_mask(line)
    out, hits, i = [], [], 0
    while True:
        m = NUMREF_DUP_RE.search(line, i)
        if not m:
            out.append(line[i:])
            break
        out.append(line[i:m.start()])
        if not mask[m.start()]:
            hits.append(m.group(0))
            i = m.end()
        else:  # pragma: no cover - 图/表 is never itself a protected token
            out.append(m.group(0))
            i = m.end()
    return "".join(out), hits


def process(path: Path, apply: bool, show: int, context: int) -> int:
    raw = path.read_text(encoding="utf-8")
    newline = "\r\n" if raw.count("\r\n") > raw.count("\n") / 2 else "\n"
    lines = raw.replace("\r\n", "\n").split("\n")
    _KINDS.clear()
    _KINDS.update(label_kinds("\n".join(lines)))
    in_fence = False
    fence_char = ""
    fence = ""            # "" | "code" | "prose"
    total = 0
    shown = 0
    for i, line in enumerate(lines):
        fm = FENCE_RE.match(line)
        if fm:
            if not fence:
                fence_char = fm.group(2)[0]
                fence = fence_kind(fm.group(3))
            elif fm.group(2)[0] == fence_char:
                fence, fence_char = "", ""
            continue
        if fence == "code":
            continue
        fixed, hits = tighten_line(line)
        if hits:
            total += len(hits)
            if shown < show:
                print(f"  {path.name}:{i + 1}  {', '.join(repr(h) for h in hits[:4])}")
                for c in range(max(0, i - context), min(len(lines), i + context + 1)):
                    print(f"     {'>>' if c == i else '  '} {lines[c][:140]}")
                shown += 1
            lines[i] = fixed
        deduped, dhits = drop_duplicate_numref_prefix(lines[i])
        if dhits:
            total += len(dhits)
            print(f"  {path.name}:{i + 1}  duplicate numref prefix {dhits!r}")
            lines[i] = deduped
        tightened, thits = tighten_numref_spacing(lines[i])
        if thits:
            total += len(thits)
            if shown < show:
                print(f"  {path.name}:{i + 1}  numref spacing {thits[:3]!r}")
                print(f"     >> {lines[i][:150]}")
            lines[i] = tightened
        linked, lhits = tighten_link_spacing(lines[i])
        if lhits:
            total += len(lhits)
            if shown < show:
                print(f"  {path.name}:{i + 1}  link spacing {lhits[:3]!r}")
                print(f"     >> {lines[i][:150]}")
            lines[i] = linked
        spaced, ghits = add_cjk_latin_spaces(lines[i])
        if ghits:
            total += len(ghits)
            if shown < show:
                print(f"  {path.name}:{i + 1}  missing CJK/Latin space {ghits[:3]!r}")
                print(f"     >> {lines[i][:150]}")
            lines[i] = spaced
    if apply and total:
        path.write_bytes(("\n".join(lines)).replace("\n", newline).encode("utf-8"))
    return total


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--show", type=int, default=3, help="how many sample lines per chapter")
    ap.add_argument("--context", type=int, default=0)
    ap.add_argument("chapters", nargs="*", default=None)
    args = ap.parse_args()

    grand = 0
    for ch in (args.chapters or CHAPTERS):
        p = ROOT / "source" / f"{ch}.md"
        if not p.exists():
            continue
        n = process(p, args.apply, args.show, args.context)
        if n:
            print(f"[{ch}] {n} over-spaced join(s)")
            grand += n
    print(f"\n{'applied' if args.apply else 'would tighten'} {grand} join(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())