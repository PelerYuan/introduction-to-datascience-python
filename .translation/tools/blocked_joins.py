#!/usr/bin/env python3
"""Report prose line pairs that *should* join but are blocked by classify().

unwrap_cjk.py joins adjacent TEXT lines whose rendered boundary needs no space. A join
that the boundary rule wants but that never happens means classify() marked the second
line STRUCT — this prints which structural rule did it, which is the only way to tell a
genuine block opener from a false positive (indented list continuations, mostly).
"""
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


def why_struct(line: str) -> str:
    if u.FENCE_RE.match(line):
        return "fence"
    if not line.strip():
        return "blank"
    if "$$" in line:
        return "math"
    if u.BLOCK_OPEN_RE.match(line):
        return "BLOCK_OPEN:" + repr(u.BLOCK_OPEN_RE.match(line).group(0)[:12])
    if u.DIRECTIVEISH_RE.match(line):
        return "DIRECTIVEISH:" + repr(u.DIRECTIVEISH_RE.match(line).group(0)[:8])
    if u.BLOCK_DIRECTIVE_RE.match(line):
        return "BLOCK_DIRECTIVE"
    return "?"


def main() -> int:
    for path in sorted(Path("source").glob("*.md")):
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        lines = text.split("\n")
        kinds = u.classify(lines)
        u._KINDS.clear()
        u._KINDS.update(u.label_kinds(text))
        found = []
        for i in range(len(lines) - 1):
            if kinds[i] != u.TEXT or kinds[i + 1] == u.TEXT:
                continue
            nxt = lines[i + 1].strip()
            if not nxt or u.ROLE_ONLY_RE.match(nxt):
                continue
            # A closing fence is a boundary, not a continuation: `boundary_chars` would
            # otherwise see "。" before ":::" and think a join was wanted.
            if re.fullmatch(r"(?:`{3,}|~{3,}|:{3,})", nxt):
                continue
            last, first = u.boundary_chars(lines[i], nxt)
            if not (last and first):
                continue
            ideo = lambda c: bool(re.match(f"[{u.IDEO}]", c))
            merge = (
                (ideo(last) and ideo(first))
                or (u.is_cjkish(last) and u.is_cjkish(first))
                or (first in u.NO_SPACE_BEFORE)
                or (last in u.NO_SPACE_AFTER)
            )
            if merge:
                found.append((i + 1, why_struct(lines[i + 1]), lines[i][-30:], nxt[:30]))
        if found:
            print(f"=== {path.name}: {len(found)} blocked join(s)")
            for ln, why, a, b in found[:6]:
                print(f"   L{ln} [{why}] {a!r} -> {b!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())