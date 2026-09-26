#!/usr/bin/env python3
r"""Rewrite the builder's own absolute paths out of the built HTML.

The book teaches by letting code fail on purpose, and a cell that fails renders its
traceback. On the machine that builds this Chinese edition those tracebacks name *this*
machine:

    File D:\Translation\Data Science A First Introduction with Python\.venv-build\
    lib\site-packages\ibis\expr\types\relations.py:1222, in Table.__getattr__

The English edition is built in the project's own Docker image, so its readers see
`/opt/conda/lib/python3.10/site-packages/ibis/...` and `/home/jovyan/work/...` instead.
Docker is not available here, so the finished pages are rewritten after the build to the
paths that image would have produced.

Rewriting is the only option that keeps the book honest. The failing cells are the
book's teaching style and must stay in, while the cells themselves must stay
byte-identical to the English source (`verify_structure.py` compares code-block hashes),
so neither `%xmode Minimal` nor an edited cell is available.

Only path strings are touched. Chart JavaScript is not: every rule is anchored on a path
this build actually owns — the repository root, `.venv-build`, a Windows temp directory,
a user profile, the notebook execution directory — and none of those strings occur in
the vega/plotly bundles that make up most of the bytes of the big pages.

Every root is derived from this file's own location, never from a hard-coded drive or
user name, so the tool works on a clone that lives anywhere.

Usage:
    python sanitize_paths.py [--dir source/_build/html]      # rewrite, print a summary
    python sanitize_paths.py --check                         # gate: list leaks, change nothing
Exit codes: 0 = rewrote / nothing left to rewrite, 1 = --check found a leak (or a file
could not be read or written), 2 = no build output to work on.
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path
from typing import Callable, NamedTuple

# The report quotes paths and Chinese file names; force UTF-8 so a cp1252 console cannot
# turn a successful run into a UnicodeEncodeError.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # pragma: no cover
        pass

ROOT = Path(__file__).resolve().parents[2]
HTML_DIR = ROOT / "source" / "_build" / "html"
VENV = ROOT / ".venv-build"

# The paths the upstream Docker image shows: what a reader of the published book must see.
CONDA = "/opt/conda"
CONDA_SITE = "/opt/conda/lib/python3.10/site-packages"
WORK = "/home/jovyan/work"
HOME = "/home/jovyan"
TMP = "/tmp"

SEP = r"[\\/]"
DRIVE = r"[A-Za-z]:"
# One path component. `:` is excluded so a trailing `:1222,` (a traceback line number)
# ends the path, and `<>"'` are excluded so a rewrite can never eat an HTML tag or an
# attribute quote. The character class is separate from the quantifier so a rule can ask
# for a component of a minimum length.
COMP_CHAR = r"[^\s\\/\"'<>|:*?]"
COMP = rf"{COMP_CHAR}+"
# A component may contain spaces — this repository is called
# `Data Science A First Introduction with Python` — but a space is only allowed inside a
# component that is *followed by another separator*. Without that guard the tail of a path
# would swallow the sentence after it and normalise separators inside prose, which is
# exactly the kind of collateral damage this tool must not do.
COMP_SP = rf"{COMP}(?:[ \t](?={COMP}{SEP}){COMP})*"
# What may still belong to a path once its machine-specific part has been replaced:
# further components, so their separators can be normalised too
# (`…/site-packages\ibis\expr\relations.py` → `…/site-packages/ibis/expr/relations.py`).
TAIL = rf"(?:{SEP}{COMP_SP})*{SEP}?"

def _lit(path: Path | str) -> str:
    """Regex source for a specific absolute path.

    Separator runs become `[\\/]+` so the pattern matches the forward-slash form as well,
    which is what lets a rewritten path come out POSIX. Case is handled by the IGNORECASE
    flag on every rule: the same Windows path is spelled with different case depending on
    which library printed it.
    """
    out = []
    for ch in str(path):
        out.append(rf"{SEP}+" if ch in "\\/" else re.escape(ch))
    return "".join(out)


def _norm(tail: str) -> str:
    """A rewritten path is a POSIX path: its own separators become forward slashes."""
    return tail.replace("\\", "/")


class Rule(NamedTuple):
    name: str
    pattern: re.Pattern[str]
    repl: Callable[[re.Match[str]], str]


def _notebook_dir() -> str:
    """`[<repo root>\\]source\\_build\\jupyter_execute\\`, in either separator style."""
    return rf"(?:{_lit(ROOT)}{SEP}+)?source{SEP}+_build{SEP}+jupyter_execute{SEP}+"


def _windows_temp() -> str:
    """`C:\\Users\\<user>\\AppData\\Local\\Temp`, whatever the user and drive are."""
    return rf"{DRIVE}{SEP}+(?:{COMP}{SEP}+)*?AppData{SEP}+Local{SEP}+Temp"


def build_rules() -> list[Rule]:
    rules: list[Rule] = []

    def add(name: str, pattern: str, repl: Callable[[re.Match[str]], str]) -> None:
        rules.append(Rule(name, re.compile(pattern, re.IGNORECASE), repl))

    # 1. The notebook a cell ran in, as a traceback names it:
    #    `File …\source\_build\jupyter_execute\reading.ipynb` → the path the Docker image
    #    keeps the book at. The `source\_build\jupyter_execute\` part is an artifact of
    #    building here at all, so it goes; `/home/jovyan/work/<name>.ipynb` is what the
    #    upstream site shows for the same cell.
    add("notebook execution directory",
        _notebook_dir() + rf"(?P<name>{COMP})(?P<tail>{TAIL})",
        lambda m: f"{WORK}/{m.group('name')}{_norm(m.group('tail'))}")

    # 2. The build virtualenv's third-party packages → the conda environment's.
    add("build venv site-packages",
        rf"(?:{_lit(ROOT)}{SEP}+)?{_lit('.venv-build')}{SEP}+lib{SEP}+site-packages(?P<tail>{TAIL})",
        lambda m: CONDA_SITE + _norm(m.group("tail")))

    # 3. A bare `sys.executable`: the venv spells it `Scripts\python.exe`, conda `bin/python`.
    add("build venv interpreter",
        rf"(?:{_lit(ROOT)}{SEP}+)?{_lit('.venv-build')}{SEP}+Scripts{SEP}+python\.exe(?P<tail>{TAIL})",
        lambda m: f"{CONDA}/bin/python" + _norm(m.group("tail")))

    # 4. Anything else under the venv root.
    add("build venv root",
        rf"(?:{_lit(ROOT)}{SEP}+)?{_lit('.venv-build')}(?P<tail>{TAIL})",
        lambda m: CONDA + _norm(m.group("tail")))

    # 5. IPython writes the code it executes to a temporary file, and warnings and
    #    tracebacks quote that file. On Windows it is
    #    `C:\Users\<user>\AppData\Local\Temp\<dir>\ipykernel_<pid>\<n>.py`; in the Docker
    #    image it is `/tmp/ipykernel_<pid>/<n>.py`. The `<dir>` between is the private temp
    #    directory this harness hands the build, so it is dropped rather than published:
    #    reproducing upstream exactly is both the honest fix and the one that leaks least.
    add("temporary ipykernel file",
        rf"(?:{_lit(tempfile.gettempdir())}|{_windows_temp()})(?:{SEP}+{COMP})?"
        rf"{SEP}+(?P<tail>ipykernel_\d+{TAIL})",
        lambda m: f"{TMP}/{_norm(m.group('tail'))}")

    # 6. Any other temporary file: only the temp root is machine-specific, everything
    #    below it is a file name the reader is meant to see.
    add("temporary file",
        rf"(?:{_lit(tempfile.gettempdir())}|{_windows_temp()})(?P<tail>{TAIL})",
        lambda m: TMP + _norm(m.group("tail")))

    # 7. Anything else inside a Windows user profile (`C:\Users\<user>\…`), which is where
    #    matplotlib, joblib and Jupyter caches end up when they are not pinned into the repo.
    add("user profile",
        rf"{DRIVE}{SEP}+Users{SEP}+{COMP}(?P<tail>{TAIL})",
        lambda m: HOME + _norm(m.group("tail")))

    # 8. Anything else under the repository root — `.build-cache`, `_build\html`, a data
    #    file. Last, because the rules above already claim the paths whose neutral form is
    #    not simply "the same path somewhere else".
    add("repository root",
        rf"{_lit(ROOT)}(?P<tail>{TAIL})",
        lambda m: WORK + _norm(m.group("tail")))

    return rules


def leak_patterns() -> list[tuple[str, re.Pattern[str]]]:
    """What `--check` refuses to let through: the same leaks the rules above rewrite."""
    return [
        # A drive letter followed by two or more *backslash*-separated components, the
        # first of them at least two characters long. Every clause is measured against
        # this book's own chart bundles, which ship vega and plotly inline:
        #   * the separator must be a backslash. Those bundles are full of
        #     `{E:/[^\s,]+/g,` — a minified object key, a colon and a JavaScript regex
        #     literal, which reads exactly like `X:/a/b` if forward slashes are accepted
        #     (120 false findings, all of them inside chart code);
        #   * two components minimum, because the same bundles contain `X:\n` escapes
        #     (`… y = a:\n  // …`) that a bare `[A-Za-z]:\\` matches 27 times;
        #   * a first component of two characters or more, because consecutive escapes
        #     look like a two-component path (`t:\n\n` appears three times).
        # The cost is a genuine single-component path such as `C:\tmp`, which this book
        # never renders; the repository root, the venv and the temp directory are matched
        # literally below, so the paths that actually leaked here are all still caught.
        ("windows drive path", re.compile(rf"{DRIVE}\\{COMP_CHAR}{{2,}}(?:\\{COMP})+")),
        # A macOS home directory: `/Users/<name>/`. The trailing separator is required, so
        # `https://www.stat.ubc.ca/users/melissa-lee` in the authors chapter is not a leak.
        ("macOS home directory", re.compile(r"(?i:/Users/[^/\s\"'<>]+/)")),
        ("repository root", re.compile(_lit(ROOT), re.IGNORECASE)),
        ("build venv root", re.compile(_lit(VENV), re.IGNORECASE)),
        ("AppData path", re.compile(r"(?i)AppData")),
        # `/tmp/ipykernel_12/2654974267.py` is *content*, not a leak: the wrangling chapter
        # prints that warning text deliberately and the English source carries the same
        # line, so only a temp path that is not already a neutral `/tmp` one counts.
        ("builder temp path", re.compile(r"(?i)(?<!/tmp/)ipykernel_\d+")),
    ]


def read_page(page: Path) -> str:
    """Read a page without touching its line endings.

    The built pages use CRLF and the tools use LF; letting the text layer translate either
    one would rewrite every line of a file this tool is only allowed to touch inside path
    strings.
    """
    with page.open("r", encoding="utf-8", errors="replace", newline="") as fh:
        return fh.read()


def write_page(page: Path, text: str) -> None:
    with page.open("w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def sanitize(text: str, rules: list[Rule]) -> tuple[str, dict[str, int]]:
    """Apply every rule once, in order, and count what each one changed."""
    counts: dict[str, int] = {}
    for rule in rules:
        text, n = rule.pattern.subn(rule.repl, text)
        if n:
            counts[rule.name] = counts.get(rule.name, 0) + n
    return text, counts


def run_check(pages: list[Path], max_show: int) -> int:
    leaks: list[tuple[Path, int, str, str]] = []
    patterns = leak_patterns()
    for page in pages:
        try:
            text = read_page(page)
        except OSError as exc:
            print(f"FAIL cannot read {page}: {exc}")
            return 1
        for label, rx in patterns:
            for m in rx.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                leaks.append((page, line, label, m.group(0)))

    for page, line, label, match in leaks[:max_show]:
        shown = match if len(match) <= 120 else match[:117] + "..."
        print(f"  {page.name}:{line}  {label}: {shown}")
    if len(leaks) > max_show:
        print(f"  ... and {len(leaks) - max_show} more")

    files = len({p for p, *_ in leaks})
    if leaks:
        print(f"FAIL {len(leaks)} builder-local path(s) in {files} html file(s)")
        return 1
    print(f"OK   no builder-local paths in {len(pages)} html file(s)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Rewrite builder-local paths in the built HTML.")
    ap.add_argument("--dir", type=Path, default=HTML_DIR,
                    help="built HTML directory (default: source/_build/html)")
    ap.add_argument("--check", action="store_true",
                    help="change nothing; list remaining local paths and exit non-zero")
    ap.add_argument("--max-show", type=int, default=10,
                    help="how many leaks --check prints before summarising (default 10)")
    args = ap.parse_args()

    if not args.dir.exists():
        print(f"no built HTML at {args.dir} - run tools/build_book.ps1 first")
        return 2

    pages = sorted(args.dir.rglob("*.html"))
    if args.check:
        return run_check(pages, args.max_show)

    rules = build_rules()
    total = changed_files = 0
    failures: list[str] = []
    for page in pages:
        try:
            text = read_page(page)
        except OSError as exc:
            failures.append(f"{page}: {exc}")
            continue
        new, counts = sanitize(text, rules)
        if not counts:
            continue
        if new == text:  # impossible in practice; never rewrite a file for nothing
            continue
        try:
            write_page(page, new)
        except OSError as exc:
            failures.append(f"{page}: {exc}")
            continue
        n = sum(counts.values())
        total += n
        changed_files += 1
        detail = ", ".join(f"{k} x{v}" for k, v in sorted(counts.items()))
        print(f"sanitized {page.name}: {n} replacement(s) - {detail}")

    print(f"total: {total} replacement(s) in {changed_files} of {len(pages)} html file(s)")
    if failures:
        for f in failures:
            print(f"FAIL {f}")
        return 1
    # The rewritten pages are verified by html_qa.py, which is the gate that failed to
    # notice this class of leak in the first place; this tool reports, it does not judge.
    return 0


if __name__ == "__main__":
    sys.exit(main())