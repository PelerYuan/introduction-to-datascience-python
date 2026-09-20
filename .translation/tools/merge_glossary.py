#!/usr/bin/env python3
"""Merge GLOSSARY_CORE.md + .translation/glossary/part_*.md into GLOSSARY.md and report conflicts."""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TR = ROOT

ENTRY_RE = re.compile(r"^([^|#>\s][^|]*?)\s*\|\s*([^|]+?)\s*(?:\|\s*(.*))?$")
# entries inside the core file are wrapped in ``` fences
CORE_ENTRY_RE = ENTRY_RE


def parse(path: Path, core: bool) -> tuple[list[tuple[str, str, str]], list[str]]:
    entries: list[tuple[str, str, str]] = []
    headings: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if line.lstrip().startswith("```"):
            continue
        if line.startswith("#"):
            headings.append(line)
            continue
        if not line.strip() or line.startswith(">") or line.strip().startswith("<!--"):
            continue
        m = ENTRY_RE.match(line.strip())
        if m:
            en = m.group(1).strip()
            zh = m.group(2).strip()
            note = (m.group(3) or "").strip()
            if en and zh and en.lower() not in {"english term", "format"}:
                entries.append((en, zh, note))
    return entries, headings


def main() -> int:
    core_entries, _ = parse(TR / "GLOSSARY_CORE.md", core=True)
    parts = sorted((TR / "glossary").glob("part_*.md"))
    part_entries: list[tuple[str, str, str]] = []
    part_blocks: list[str] = []
    for p in parts:
        e, h = parse(p, core=False)
        part_entries.extend(e)
        part_blocks.append(p.read_text(encoding="utf-8").rstrip())

    core_map = {en.lower(): zh for en, zh, _ in core_entries}
    conflicts: list[str] = []
    by_en: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for en, zh, note in part_entries:
        by_en[en.lower()].append((zh, note))

    # 1. conflicts with the core glossary
    for en_l, vals in by_en.items():
        if en_l in core_map:
            zhs = {zh for zh, _ in vals}
            if zhs - {core_map[en_l]}:
                conflicts.append(f"[CORE] {en_l!r}: core={core_map[en_l]!r} parts={sorted(zhs)}")

    # 2. internal conflicts between parts
    for en_l, vals in sorted(by_en.items()):
        zhs = sorted({zh for zh, _ in vals})
        if len(zhs) > 1:
            conflicts.append(f"[PART] {en_l!r}: {zhs}")

    # 3. duplicates within a part
    dupes = defaultdict(int)
    for en, _, _ in part_entries:
        dupes[en.lower()] += 1
    dup_list = sorted(k for k, v in dupes.items() if v > 1)

    out = [
        "# 《数据科学：Python 入门》翻译术语表（GLOSSARY）",
        "",
        "> 本表是全书术语一致性的唯一依据。**翻译与审校时必须逐条遵守。**",
        "> 第一节为核心术语（总协调人确定，优先级最高，不得更改）；其余各节由领域术语抽取生成。",
        "> **凡后文条目与第一部分（核心术语）冲突，一律以第一部分为准；同一条目在同一节内出现多次时，取第一次出现的译法。**",
        "> 标记 `[保留英文]` 的词在任何情况下都不翻译；标记 `[保留原文]` 的词保留原语言写法。",
        "",
        "---",
        "",
        "## 第一部分：核心术语（最高优先级）",
        "",
        (TR / "GLOSSARY_CORE.md").read_text(encoding="utf-8").strip(),
        "",
        "---",
        "",
    ]
    for block in part_blocks:
        out.append(block)
        out.append("")
        out.append("---")
        out.append("")

    header = "\n".join(out).rstrip() + "\n"
    (TR / "GLOSSARY.md").write_text(header, encoding="utf-8")

    print(f"core entries: {len(core_entries)}")
    print(f"part entries: {len(part_entries)}  (unique English: {len(by_en)})")
    print(f"total lines: {len(header.splitlines())}, bytes: {len(header.encode('utf-8'))}")
    print(f"internal duplicates: {len(dup_list)}")
    if conflicts:
        print(f"\nCONFLICTS ({len(conflicts)}):")
        for c in conflicts[:60]:
            print("  " + c)
    else:
        print("\nNo conflicts detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())