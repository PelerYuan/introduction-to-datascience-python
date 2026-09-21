#!/usr/bin/env python3
"""Write a paragraph-aligned EN/ZH side-by-side view for review.

The machine gates prove structure, terminology and rendering are correct; they cannot
judge whether a sentence says the right thing in natural Chinese. That check is a human
read, and it is far faster when the English sits directly above the Chinese.

Paragraph i of the English and paragraph i of the Chinese correspond, because
verify_structure.py asserts both counts are equal for every chapter. Code blocks are
excluded from these paragraph lists on purpose: they are verified byte-identical to the
English source, so there is nothing to review inside them.

Usage: python side_by_side.py [--out .translation/review] [chapter ...]
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_structure as vs  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def paragraphs(path: Path) -> list[str]:
    return vs.structure(path.read_text(encoding="utf-8"))["paragraph_list"]


def wrap(text: str, width: int = 100) -> list[str]:
    words, line, out = text.split(), "", []
    for w in words:
        if len(line) + len(w) + 1 > width:
            out.append(line)
            line = w
        else:
            line = f"{line} {w}".strip()
    out.append(line)
    return [l for l in out if l]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("chapters", nargs="*")
    ap.add_argument("--en-dir", type=Path, default=Path(".translation/source_en"))
    ap.add_argument("--zh-dir", type=Path, default=Path("source"))
    ap.add_argument("--out", type=Path, default=Path(".translation/review"))
    args = ap.parse_args()

    names = args.chapters or [p.stem for p in sorted(args.zh_dir.glob("*.md"))]
    args.out.mkdir(parents=True, exist_ok=True)
    bad = 0
    for name in names:
        en = paragraphs(args.en_dir / f"{name}.md")
        zh = paragraphs(args.zh_dir / f"{name}.md")
        if len(en) != len(zh):
            print(f"SKIP {name}: paragraph count differs (EN={len(en)} ZH={len(zh)})")
            bad += 1
            continue
        lines = [f"# {name} — 逐段对照（EN / ZH）", ""]
        for i, (a, b) in enumerate(zip(en, zh), 1):
            lines.append(f"## [{i}]")
            lines.append("")
            lines.append("**EN**")
            lines.append("")
            lines.extend(wrap(a))
            lines.append("")
            lines.append("**ZH**")
            lines.append("")
            lines.append(b)
            lines.append("")
        (args.out / f"{name}.md").write_text("\n".join(lines), encoding="utf-8")
        print(f"OK   {name}: {len(zh)} paragraph pairs -> {args.out / (name + '.md')}")
    print(f"\n{len(names) - bad}/{len(names)} chapters written to {args.out}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())