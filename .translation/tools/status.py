#!/usr/bin/env python3
"""Book-wide translation status dashboard.

For every chapter chunk: does a translation exist, does it pass the structural
verifier against its own source chunk, does it pass the Chinese linter.

Usage:
    python status.py [--json .translation/reports/status.json] [--verify]
Exit code 0 always (this is a report, not a gate).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TR = ROOT / ".translation"
TOOLS = TR / "tools"

CHAPTERS = [
    "index", "preface-text", "foreword-text", "acknowledgements", "authors",
    "intro", "reading", "wrangling", "viz", "classification1", "classification2",
    "regression1", "regression2", "clustering", "inference", "jupyter",
    "version-control", "setup",
]
TITLES = {
    "index": "封面", "preface-text": "前言", "foreword-text": "序", "acknowledgements": "致谢",
    "authors": "作者", "intro": "Ch1 Python 与 Pandas", "reading": "Ch2 读取数据",
    "wrangling": "Ch3 数据清洗与整理", "viz": "Ch4 有效的数据可视化",
    "classification1": "Ch5 分类 I", "classification2": "Ch6 分类 II",
    "regression1": "Ch7 回归 I", "regression2": "Ch8 回归 II", "clustering": "Ch9 聚类",
    "inference": "Ch10 统计推断", "jupyter": "Ch11 Jupyter", "version-control": "Ch12 版本控制",
    "setup": "Ch13 环境配置",
}

HAN = re.compile(r"[\u4e00-\u9fff]")


def idx(p: Path) -> int:
    return int(re.search(r"chunk_(\d+)", p.name).group(1))


def run(cmd: list[str]) -> tuple[int, str]:
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env={"PYTHONIOENCODING": "utf-8",
                                              "PATH": __import__("os").environ.get("PATH", "")})
    return r.returncode, (r.stdout or "").strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=Path, default=None)
    ap.add_argument("--verify", action="store_true", help="also run the structural verifier")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    report: dict = {"chapters": {}, "totals": {}}
    n_done = n_missing = n_vfail = n_lfail = 0

    for ch in CHAPTERS:
        d = TR / "work" / ch
        if not d.exists():
            continue
        srcs = sorted(d.glob("chunk_*.src.md"), key=idx)
        entry = {"title": TITLES.get(ch, ch), "chunks": []}
        for s in srcs:
            z = d / f"{s.name.replace('.src.md', '.zh.md')}"
            rec = {"chunk": idx(s), "src_kb": round(s.stat().st_size / 1024, 1)}
            if not z.exists():
                rec["status"] = "MISSING"
                n_missing += 1
            else:
                rec["zh_kb"] = round(z.stat().st_size / 1024, 1)
                rec["han"] = len(HAN.findall(z.read_text(encoding="utf-8")))
                rec["status"] = "ok"
                if args.verify:
                    rc, out = run([sys.executable, str(TOOLS / "verify_structure.py"),
                                   "--en", str(s), "--zh", str(z)])
                    rec["verify"] = "OK" if rc == 0 else "FAIL"
                    if rc != 0:
                        rec["verify_detail"] = out.splitlines()[1:4]
                        n_vfail += 1
                        rec["status"] = "VFAIL"
                rc2, out2 = run([sys.executable, str(TOOLS / "lint_zh.py"), "--zh", str(z)])
                rec["lint"] = "OK" if rc2 == 0 else out2.splitlines()[0][:110]
                if rc2 != 0:
                    n_lfail += 1
                n_done += 1
            entry["chunks"].append(rec)
        entry["done"] = sum(1 for c in entry["chunks"] if c["status"] == "ok")
        entry["total"] = len(entry["chunks"])
        report["chapters"][ch] = entry

    report["totals"] = {"chunks_done": n_done, "chunks_missing": n_missing,
                        "verify_fail": n_vfail, "lint_warn": n_lfail}

    if not args.quiet:
        print(f"{'chapter':<34} {'chunks':>7}  detail")
        print("-" * 78)
        for ch, e in report["chapters"].items():
            marks = "".join({"ok": ".", "MISSING": "M", "VFAIL": "V"}.get(c["status"], "?")
                            for c in e["chunks"])
            print(f"{e['title']:<34} {e['done']:>3}/{e['total']:<3}  {marks}")
        t = report["totals"]
        print("-" * 78)
        print(f"chunks done {t['chunks_done']} | missing {t['chunks_missing']} | "
              f"verify FAIL {t['verify_fail']} | lint warn {t['lint_warn']}")
        if args.verify:
            print("\nFailures:")
            for ch, e in report["chapters"].items():
                for c in e["chunks"]:
                    if c["status"] != "ok":
                        print(f"  {ch}/chunk_{c['chunk']:02d}: {c['status']} "
                              f"{c.get('verify_detail') or c.get('lint') or ''}")
                    elif c.get("lint") != "OK":
                        print(f"  {ch}/chunk_{c['chunk']:02d}: lint -> {c['lint']}")

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())