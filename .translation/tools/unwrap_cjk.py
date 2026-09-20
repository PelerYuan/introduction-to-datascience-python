#!/usr/bin/env python3
"""Remove spurious spaces from hard-wrapped Chinese paragraphs.

The English source hard-wraps prose, and translators mirrored that wrapping. In
CommonMark a soft line break inside a paragraph renders as a *space*, so a wrapped
Chinese paragraph would display with stray spaces at every wrap point — an obvious
typographic defect in Chinese text. English needs those spaces; Chinese does not.

This pass joins the lines of a prose paragraph with "" exactly when correct Chinese
typography calls for no space, and leaves the line break (which renders as a space)
wherever Latin script needs one.

Structural lines are classified first and never merged, in either direction:
fenced blocks (code cells and directives), display math (`$$…$$`), HTML comments,
headings, `+++` separators, `(label)=` targets, list-item openers and table rows.

Usage:
    python unwrap_cjk.py --path source/wrangling.md [--check]
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

# Directives whose bodies are prose (note bodies, figure captions, table cells) rather
# than code. Everything else opened by a fence is treated as opaque code.
PROSE_DIRECTIVES = {
    "note", "tip", "warning", "important", "caution", "seealso", "epigraph", "figure",
    "table", "list-table", "index", "admonition", "dropdown", "margin", "sidebar",
    "exercise", "solution", "bibliography", "glossary", "tableofcontents", "include",
}
FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")
DIRECTIVEISH_RE = re.compile(r"^\s*(?::|\||\.\.\.)")
# A `{...}` at the start of a line is only a block opener when it names a real
# directive. `{numref}`x`` and `{glue:text}`x`` starting a wrapped line are ordinary
# prose continuations and must stay mergeable.
BLOCK_DIRECTIVE_RE = re.compile(
    r"^\s*\{(?:index|figure|table|list-table|code-cell|code-block|note|tip|warning|"
    r"important|caution|seealso|epigraph|dropdown|margin|sidebar|bibliography|"
    r"admonition|tableofcontents|glossary|exercise|solution|include|raw|math)[\s}]"
)
# A line that carries no prose at all — only roles, inline code or markup. Never absorb
# it into the previous line: it is a paragraph of its own as far as the EN/ZH structure
# comparison is concerned, and merging would desynchronise the paragraph counts.
ROLE_ONLY_RE = re.compile(r"^(?:\{[a-zA-Z-]+\}`[^`]*`|`[^`]*`|\$[^$]*\$|[*_~]+|\s)+$")
# Lines that open a block and must never be absorbed into the previous line.
BLOCK_OPEN_RE = re.compile(
    r"^\s*(?:#{1,6}\s|\+\+\+\s*$|\([^)]*\)=\s*$|[-*+]\s|\d+\.\s|\* -|>\s|"
    r"\[[^\]]*\]:|<!--|</?[a-zA-Z])"
)

IDEO = r"\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\u3040-\u30ff\uac00-\ud7af"
CJK_PUNCT = r"\u3000-\u303f\uff01-\uff0f\uff1a-\uff20\uff3b-\uff40\uff5b-\uff65\uffe0-\uffe6"
CJK_ANY = IDEO + CJK_PUNCT

# CJK punctuation that must never be preceded by a space (closing/trailing marks)
NO_SPACE_BEFORE = set("、。，；：！？）〕〗〙〛」』】》〉…—～·％℃”’")
# …and that must never be followed by one (adds the opening marks)
NO_SPACE_AFTER = NO_SPACE_BEFORE | set("（〔〖〘〚「『【《〈“‘")
ENDS_HARD_BREAK_RE = re.compile(r"(?:\\|  )$")

TEXT = "T"
STRUCT = "S"


def is_cjkish(ch: str) -> bool:
    return bool(ch) and bool(re.match(f"[{CJK_ANY}]", ch))


def fence_kind(info: str) -> str:
    """Classify a fence opener as `code` (opaque) or `prose` (still ordinary text).

    `{code-cell}` and bare ``` hold Python and data values: never touch them. But
    `{note}`, `{figure}` and friends wrap *prose* — note bodies and figure captions are
    translated sentences, and hard-wrapping inside them renders exactly the stray spaces
    this tool exists to remove.
    """
    m = re.match(r"^\s*\{([a-zA-Z:-]+)\}", info)
    if m:
        return "prose" if m.group(1).lower() in PROSE_DIRECTIVES else "code"
    return "code"  # bare ``` or a language hint


