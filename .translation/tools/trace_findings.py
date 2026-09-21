#!/usr/bin/env python3
"""Trace rendered-space findings whose text spans a source line break.

Same idea as trace_findings.py, but the search is whitespace-insensitive across a window
of lines, so it also finds spots where the renderer's space comes from a line break rather
than from characters in the file. That distinction is the whole question: a break between
two Chinese characters is a defect, a break at a Latin boundary is not.
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

TARGETS = [
    ("index", "采用知识共享署名"),
    ("regression2", "实用的教程和"),
    ("viz", "例如配色方案功能"),
    ("viz", "在y轴上绘制"),
    ("viz", "这种关系就是强相关关系"),
    ("wrangling", "列出了使用str.split"),
    ("classification2", "以及进阶用法时极好"),
]


def main() -> int:
    for chapter, needle in TARGETS:
        path = Path("source") / f"{chapter}.md"
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        lines = text.split("\n")
        kinds = u.classify(lines)
        # Whitespace-insensitive search over the joined text, then map back to lines.
        starts, joined = [], []
        for i, line in enumerate(lines):
            starts.append(len(joined))
            joined.extend(re.sub(r"\s+", "", line))
        flat = "".join(joined)
        want = re.sub(r"\s+", "", needle)
        pos = flat.find(want)
        print(f"\n--- {chapter}.md  needle {needle!r}  -> ", end="")
        if pos < 0:
            print("NOT FOUND")
            continue
        end = pos + len(want) - 1
        first = max(i for i, s in enumerate(starts) if s <= pos)
        last = max(i for i, s in enumerate(starts) if s <= end)
        print(f"L{first + 1}..L{last + 1}")
        for k in range(max(0, first - 1), min(len(lines), last + 2)):
            print(f"   {k + 1:5} [{kinds[k]}] {lines[k][:160]!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())