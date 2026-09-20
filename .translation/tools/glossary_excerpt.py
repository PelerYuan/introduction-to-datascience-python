#!/usr/bin/env python3
"""Build a per-chapter glossary excerpt so translators need not load the full 48 KB table.

Always includes the whole core table (sections A-I), plus every part entry whose
English headword or Chinese rendering occurs in that chapter's source chunks.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TR = ROOT / ".translation"

ENTRY_RE = re.compile(r"^([^|#>\s][^|]*?)\s*\|\s*([^|]+?)\s*(?:\|\s*(.*))?$")

CHAPTERS = [
    "index", "preface-text", "foreword-text", "acknowledgements", "authors",
    "intro", "reading", "wrangling", "viz", "classification1", "classification2",
    "regression1", "regression2", "clustering", "inference", "jupyter",
    "version-control", "setup",
]


def load_entries(path: Path) -> list[str]:
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith(">") or s.startswith("`"):
            continue
        if ENTRY_RE.match(s):
            out.append(s)
    return out


def main() -> int:
    core = load_entries(TR / "GLOSSARY_CORE.md")
    parts: list[tuple[Path, list[str]]] = []
    for p in sorted((TR / "glossary").glob("part_*.md")):
        parts.append((p, load_entries(p)))
    total_all = len(core) + sum(len(e) for _, e in parts)

    for ch in CHAPTERS:
        d = TR / "work" / ch
        srcs = sorted(d.glob("chunk_*.src.md"))
        if not srcs:
            continue
        corpus = "\n".join(s.read_text(encoding="utf-8") for s in srcs)
        corpus_low = corpus.lower()

        lines = [
            f"# 本章术语表（{ch}）",
            "",
            "> 这是从全书术语表按本章语料抽取的子集，**已包含全部核心术语**。",
            "> 需要查证未列出的词时，再打开 `.translation/GLOSSARY.md` 全文。",
            "> 格式：`English | 中文 | 备注`",
            "",
            "## 一、核心术语（最高优先级，含跨节裁决）",
            "",
        ]
        lines += core
        for p, entries in parts:
            hits = [e for e in entries
                    if e.split("|")[0].strip()
                    and (e.split("|")[0].strip().lower() in corpus_low
                         or (len(e.split("|")) > 1 and e.split("|")[1].strip() in corpus))]
            if hits:
                lines += ["", f"## {p.stem}（本章相关条目）", ""]
                lines += hits

        dest = d / "glossary_excerpt.md"
        dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"{ch:<20} excerpt {len(lines):>5} lines / {dest.stat().st_size/1024:>6.1f} KB "
              f"(full table: {total_all} entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())