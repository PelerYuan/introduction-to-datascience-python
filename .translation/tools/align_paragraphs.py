#!/usr/bin/env python3
"""Align EN/ZH paragraph lists by their (byte-identical) role fingerprints.

A mismatch pinpoints text that the translator lost or duplicated. Role-only lines have
no roles themselves, so each paragraph's fingerprint also records whether it consists
solely of a role — that is exactly the paragraph separator the verifier counts.
"""
import difflib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_structure as vs  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROLE = re.compile(r"\{[a-zA-Z-]+\}`[^`]*`")
ROLE_ONLY = re.compile(r"^(?:\{[a-zA-Z-]+\}`[^`]*`|`[^`]*`|\$[^$]*\$|[*_~]+|\s)+$")


def fp(p: str) -> str:
    """Paragraph fingerprint: identical in both languages."""
    stripped = p.strip()
    if ROLE_ONLY.match(stripped):
        return "<<ROLE-ONLY-SEPARATOR>>"
    return " ".join(sorted(ROLE.findall(p)))


def load(path: str) -> list[str]:
    return vs.structure(Path(path).read_text(encoding="utf-8"))["paragraph_list"]


def main() -> int:
    en_path, zh_path = sys.argv[1], sys.argv[2]
    en, zh = load(en_path), load(zh_path)
    print(f"{Path(zh_path).name}: EN {len(en)} | ZH {len(zh)}")
    if len(en) == len(zh) and all(fp(a) == fp(b) for a, b in zip(en, zh)):
        print("  aligned: every paragraph matches by role content")
        return 0
    sm = difflib.SequenceMatcher(None, [fp(p) for p in en], [fp(p) for p in zh], autojunk=False)
    bad = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        bad += 1
        print(f"\n  {tag}  EN[{i1}:{i2}] -> ZH[{j1}:{j2}]")
        for k in range(i1, min(i2, i1 + 2)):
            print(f"    EN[{k}] {en[k][:160]}")
        for k in range(j1, min(j2, j1 + 2)):
            print(f"    ZH[{k}] {zh[k][:160]}")
    print(f"\n  {bad} mismatching region(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())