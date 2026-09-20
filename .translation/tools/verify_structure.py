#!/usr/bin/env python3
"""Compare the *protected structure* of an English MyST chapter with its Chinese translation.

Reports every structural difference. Any difference is a defect in the translation
unless it is explicitly in the allowed-to-change set (visible prose, captions,
headings, index terms, numref custom text).

Usage:
    python verify_structure.py --en EN.md --zh ZH.md [--json out.json]
Exit code 0 = structurally identical, 1 = differences found.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

# Reports contain Chinese and code excerpts; force UTF-8 so a cp1252 console cannot
# turn a clean run into a UnicodeEncodeError with a non-zero exit.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # pragma: no cover
        pass

FENCE_OPEN_RE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")
FRONT_MATTER_RE = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.DOTALL)

CODE_DIRECTIVES = {"code-cell", "code-block"}
OPTION_LINE_RE = re.compile(r"^\s*:[A-Za-z_][A-Za-z0-9_-]*:")
# Directives whose info line carries *translatable* visible text (a title, a table
# caption, or `{index}` terms) rather than an invariant identifier or path.
# For these, only the option lines are compared; the text itself is prose.
TITLED_DIRECTIVES = {
    "index", "list-table", "table", "admonition", "note", "tip", "warning",
    "important", "caution", "seealso", "epigraph", "dropdown", "margin", "sidebar",
}
ROLE_RE = re.compile(r"\{([a-z]+(?::[a-z]+)?)\}`([^`]*)`")
INLINE_CODE_RE = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)")
MATH_RE = re.compile(r"\${1,2}[^$]+\${1,2}")
ESCAPED_DOLLAR = "\\$"
# Translators may append a provisional terminology register; the assembler strips it
# before the chapter is written, so the verifier must ignore it too.
TERM_BLOCK_RE = re.compile(r"<<TERM>>.*?<<END>>", re.DOTALL)
LINK_RE = re.compile(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
IMG_SRC_RE = re.compile(r"<img[^>]*?src=\"([^\"]+)\"")
TARGET_RE = re.compile(r"^\(([A-Za-z0-9_:\-\.]+)\)=\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


def h(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]


def strip_front_matter(text: str) -> tuple[str, str]:
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return "", text
    return m.group(0), text[m.end():]


def parse_blocks(text: str) -> list[dict]:
    """Return a list of blocks: prose runs and fenced blocks."""
    lines = text.splitlines(keepends=True)
    blocks: list[dict] = []
    buf: list[str] = []
    i = 0
    while i < len(lines):
        m = FENCE_OPEN_RE.match(lines[i])
        if m:
            if buf:
                blocks.append({"kind": "prose", "text": "".join(buf)})
                buf = []
            indent, fence, info = m.group(1), m.group(2), m.group(3).strip()
            body: list[str] = []
            i += 1
            while i < len(lines):
                cm = FENCE_OPEN_RE.match(lines[i])
                if cm and cm.group(2)[0] == fence[0] and len(cm.group(2)) >= len(fence):
                    i += 1
                    break
                body.append(lines[i])
                i += 1
            blocks.append({"kind": "fence", "fence": fence, "info": info, "body": "".join(body)})
        else:
            buf.append(lines[i])
            i += 1
    if buf:
        blocks.append({"kind": "prose", "text": "".join(buf)})
    return blocks


def directive_name(info: str) -> str:
    m = re.match(r"\{([^}]+)\}", info)
    if m:
        return m.group(1).strip()
    return ""


def structure(text: str) -> dict:
    text = TERM_BLOCK_RE.sub("", text)
    fm, body = strip_front_matter(text)
    blocks = parse_blocks(body)
    prose_all = "".join(b["text"] for b in blocks if b["kind"] == "prose")

    code_hashes: list[str] = []
    directives: list[tuple[str, str]] = []   # (name, normalized-options)
    index_struct: list[str] = []
    targets: list[str] = []

    for b in blocks:
        if b["kind"] != "fence":
            continue
        name = directive_name(b["info"])
        body_lines = b["body"].splitlines()
        if not name or name in CODE_DIRECTIVES:
            code_hashes.append(h(b["body"].rstrip("\n")))
            continue
        # directive: keep the directive name, the info-line remainder, and option lines
        info_rest = b["info"][len(name) + 2:].strip() if name else b["info"]
        opts = [l.strip() for l in body_lines if OPTION_LINE_RE.match(l)]
        # YAML option block between --- markers inside directives
        yaml_opts = []
        inside_yaml = False
        for l in body_lines:
            if l.strip() == "---":
                inside_yaml = not inside_yaml
                continue
            if inside_yaml:
                yaml_opts.append(l.strip())
        # For titled directives the info-line text is visible prose (translatable), so
        # only the directive name and its option lines are invariant.
        info_cmp = "" if name in TITLED_DIRECTIVES else info_rest
        directives.append((name, json.dumps([info_cmp, opts, yaml_opts], ensure_ascii=False)))
        if name == "index":
            for l in body_lines:
                s = l.strip()
                if not s:
                    continue
                index_struct.append(f"see:{s.startswith('see:')}|semicolons:{s.count(';')}")

    for line in prose_all.splitlines():
        if TARGET_RE.match(line):
            targets.append(TARGET_RE.match(line).group(1))

    roles = Counter()
    for name, content in ROLE_RE.findall(prose_all):
        if name in ("cite:p", "cite:ps", "cite:t", "glue:text", "glue:figure", "glue:table"):
            roles[f"{name}:{content.strip()}"] += 1
        elif name == "numref":
            m = re.search(r"<([^>]+)>\s*$", content)
            key = m.group(1) if m else content.strip()
            roles[f"numref:{key}"] += 1
        else:
            roles[f"{name}:{content.strip()}"] += 1

    # inline code spans, excluding those inside roles
    prose_wo_roles = ROLE_RE.sub(" ", prose_all)
    # Escaped dollars (\$) are literal currency signs, not math delimiters. Without
    # neutralising them the MATH_RE pairs two escaped dollars and swallows the prose
    # between them, which makes the `math` field compare translatable text.
    math_src = prose_wo_roles.replace(ESCAPED_DOLLAR, "\\\x00")
    inline_codes = Counter(m.group(2).strip() for m in INLINE_CODE_RE.finditer(prose_wo_roles))
    math = Counter(m.group(0).strip() for m in MATH_RE.finditer(math_src))
    urls = Counter(m.group(1) for m in LINK_RE.finditer(prose_all))
    urls.update(IMG_SRC_RE.findall(prose_all))
    headings = [len(m.group(1)) for m in (HEADING_RE.match(l) for l in prose_all.splitlines()) if m]
    plusplus = sum(1 for l in prose_all.splitlines() if l.strip() == "+++")
    # Paragraphs are counted on the *unmodified* prose lines. Roles are stripped to
    # compare translatable text, but that turns a line holding only a role
    # (`{numref}`fig:x``) into an empty line — which would read as a paragraph break even
    # though the renderer shows it inline. Both languages are measured the same way, so
    # counting before stripping keeps the comparison meaningful.
    paragraphs = 0
    prev_blank = True
    paragraph_list: list[str] = []
    cur: list[str] = []
    for l in prose_all.splitlines():
        if l.strip():
            if prev_blank:
                paragraphs += 1
            prev_blank = False
            cur.append(l.strip())
        else:
            if cur:
                paragraph_list.append(" ".join(cur))
                cur = []
            prev_blank = True
    if cur:
        paragraph_list.append(" ".join(cur))

    return {
        "front_matter": h(fm) if fm else "NONE",
        "code_blocks": sorted(code_hashes),
        "code_block_count": len(code_hashes),
        "directives": sorted(directives),
        "directive_count": len(directives),
        "index_struct": index_struct,
        "targets": targets,
        "roles": roles,
        "inline_codes": inline_codes,
        "math": math,
        "urls": urls,
        "heading_levels": headings,
        "plusplus": plusplus,
        "paragraphs": paragraphs,
        "paragraph_list": paragraph_list,
    }


def comparable(s: dict) -> dict:
    """Fields where exact equality is required (multisets as sorted lists)."""
    return {
        "front_matter": s["front_matter"],
        "code_blocks": s["code_blocks"],
        "directives": s["directives"],
        "index_struct": s["index_struct"],
        "targets": s["targets"],
        "roles": sorted(s["roles"].items()),
        "inline_codes": sorted(s["inline_codes"].items()),
        "math": sorted(s["math"].items()),
        "urls": sorted(s["urls"].items()),
        "heading_levels": s["heading_levels"],
        "plusplus": s["plusplus"],
        "paragraphs": s["paragraphs"],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--en", type=Path, required=True)
    ap.add_argument("--zh", type=Path, required=True)
    ap.add_argument("--json", type=Path, default=None)
    ap.add_argument("--quiet-ok", action="store_true")
    args = ap.parse_args()

    en = structure(args.en.read_text(encoding="utf-8"))
    zh = structure(args.zh.read_text(encoding="utf-8"))
    a, b = comparable(en), comparable(zh)

    issues: list[dict] = []
    for key in a:
        if key == "front_matter":
            # A chunk source has no front matter (the assembler owns it, and some
            # translators prepend a copy). Only compare when both sides have one.
            if a[key] != "NONE" and a[key] != b[key]:
                issues.append({"field": key, "detail": f"EN={a[key]!r} ZH={b[key]!r}"})
            continue
        if key in ("plusplus", "paragraphs"):
            if a[key] != b[key]:
                issues.append({"field": key, "detail": f"EN={a[key]!r} ZH={b[key]!r}"})
            continue
        if key in ("code_blocks", "directives", "index_struct", "heading_levels", "targets"):
            if a[key] != b[key]:
                only_en = [x for x in a[key] if x not in b[key]]
                only_zh = [x for x in b[key] if x not in a[key]]
                issues.append({"field": key,
                               "detail": f"missing_in_zh={len(only_en)} extra_in_zh={len(only_zh)}",
                               "missing_in_zh": [str(x)[:160] for x in only_en][:12],
                               "extra_in_zh": [str(x)[:160] for x in only_zh][:12]})
            continue
        ca, cb = Counter(dict(a[key])), Counter(dict(b[key]))
        if ca != cb:
            missing = ca - cb
            extra = cb - ca
            issues.append({"field": key,
                           "detail": f"missing_in_zh={sum(missing.values())} extra_in_zh={sum(extra.values())}",
                           "missing_in_zh": [f"{k} x{v}" for k, v in list(missing.items())[:12]],
                           "extra_in_zh": [f"{k} x{v}" for k, v in list(extra.items())[:12]]})

    report = {"en": str(args.en), "zh": str(args.zh), "ok": not issues, "issues": issues,
              "stats": {"code_blocks": en["code_block_count"], "directives": en["directive_count"],
                        "targets": len(en["targets"]), "roles": sum(en["roles"].values()),
                        "inline_codes": sum(en["inline_codes"].values())}}
    if args.json:
        args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if not issues:
        if not args.quiet_ok:
            print(f"OK  {args.zh.name}: structure matches "
                  f"({en['code_block_count']} code blocks, {en['directive_count']} directives, "
                  f"{len(en['targets'])} targets, {sum(en['roles'].values())} roles)")
    else:
        print(f"FAIL {args.zh.name}: {len(issues)} structural difference(s)")
        for it in issues:
            print(f"  - {it['field']}: {it['detail']}")
            for x in it.get("missing_in_zh", [])[:5]:
                print(f"      missing: {x}")
            for x in it.get("extra_in_zh", [])[:5]:
                print(f"      extra:   {x}")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())