#!/usr/bin/env python3
"""Detect Markdown markers that survive rendering and reach the reader as literal text.

`lint_zh.py` checks the Chinese prose, and `verify_structure.py` compares structure, but
neither of them renders anything — so neither could see the defect that mattered most to
readers here: an emphasis run that CommonMark refuses to close, leaving `**` visible in the
middle of a sentence.

The rule that causes it is the "right-flanking delimiter run" rule. A closing `**` is only
valid if it is not preceded by whitespace and either

  * is not preceded by punctuation, or
  * is preceded by punctuation *and* followed by whitespace or punctuation.

English rarely trips this because `**word**` is followed by a space or a full stop. Chinese
does: `**汇总：**计算……` closes a run that is preceded by `：` and followed by `计`, so it
never closes and the asterisks are printed.

Rather than re-implementing that rule (and getting it subtly wrong), this renders each
prose block with markdown-it — the same engine MyST uses — and looks for emphasis
delimiters that survived into the output text.

Usage:
    python check_emphasis.py [--path source/intro.md] [--all] [--max-show 5]
Exit code 1 when any leaked marker is found.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import unwrap_cjk as u  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from markdown_it import MarkdownIt  # noqa: E402

MD = MarkdownIt("commonmark")

# A leftover delimiter is one or two `*` or `_` sitting in rendered text.
LEAK = re.compile(r"(?<![\\\w])(\*{1,3}|_{1,3})(?![*\s])")

# Emphasis that swallows several sentences is almost always the *other* half of this
# defect: when the intended closing run fails to close, it pairs with the next opening run
# instead, so a whole paragraph ends up bold and no literal marker is left behind.
# Restricted to <strong>: a long <em> is usually a deliberately italicised quotation, and
# flagging those buries the real finding in noise.
SENTENCE_END = re.compile(r"[。！？]")
SPAN = re.compile(r"<(strong)>(.*?)</\1>", re.S)
SPAN_MAX = 60

# Math is not markup. CommonMark does not parse `$...$`, so `CO$_{\text{2}}$` reaches this
# check as literal text and its subscript looks exactly like leaked `_` emphasis. The
# English source produces 15 of these and nothing else, which is how the false positive
# was found — so math is blanked out before markers are counted.
MATH = re.compile(r"\$\$[^$]*\$\$|\$[^$\n]*\$")

FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")


def prose_lines(lines: list[str]) -> list[tuple[int, str]]:
    """(line_number, text) for every line that is not inside a code fence.

    Code fences are opaque — a `*` inside one is data, not markup. Everything else is
    fair game, including STRUCT lines: a list item such as
    `1. **汇总：**计算……` carries prose and its emphasis is rendered like any other.
    """
    out: list[tuple[int, str]] = []
    fence: str | None = None
    for i, line in enumerate(lines):
        m = FENCE_RE.match(line)
        if m:
            if fence is None:
                fence = u.fence_kind(m.group(3).strip())
            else:
                fence = None
            continue
        if fence == "code":
            continue
        out.append((i + 1, line))
    return out


def blocks(lines: list[str]) -> list[tuple[int, str]]:
    """Group consecutive non-blank prose lines into (first_line_number, text) blocks.

    Rendering the whole block matters: a delimiter run at the end of one source line is
    followed by whatever the next line starts with once the paragraph is unwrapped, and
    that is what decides whether it closes.
    """
    out, buf, start = [], [], 0
    for num, line in prose_lines(lines):
        if line.strip():
            if not buf:
                start = num
            buf.append(line.strip())
        elif buf:
            out.append((start, "\n".join(buf)))
            buf = []
    if buf:
        out.append((start, "\n".join(buf)))
    return out


def scan(path: Path) -> tuple[list[tuple[int, str, str]], list[tuple[int, str, str]]]:
    raw = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    lines = raw.split("\n")
    leaks, spans = [], []
    for start, text in blocks(lines):
        # Math is blanked in the *source* before rendering. Doing it afterwards does not
        # work: commonmark never parses `$...$`, so the underscore in `CO$_{\text{2}}$`
        # survives into the rendered text and looks exactly like leaked emphasis.
        masked = MATH.sub(lambda m: " " * len(m.group(0)), text)
        html = MD.render(masked)
        # Strip code spans from the rendered output before looking for leftovers.
        visible = re.sub(r"<code>.*?</code>", "", html, flags=re.S)
        plain = re.sub(r"<[^>]+>", "", visible)
        for m in LEAK.finditer(plain):
            a = max(0, m.start() - 45)
            leaks.append((start, m.group(0), plain[a:m.end() + 45].replace("\n", " ")))
        for m in SPAN.finditer(html):
            inner = re.sub(r"<[^>]+>", "", m.group(2))
            if len(inner) > SPAN_MAX and SENTENCE_END.search(inner):
                spans.append((start, m.group(1), inner[:70].replace("\n", " ")))
    return leaks, spans


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", type=Path)
    ap.add_argument("--dir", type=Path, default=Path("source"))
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--max-show", type=int, default=5)
    args = ap.parse_args()

    targets = [args.path] if args.path else sorted(args.dir.glob("*.md"))
    total, total_spans = 0, 0
    for path in targets:
        leaks, spans = scan(path)
        if not leaks and not spans:
            continue
        total += len(leaks)
        total_spans += len(spans)
        print(f"\n{path.name}: {len(leaks)} leaked marker(s), {len(spans)} over-long span(s)")
        for line, marker, ctx in leaks[: args.max_show]:
            print(f"   L{line} LEAK {marker!r}  …{ctx.strip()}…")
        for line, tag, ctx in spans[: args.max_show]:
            print(f"   L{line} SPAN <{tag}> spans {ctx!r}…")
        shown = max(len(leaks), len(spans))
        if shown > args.max_show:
            print(f"   … and {shown - args.max_show} more of each")

    print(f"\ntotal: {total} leaked marker(s), {total_spans} over-long span(s) in {len(targets)} file(s)")
    if total or total_spans:
        print("fix: move the punctuation outside the emphasis (`**X：**Y` -> `**X**：Y`),")
        print("     or bold only the Chinese term (`**X（E）**Y` -> `**X**（E）Y`).")
        return 1
    print("OK   no Markdown marker leaks into rendered prose")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())