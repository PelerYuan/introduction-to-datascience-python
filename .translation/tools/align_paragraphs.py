#!/usr/bin/env python3
"""Prove that no role or inline construct was lost while the translation was edited.

This began as a one-off forensic tool for a real incident: a bug in `fix_spacing.py`
mutated the line it was iterating over, and stale match offsets deleted arbitrary text.
Paragraph counts alone did not reveal it, because the damage did not change how many
paragraphs there were. Comparing paragraphs by the roles they contain did reveal it.

The check it performs now is narrower and does not depend on how prose happens to wrap:

* paragraph counts must match (that is also what verify_structure.py asserts), and
* the chapter-wide multiset of MyST roles must match.

Roles are compared as a multiset rather than in order, because Chinese legitimately
reorders them within a sentence ("recall from {numref}`x` that ..." -> "回想一下
{numref}`x` 中 ..."). Per-paragraph fingerprints are deliberately *not* compared: a
paragraph holding only a role may legitimately be absorbed into its neighbour, since
CommonMark would otherwise render the line break between them as a stray space.
"""
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_structure as vs  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROLE = re.compile(r"\{([a-zA-Z:-]+)\}`([^`]*)`")
TARGET = re.compile(r"<([^>]*)>")


def norm_role(m: re.Match) -> str:
    """Fingerprint a role by its *target*, not its display text.

    The book localises numref display text on purpose: the English source writes
    ``{numref}`Chapter %s <wrangling>``` and the Chinese writes
    ``{numref}`第 %s 章 <wrangling>```. Both point at the same target, so the target is
    what must be identical on both sides — comparing the whole role would report that
    deliberate localisation as content loss.
    """
    name, content = m.group(1), m.group(2)
    target = TARGET.search(content)
    return f"{{{name}}}<{target.group(1) if target else content.strip()}>"


def load(path: str) -> tuple[int, Counter]:
    """(paragraph count, role multiset) for one chapter."""
    text = Path(path).read_text(encoding="utf-8")
    info = vs.structure(text)
    body = "\n".join(info["paragraph_list"])
    return len(info["paragraph_list"]), Counter(norm_role(m) for m in ROLE.finditer(body))


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    en_path, zh_path = sys.argv[1], sys.argv[2]
    name = Path(zh_path).name
    (en_n, en_roles), (zh_n, zh_roles) = load(en_path), load(zh_path)

    problems = []
    if en_n != zh_n:
        problems.append(f"paragraphs: EN={en_n} ZH={zh_n}")
    missing, extra = en_roles - zh_roles, zh_roles - en_roles
    for role, count in sorted(missing.items()):
        problems.append(f"missing x{count}: {role}")
    for role, count in sorted(extra.items()):
        problems.append(f"unexpected x{count}: {role}")

    if problems:
        print(f"FAIL {name}: {len(problems)} difference(s)")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"OK   {name}: {zh_n} paragraphs, {sum(zh_roles.values())} roles, no content lost")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())