def classify(lines: list[str]) -> list[str]:
    """Label each line TEXT (a prose line that may be joined) or STRUCT."""
    kinds: list[str] = []
    fence_char = ""
    fence = ""            # "" | "code" | "prose"
    in_math = False
    in_comment = False

    for line in lines:
        fm = FENCE_RE.match(line)
        if fm:
            if not fence:
                fence_char = fm.group(2)[0]
                fence = fence_kind(fm.group(3))
            elif fm.group(2)[0] == fence_char:
                fence, fence_char = "", ""
            kinds.append(STRUCT)
            continue
        if fence == "code":
            kinds.append(STRUCT)
            continue

        if in_comment:
            kinds.append(STRUCT)
            if "-->" in line:
                in_comment = False
            continue
        if "<!---" in line or "<!--" in line:
            kinds.append(STRUCT)
            if "-->" not in line:
                in_comment = True
            continue

        if "$$" in line:
            if line.count("$$") % 2 == 1:
                in_math = not in_math
            kinds.append(STRUCT)
            continue
        if in_math:
            kinds.append(STRUCT)
            continue

        if not line.strip():
            kinds.append(STRUCT)
            continue
        if BLOCK_OPEN_RE.match(line) or DIRECTIVEISH_RE.match(line) or BLOCK_DIRECTIVE_RE.match(line):
            kinds.append(STRUCT)
            continue
        kinds.append(TEXT)
    return kinds


_LEAD_MARKUP_RE = re.compile(r"^(?:[*_~]+)")
# Inline constructs that render as Chinese and therefore hide a Chinese boundary from the
# raw-text test: a `{numref}` renders "图 5.1" / "第 3 章", and a link's own text is what
# the reader sees. Without looking through them, `并按照` + newline + `{numref}…` keeps a
# soft break that shows up as a stray space in the rendered book.
_NUMREF_LEAD_RE = re.compile(r"^\{numref\}`[^`]*`")
_LINK_LEAD_RE = re.compile(r"^\[([^\]\n]*)\]\(")
_NUMREF_TAIL_RE = re.compile(r"\{numref\}`[^`]*`$")
_LINK_TAIL_RE = re.compile(r"\[([^\]\n]*)\]\([^)\n]*\)$")


_FENCE_OPEN_RE = re.compile(r"^\s*(`{3,}|~{3,})\s*\{([a-zA-Z:-]+)\}")
_FENCE_ARG_RE = re.compile(r"^\s*(?:`{3,}|~{3,}|:{3,})\s*\{([a-zA-Z:-]+)\}\s+([A-Za-z0-9_:-]+)\s*$")
_COLON_OPEN_RE = re.compile(r"^\s*:{3,}\s*\{([a-zA-Z:-]+)\}")
_LABELISH_RE = re.compile(r"^[A-Za-z0-9_:-]+$")
_NAME_OPT_RE = re.compile(r"^\s*:name:\s*(\S+)\s*$")
_TARGET_RE = re.compile(r"^\(([^)]+)\)=\s*$")


def _kind_of_directive(name: str) -> str:
    """`figure`/`glue:figure` -> figure; `table`/`list-table` -> table; else nothing."""
    n = name.lower()
    if "table" in n:
        return "table"
    if "figure" in n:
        return "figure"
    return ""


def label_kinds(text: str) -> dict[str, str]:
    """Map every label in a chapter to "figure", "table" or "section".

    Both fence styles matter here: `:::{glue:figure} can_lang_plot_percent` names its
    target as a directive *argument* while ``` ```{figure} x ``` may instead use a
    `:name:` option, and `(label)=` targets are sections.
    """
    kinds: dict[str, str] = {}
    fence_char, fence_len, current = "", 0, ""
    for line in text.replace("\r\n", "\n").split("\n"):
        m = _TARGET_RE.match(line)
        if m:
            kinds[m.group(1)] = "section"
        if fence_char:
            if line.lstrip().startswith(fence_char * fence_len):
                fence_char, current = "", ""
                continue
            m = _NAME_OPT_RE.match(line)
            if m and current:
                kinds[m.group(1)] = current
            continue
        m = _FENCE_ARG_RE.match(line)
        if m:
            kind = _kind_of_directive(m.group(1))
            if kind and _LABELISH_RE.match(m.group(2)):
                kinds[m.group(2)] = kind
        m = _FENCE_OPEN_RE.match(line) or _COLON_OPEN_RE.match(line)
        if m:
            fence_char = ":" if line.lstrip().startswith(":") else line.lstrip()[0]
            fence_len = 3
            current = _kind_of_directive(m.group(1))

    # A bare `(label)=` target takes the kind of whatever it labels: right before a
    # heading it names a section, but right before a figure/table directive it names
    # that float — which is what decides the `{numref}` rendering, so it must override
    # the "section" default recorded above.
    lines = text.replace("\r\n", "\n").split("\n")
    for i, line in enumerate(lines):
        m = _TARGET_RE.match(line)
        if not m:
            continue
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j >= len(lines):
            continue
        m2 = (_FENCE_ARG_RE.match(lines[j]) or _FENCE_OPEN_RE.match(lines[j])
              or _COLON_OPEN_RE.match(lines[j]))
        if m2:
            kind = _kind_of_directive(m2.group(1))
            if kind:
                kinds[m.group(1)] = kind
    return kinds


