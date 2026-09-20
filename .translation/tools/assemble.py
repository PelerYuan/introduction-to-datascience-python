#!/usr/bin/env python3
"""Assemble translated chunks into final chapter files, with QA gates.

Assembly is **seam-exact**: the chunker splits at structural break points where the
original may have had no blank line (e.g. `(label)=` immediately followed by a
heading). Joining blindly with a blank line would insert a paragraph that the
source did not have. So the assembler re-derives the exact inter-chunk whitespace
from the English source and reproduces it verbatim.

    source/<chapter>.md == front_matter + L0 + zh0 + (T0+L1) + zh1 + ... + Tn

Also:
  * strips any `<<TERM>> ... <<END>>` blocks emitted by translators and collects them
    into .translation/work/term_requests.md
  * preserves the source file's line-ending convention
  * runs tools/verify_structure.py against .translation/source_en/<chapter>.md
  * runs tools/lint_zh.py
  * refuses to write a chapter when a chunk is missing, unless --allow-missing

Exit code 0 = all requested chapters assembled and structurally valid.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TR = ROOT / ".translation"
TOOLS = TR / "tools"
sys.path.insert(0, str(TOOLS))
import segment as seg  # noqa: E402
import unwrap_cjk  # noqa: E402

TERM_BLOCK_RE = re.compile(r"<<TERM>>.*?<<END>>", re.DOTALL)
LEAD_FM_RE = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.DOTALL)

TARGET_LINES = 480
SOFT_MAX = 780

CHAPTERS = [
    "index", "preface-text", "foreword-text", "acknowledgements", "authors",
    "intro", "reading", "wrangling", "viz", "classification1", "classification2",
    "regression1", "regression2", "clustering", "inference", "jupyter",
    "version-control", "setup",
]


def idx(p: Path) -> int:
    return int(re.search(r"chunk_(\d+)", p.name).group(1))


def lead_ws(s: str) -> str:
    return re.match(r"\s*", s).group(0)


def trail_ws(s: str) -> str:
    return re.search(r"\s*$", s).group(0)


def assemble(chapter: str, allow_missing: bool, verbose: bool) -> tuple[bool, list[str], dict]:
    d = TR / "work" / chapter
    msgs: list[str] = []
    info: dict = {}

    src_chunks = sorted(d.glob("chunk_*.src.md"), key=idx)
    zh_chunks = sorted(d.glob("chunk_*.zh.md"), key=idx)
    expected = [p.name.replace(".src.md", ".zh.md") for p in src_chunks]
    got = {p.name for p in zh_chunks}
    missing = [n for n in expected if n not in got]
    if missing:
        msgs.append(f"MISSING CHUNKS: {', '.join(missing)}")
        info["missing"] = missing
        if not allow_missing:
            return False, msgs, info

    # --- re-derive the original chunks and the exact seam whitespace -------------
    en_path = TR / "source_en" / f"{chapter}.md"
    en_bytes = en_path.read_bytes()
    newline = "\r\n" if en_bytes.count(b"\r\n") > en_bytes.count(b"\n") / 2 else "\n"
    en_text = en_bytes.decode("utf-8").replace("\r\n", "\n")
    _, en_pieces = seg.segment(en_text, TARGET_LINES, SOFT_MAX)

    if len(en_pieces) != len(src_chunks):
        msgs.append(f"WARNING: re-segmentation produced {len(en_pieces)} pieces but "
                    f"{len(src_chunks)} source chunks exist; seams may be inexact")
        info["seam_warning"] = True
        en_pieces = en_pieces[: len(src_chunks)] or en_pieces
    else:
        # sanity check: pieces must match the emitted src chunks
        for i, (p, f) in enumerate(zip(en_pieces, src_chunks)):
            if p.replace("\r\n", "\n") != f.read_text(encoding="utf-8").replace("\r\n", "\n"):
                msgs.append(f"WARNING: re-derived piece {i + 1} differs from {f.name}")
                info["seam_warning"] = True
                break

    fm = (d / "front_matter.txt").read_text(encoding="utf-8")
    fm = fm.replace("\r\n", "\n")
    l0 = lead_ws(en_pieces[0]) if en_pieces else ""
    tn = trail_ws(en_pieces[-1]) if en_pieces else "\n"

    seps: list[str] = []
    for i in range(len(en_pieces) - 1):
        seps.append(trail_ws(en_pieces[i]) + lead_ws(en_pieces[i + 1]))

    # --- collect translated cores ----------------------------------------------
    cores: list[str] = []
    terms: list[str] = []
    for p in zh_chunks:
        text = p.read_text(encoding="utf-8").replace("\r\n", "\n")
        text = LEAD_FM_RE.sub("", text, count=1)
        if "<<" in text:
            for m in TERM_BLOCK_RE.finditer(text):
                terms.extend(l.strip() for l in m.group(0).splitlines()
                             if l.strip() and not l.strip().startswith("<<"))
            text = TERM_BLOCK_RE.sub("", text)
        cores.append(text.strip("\n"))

    parts = [fm, l0, cores[0]] if cores else [fm]
    for i, core in enumerate(cores[1:]):
        parts.append(seps[i] if i < len(seps) else "\n\n")
        parts.append(core)
    out_lf = "".join(parts).rstrip("\n") + tn

    # Chinese typography: a soft line break renders as a space, which is wrong
    # between Chinese characters. Join those soft breaks with "" (English-dependent
    # breaks keep the newline, which correctly renders as a space).
    out_lf, joins = unwrap_cjk.unwrap(out_lf)
    info["soft_break_joins"] = joins

    out = out_lf.replace("\n", newline)
    target = ROOT / "source" / f"{chapter}.md"
    target.write_bytes(out.encode("utf-8"))

    if terms:
        tf = TR / "work" / "term_requests.md"
        existing = tf.read_text(encoding="utf-8") if tf.exists() else "# 译者登记的候选术语\n"
        existing += f"\n## {chapter}\n" + "\n".join(terms) + "\n"
        tf.write_text(existing, encoding="utf-8")

    info["bytes"] = len(out.encode("utf-8"))
    info["chunks"] = f"{len(zh_chunks)}/{len(expected)}"
    info["newline"] = "CRLF" if newline == "\r\n" else "LF"
    msgs.append(f"wrote source/{chapter}.md ({info['bytes'] / 1024:.1f} KB, "
                f"{info['chunks']} chunks, {info['newline']}, "
                f"joined {info.get('soft_break_joins', 0)} CJK soft breaks)")
    if verbose and seps:
        tight = [i + 1 for i, s in enumerate(seps) if "\n\n" not in s]
        if tight:
            msgs.append(f"   seam-exact joins preserved {len(tight)} tight seam(s): {tight}")
    return True, msgs, info


def run(cmd: list[str]) -> tuple[int, str]:
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=env)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("chapters", nargs="*", default=None)
    ap.add_argument("--allow-missing", action="store_true")
    ap.add_argument("--skip-verify", action="store_true")
    ap.add_argument("--json", type=Path, default=None)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    chapters = args.chapters or CHAPTERS
    report: dict = {}
    worst = 0
    for ch in chapters:
        if not (TR / "work" / ch).exists():
            continue
        ok, msgs, info = assemble(ch, args.allow_missing, args.verbose)
        for m in msgs:
            print(f"[{ch}] {m}" if not m.startswith("   ") else f"[{ch}]{m}")
        entry = {"assembled": ok, "messages": msgs, **info}
        if ok and not args.skip_verify:
            rc, out = run([sys.executable, str(TOOLS / "verify_structure.py"),
                           "--en", str(TR / "source_en" / f"{ch}.md"),
                           "--zh", str(ROOT / "source" / f"{ch}.md")])
            print("   " + out.strip().replace("\n", "\n   "))
            entry["verify_rc"] = rc
            if rc != 0:
                worst = 1
                rc2, out2 = run([sys.executable, str(TOOLS / "diff_paragraphs.py"),
                                 "--en", str(TR / "source_en" / f"{ch}.md"),
                                 "--zh", str(ROOT / "source" / f"{ch}.md"),
                                 "--context", "0"])
                entry["paragraph_diff"] = out2.strip().splitlines()[:24]
                print("   " + "\n   ".join(entry["paragraph_diff"]))
            rc3, out3 = run([sys.executable, str(TOOLS / "lint_zh.py"),
                             "--zh", str(ROOT / "source" / f"{ch}.md")])
            entry["lint_rc"] = rc3
            print("   " + (out3.strip().splitlines()[0] if out3.strip() else ""))
        if not ok:
            worst = 1
        report[ch] = entry

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return worst


if __name__ == "__main__":
    raise SystemExit(main())