"""Throwaway inventory scan: what machine-local path strings exist in the built HTML?"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HTML = ROOT / "source" / "_build" / "html"

PATS = {
    "win_drive": re.compile(r"[A-Za-z]:\\"),
    "win_drive_fwd": re.compile(r"[A-Za-z]:/"),
    "users_mac": re.compile(r"/Users/"),
    "appdata": re.compile(r"AppData", re.I),
    "ipykernel": re.compile(r"ipykernel_\d+"),
    "venv": re.compile(r"\.venv-build", re.I),
    "jexec": re.compile(r"jupyter_execute", re.I),
    "repo_root": re.compile(re.escape(str(ROOT)), re.I),
    "tmp": re.compile(r"/tmp/"),
    "file_line": re.compile(r"File [\"']?[^\s<>\"']+"),
    "site_packages": re.compile(r"site-packages"),
    "backslash": re.compile(r"\\\\"),
}

def main() -> int:
    targets = sorted(HTML.rglob("*.html"))
    print(f"scanning {len(targets)} html files under {HTML}")
    totals = {k: 0 for k in PATS}
    for p in targets:
        t = p.read_text(encoding="utf-8", errors="replace")
        hits = {}
        for k, rx in PATS.items():
            n = len(rx.findall(t))
            totals[k] += n
            if n:
                hits[k] = n
        if hits:
            print(f"\n### {p.relative_to(HTML)}  {hits}")
            for k in hits:
                if k in ("backslash", "tmp", "site_packages", "file_line", "win_drive"):
                    for m in list(PATS[k].finditer(t))[:6]:
                        s = max(0, m.start() - 60)
                        print(f"   [{k}] …{t[s:m.end() + 80]}…".replace("\n", "\\n"))
    print("\n=== totals ===")
    for k, v in totals.items():
        print(f"{k:14} {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())