# Label -> kind, resolved per file by label_kinds(). MyST label names in this book are
# not always prefixed — `confusion-matrix-table` is a table and `canadamap` is a figure —
# so the `fig:`/`tab:` prefix alone cannot tell us what a `{numref}` will render.
_KINDS: dict[str, str] = {}


def numref_edges(arg: str, kinds: dict[str, str] | None = None) -> tuple[bool, bool]:
    """What does this `{numref}` render at its first and last character?

    The book's `_config.yml` sets ``numfig_format`` to ``图 %s`` / ``表 %s`` /
    ``第 %s 节``, so the *kind of target* decides:

    figure/table target -> "图 5.1" / "表 3.2"  starts Chinese, ends with a digit
    section target      -> "第 5.8 节"           starts and ends Chinese
    custom text         -> "第 3 章"             the text itself decides

    A Chinese edge takes no adjacent space; a digit edge needs the CJK↔Latin space.
    """
    if "<" in arg:
        text = arg.split("<", 1)[0]
        return (not text.lstrip().startswith("%s"),
                not text.rstrip().endswith("%s"))
    target = arg.strip()
    if re.match(r"\s*(?:fig|figure|tab|table|code-block|code):", target):
        return True, False
    kind = (kinds if kinds is not None else _KINDS).get(target)
    if kind == "section":
        return True, True       # a section reference: "第 5.8 节"
    # figure, table, or a label we could not resolve from this chapter (a label defined
    # elsewhere, or one whose directive we failed to parse). All of those render with a
    # 图/表 prefix and a trailing *number*, so the tail needs the CJK↔Latin space.
    return True, False


def _leading_visible(nxt: str) -> str:
    """First character the reader actually sees at the start of `nxt`."""
    s = _LEAD_MARKUP_RE.sub("", nxt)
    m = _NUMREF_LEAD_RE.match(s)
    if m:
        head_cjk, _ = numref_edges(m.group(0)[len("{numref}`"):-1])
        return "图" if head_cjk else "1"
    m = _LINK_LEAD_RE.match(s)
    if m and m.group(1):
        return m.group(1)[0]
    return s[:1] or nxt[:1]


def _trailing_visible(cur: str) -> str:
    """Last character the reader actually sees at the end of `cur`."""
    s = re.sub(r"[*_~]+$", "", cur.rstrip())
    m = _LINK_TAIL_RE.search(s)
    if m and m.group(1):
        return m.group(1)[-1]
    m = _NUMREF_TAIL_RE.search(s)
    if m:
        _, tail_cjk = numref_edges(m.group(0)[len("{numref}`"):-1])
        return "节" if tail_cjk else "1"
    return s[-1:] or cur[-1]


def boundary_chars(cur: str, nxt: str) -> tuple[str, str]:
    """Last/first *rendered* characters of two lines being considered for joining."""
    return _trailing_visible(cur), _leading_visible(nxt)


def unwrap(text: str) -> tuple[str, int]:
    """Return (unwrapped_text, number_of_joins)."""
    lines = text.split("\n")
    kinds = classify(lines)
    out: list[str] = []
    joins = 0
    i = 0
    n = len(lines)
    while i < n:
        if kinds[i] == STRUCT:
            out.append(lines[i])
            i += 1
            continue
        cur = lines[i]
        j = i + 1
        while j < n and kinds[j] == TEXT:
            nxt = lines[j]
            if ENDS_HARD_BREAK_RE.search(cur):
                break
            stripped = nxt.strip()
            if not stripped or ROLE_ONLY_RE.match(stripped):
                break
            last, first = boundary_chars(cur, stripped)
            # Join with "" only where Chinese typography forbids a space. Where the
            # boundary needs one (Latin↔ideograph), keep the line break: CommonMark
            # renders it as exactly one space, which is what the style guide wants.
            ideo = lambda c: bool(c) and bool(re.match(f"[{IDEO}]", c))
            merge = (
                (ideo(last) and ideo(first))
                or (is_cjkish(last) and is_cjkish(first))
                or (first in NO_SPACE_BEFORE)
                or (last in NO_SPACE_AFTER)
            )
            if not merge:
                break
            cur = cur + stripped
            joins += 1
            j += 1
        out.append(cur)
        i = j
    return "\n".join(out), joins


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", type=Path, required=True)
    ap.add_argument("--check", action="store_true", help="report only, do not write")
    args = ap.parse_args()

    raw = args.path.read_text(encoding="utf-8")
    newline = "\r\n" if raw.count("\r\n") > raw.count("\n") / 2 else "\n"
    body = raw.replace("\r\n", "\n")
    _KINDS.clear()
    _KINDS.update(label_kinds(body))
    fixed, joins = unwrap(body)
    if args.check:
        print(f"{args.path.name}: would join {joins} soft break(s)")
        return 0
    if fixed == body:
        print(f"{args.path.name}: already unwrapped (0 joins)")
        return 0
    args.path.write_bytes(fixed.replace("\n", newline).encode("utf-8"))
    print(f"{args.path.name}: joined {joins} soft break(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())