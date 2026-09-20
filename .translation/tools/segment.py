#!/usr/bin/env python3
"""Split a MyST chapter into translation chunks at structurally safe boundaries.

Guarantees: concatenating the emitted chunk files in order reproduces the original
body byte-for-byte (verified by this script's `--selftest`).

Never splits inside a fenced code block. Splits only immediately before a
`## `-level heading or a `+++` cell separator, falling back to blank-line
paragraph boundaries when a single section is too large.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

FRONT_MATTER_RE = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.DOTALL)


def split_front_matter(text: str) -> tuple[str, str]:
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return "", text
    return m.group(0), text[m.end():]


def fence_map(lines: list[str]) -> list[bool]:
    """inside[i] is True when lines[i] is inside a fenced code block (exclusive of the fence lines themselves)."""
    inside = [False] * len(lines)
    open_fence = False
    fence_char = ""
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        m = re.match(r"(`{3,}|~{3,})", stripped)
        if not open_fence:
            if m:
                open_fence = True
                fence_char = m.group(1)[0]
            inside[i] = False
        else:
            inside[i] = True
            if m and m.group(1)[0] == fence_char:
                inside[i] = False
                open_fence = False
    return inside


def candidate_breaks(lines: list[str], inside: list[bool]) -> list[int]:
    """Indices i such that a chunk may start at lines[i]."""
    cands = []
    for i, line in enumerate(lines):
        if inside[i]:
            continue
        if re.match(r"^#{1,2} ", line) or line.strip() == "+++":
            cands.append(i)
    return cands


def paragraph_breaks(lines: list[str], inside: list[bool]) -> list[int]:
    """Indices i such that a chunk may start at lines[i] (finer granularity)."""
    cands = []
    for i, line in enumerate(lines):
        if inside[i]:
            continue
        if i == 0:
            cands.append(i)
            continue
        # blank line followed by content, or a +++ marker
        if line.strip() == "+++":
            cands.append(i)
        elif line.strip() == "" and lines[i - 1].strip() != "":
            cands.append(i + 1 if i + 1 < len(lines) else i)
    return sorted(set(cands))


def section_spans(lines: list[str], inside: list[bool]) -> list[tuple[int, int]]:
    cands = candidate_breaks(lines, inside)
    if not cands or cands[0] != 0:
        cands = [0] + cands
    spans = []
    for a, b in zip(cands, cands[1:]):
        spans.append((a, b))
    spans.append((cands[-1], len(lines)))
    return spans


def hard_split(lines: list[str], inside: list[bool], start: int, end: int, target: int) -> list[tuple[int, int]]:
    """Split a large span at paragraph boundaries."""
    breaks = [b for b in paragraph_breaks(lines, inside) if start < b < end]
    breaks = [start] + breaks + [end]
    out = []
    cur = start
    for b in breaks[1:]:
        if b in (start, end):
            continue
        if b - cur >= target:
            out.append((cur, b))
            cur = b
    out.append((cur, end))
    return out


def segment(text: str, target: int, soft_max: int) -> tuple[str, list[str]]:
    head, body = split_front_matter(text)
    lines = body.splitlines(keepends=True)
    inside = fence_map(lines)
    spans = section_spans(lines, inside)

    # expand oversized spans
    expanded: list[tuple[int, int]] = []
    for a, b in spans:
        if b - a > soft_max:
            expanded.extend(hard_split(lines, inside, a, b, target))
        else:
            expanded.append((a, b))

    # greedily group into chunks
    chunks: list[tuple[int, int]] = []
    cur_a, cur_b = expanded[0]
    for a, b in expanded[1:]:
        if (b - cur_a) <= target or (cur_b - cur_a) < target * 0.6:
            cur_b = b
        else:
            chunks.append((cur_a, cur_b))
            cur_a, cur_b = a, b
    chunks.append((cur_a, cur_b))

    pieces = ["".join(lines[a:b]) for a, b in chunks]
    return head, pieces


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path)
    ap.add_argument("outdir", type=Path)
    ap.add_argument("--target", type=int, default=330)
    ap.add_argument("--soft-max", type=int, default=560)
    ap.add_argument("--context-lines", type=int, default=25)
    ap.add_argument("--from-en", type=Path, default=None,
                    help="Also emit a .en.md copy of each chunk (for the original English repo layout)")
    args = ap.parse_args()

    text = args.src.read_text(encoding="utf-8")
    head, pieces = segment(text, args.target, args.soft_max)

    # selftest: reassembly must be byte-exact
    if head + "".join(pieces) != text:
        print("FATAL: segmentation is not lossless", file=sys.stderr)
        return 2

    args.outdir.mkdir(parents=True, exist_ok=True)
    for p in args.outdir.glob("chunk_*"):
        p.unlink()
    (args.outdir / "front_matter.txt").write_text(head, encoding="utf-8")

    lines = pieces
    for i, piece in enumerate(lines, 1):
        (args.outdir / f"chunk_{i:02d}.src.md").write_text(piece, encoding="utf-8")
        if args.from_en is not None:
            (args.outdir / f"chunk_{i:02d}.en.md").write_text(piece, encoding="utf-8")
        # read-only preceding context (last N lines of the previous chunk)
        ctx = ""
        if i >= 2:
            prev = lines[i - 2]
            ctx = "".join(prev.splitlines(keepends=True)[-args.context_lines:])
        (args.outdir / f"chunk_{i:02d}.ctx.md").write_text(ctx, encoding="utf-8")

    meta = {
        "src": str(args.src),
        "front_matter_bytes": len(head.encode("utf-8")),
        "chunks": [
            {
                "index": i,
                "lines": len(p.splitlines()),
                "bytes": len(p.encode("utf-8")),
                "first_line": p.splitlines()[0] if p.splitlines() else "",
            }
            for i, p in enumerate(pieces, 1)
        ],
    }
    (args.outdir / "chunks.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{args.src.name}: {len(pieces)} chunks, "
          f"{sum(c['bytes'] for c in meta['chunks']) / 1024:.1f} KB body, lossless=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())