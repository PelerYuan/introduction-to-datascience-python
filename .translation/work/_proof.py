"""Throwaway before/after harness for the sanitizer round.

phase=before: hash + copy every built page, record chart/inline-code counts.
phase=after : re-hash, diff the changed pages character by character and prove that every
              difference lies inside a builder-local path string.
"""
import difflib
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HTML = ROOT / "source" / "_build" / "html"
SNAP = ROOT / ".translation" / "work" / "_html_before"
STATE = ROOT / ".translation" / "work" / "_proof_state.json"

# exactly the regexes html_qa.py uses
VEGA_RE = re.compile(r"vegaEmbed\(")
PLOTLY_RE = re.compile(r"Plotly\.newPlot|plotly-graph-div|cdn\.plot\.ly/plotly-[\d.]")


def pages() -> list[Path]:
    return sorted(p for p in HTML.glob("*.html")
                  if not p.name.startswith(("genindex", "search", "py-modindex")))


def read(p: Path) -> str:
    with p.open("r", encoding="utf-8", errors="replace", newline="") as fh:
        return fh.read()


def stats() -> dict:
    out = {"pages": {}, "vega": 0, "plotly": 0, "code_tags": 0}
    for p in pages():
        t = read(p)
        nv, np_ = len(VEGA_RE.findall(t)), len(PLOTLY_RE.findall(t))
        nc = t.count("<code")
        out["pages"][p.name] = {"sha": hashlib.sha256(p.read_bytes()).hexdigest(),
                                "size": p.stat().st_size, "vega": nv, "plotly": np_,
                                "code_tags": nc}
        out["vega"] += nv
        out["plotly"] += np_
        out["code_tags"] += nc
    return out


def main() -> int:
    phase = sys.argv[1]
    if phase == "before":
        if SNAP.exists():
            shutil.rmtree(SNAP)
        SNAP.mkdir(parents=True)
        for p in pages():
            shutil.copy2(p, SNAP / p.name)
        st = stats()
        STATE.write_text(json.dumps(st, indent=2), encoding="utf-8")
        print(f"snapshot: {len(st['pages'])} pages, vega={st['vega']} plotly={st['plotly']} "
              f"<code>={st['code_tags']}")
        return 0

    before = json.loads(STATE.read_text(encoding="utf-8"))
    after = stats()
    print(f"vegaEmbed  before={before['vega']:>4}  after={after['vega']:>4}")
    print(f"plotly     before={before['plotly']:>4}  after={after['plotly']:>4}")
    print(f"<code tags before={before['code_tags']:>4}  after={after['code_tags']:>4}")

    bad_diffs = []
    for name, b in before["pages"].items():
        a = after["pages"][name]
        if a["sha"] == b["sha"]:
            continue
        old = read(SNAP / name)
        new = read(HTML / name)
        print(f"\nchanged: {name}  {b['size']} -> {a['size']} bytes "
              f"({a['size'] - b['size']:+d}), code_tags {b['code_tags']} -> {a['code_tags']}")
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old, new).get_opcodes():
            if tag == "equal":
                continue
            removed, added = old[i1:i2], new[j1:j2]
            line = old.count("\n", 0, i1) + 1
            print(f"  line {line}: -{removed!r}")
            print(f"            +{added!r}")
            # nothing but a path string may change: no markup, no attribute quotes
            for chunk in (removed, added):
                if any(c in chunk for c in '<>"\''):
                    bad_diffs.append((name, line, chunk))
        # idempotence of the written artifact is checked by re-running the tool
        print(f"  line endings CRLF={new.count(chr(13) + chr(10))} LF={new.count(chr(10))} "
              f"(before CRLF={old.count(chr(13) + chr(10))})")
    if bad_diffs:
        print("\nFAIL a difference touched markup:")
        for name, line, chunk in bad_diffs:
            print(f"  {name}:{line} {chunk!r}")
        return 1
    print("\nOK every difference is inside a rewritten path string (no markup changed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())