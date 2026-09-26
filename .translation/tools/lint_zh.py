#!/usr/bin/env python3
"""Lint a translated Chinese MyST chapter.

All checks run outside protected regions (front matter, code fences, inline code,
math, URLs, HTML tags, roles).

  1. UNTRANSLATED   >= 6 consecutive English words left in the prose (titles in
                    *italics* are exempt)
  2. AI_FLAVOR      blacklisted machine-translation patterns (STYLE_GUIDE.md section 2)
  3. HALFWIDTH_PUNC half-width , . ; : ? ! used between/after CJK
  4. CJK_LATIN_GAP  missing space between a CJK character and a Latin letter/digit
  5. ROLE_GAP       a {numref}/{glue}/{cite} role glued directly to CJK text
  6. MDASH_ENTITY   a leftover &mdash; in translatable prose
  7. BARE_ENTITY    a leftover HTML entity such as &nbsp; / &amp; in prose
  8. ASCII_QUOTE    straight ASCII quotes " ' used around CJK text

Usage:
    python lint_zh.py --zh ZH.md [--json out.json] [--allow "word1,word2"]
Exit code 0 = clean, 1 = findings.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# The reports are Chinese; a cp1252/cp437 console would raise UnicodeEncodeError while
# printing them and surface as a bogus non-zero exit. Force UTF-8 output regardless.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # pragma: no cover - non-reconfigurable stream
        pass

FRONT_MATTER_RE = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.DOTALL)
FENCE_OPEN_RE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")
ROLE_SPAN_RE = re.compile(r"\{[a-z]+(?::[a-z]+)?\}`[^`]*`")
INLINE_CODE_RE = re.compile(r"``[^`]*``|`[^`\n]+`")
MATH_RE = re.compile(r"\$\$[^$]*\$\$|\$[^$\n]*\$")
HTML_TAG_RE = re.compile(r"<[^>]+>")
LINK_URL_RE = re.compile(r"\]\([^)\s]+(?:\s+\"[^\"]*\")?\)")
IMG_MD_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
AUTOLINK_RE = re.compile(r"https?://\S+")
ITALIC_RE = re.compile(r"\*[^*\n]+\*")
# STYLE_GUIDE §5.7: a work with no established Chinese title keeps its English title
# inside Chinese book-title marks, e.g. 《Good enough practices in scientific computing》.
# Such spans are deliberate, so they are exempt from the untranslated-prose check.
BOOK_TITLE_RE = re.compile(r"《[^》\n]*》")
# A UI label keeps its English so readers can find the button ("GitHub has no Chinese UI"),
# written as `**中文**（English）` with the gloss outside the bold. That gloss is deliberate
# English, so it is exempt from the untranslated-prose check. Without the exemption the
# longest JupyterLab menu item — six Latin words — fails the gate, which forces its gloss
# inside the bold and makes the book's label formatting inconsistent.
UI_GLOSS_RE = re.compile(r"\*\*[^*\n]+\*\*（[A-Za-z][^）\n]*）")
TARGET_RE = re.compile(r"^\([A-Za-z0-9_:\-\.]+\)=\s*$", re.M)
ESCAPED_DOLLAR = "\\$"

CJK_RANGE = r"\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\u3000-\u303f\uff01-\uff60\uffe0-\uffe6"
# Ideographs only: the CJK<->Latin spacing rule applies to these, not to CJK punctuation
CJK_IDEO = r"\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff"

AI_FLAVOR = [
    (r"让我们(?![们])", "「让我们」——原文 Let's 在中文教材里通常省略主语"),
    (r"进行一个[^，。；]{0,12}的(操作|动作|过程)", "「进行一个……的操作」冗余"),
    (r"在[^，。]{0,20}的情况下", "「在……的情况下」——改为「如果……」「当……时」"),
    (r"基于[^，。]{0,20}的基础上", "语义重复"),
    (r"由于[^，。]{0,20}的原因", "语义重复"),
    (r"各种各样的", "改为「各种」"),
    (r"非常(重要|关键|显著)", "改为「很重要」「至关重要」"),
    (r"(相关的|有关的)(内容|数据|信息|知识|方面)", "删掉无意义的修饰"),
    (r"与此同时同时", "同义堆叠"),
    (r"从而使得", "改为「从而」或「使得」"),
    (r"当[^，。]{0,25}的时候", "「当」已含「的时候」"),
    (r"被广泛地认为", "改为「普遍认为」"),
    (r"这是值得注意的", "改为「值得注意的是」"),
    # Only a *bloated* pre-modifier is machine-translation flavour; short natural
    # phrases such as 「一个预测变量的模型」 are idiomatic Chinese and must not fire.
    # The character class excludes sentence punctuation so the match cannot straddle
    # a sentence boundary.
    (r"一个[^，。；：！？、\n]{10,30}的(数据集|数据框|变量|观测|图|模型|问题|方法|函数|过程|结果|包|库)", "冗长定语，考虑改为「该数据集……」或拆句"),
    (r"不仅[^，。]{0,30}而且", "滥用关联词（全章不超过 2 次）"),
    (r"具有[^，。；]{0,15}的特点", "改为「是……」「具有……」"),
    (r"通过[^，。；]{0,20}的方式", "改为「用……」「借助……」"),
    (r"读者(将|可以|能够|需要)", "正文用「你」，不用「读者」"),
    (r"您", "正文用「你」，不用「您」"),
    (r"(是|要)非常(重要|关键)", "语病"),
    (r"进行(学习|研究|分析|讨论)(一下)?$", "空动词，改为具体动词"),
]

WORDS_RE = re.compile(r"[A-Za-z][A-Za-z'\-]*(?:\s+[A-Za-z][A-Za-z'\-]*){5,}")

DEFAULT_ALLOW = {
    # tools, languages, formats
    "pandas", "numpy", "altair", "scikit", "learn", "scikit-learn", "plotly", "seaborn",
    "jupyter", "jupyterlab", "notebook", "github", "gitlab", "git", "docker", "python",
    "anaconda", "conda", "mamba", "markdown", "myst", "html", "css", "json", "yaml",
    "url", "api", "csv", "tsv", "sql", "pdf", "png", "svg", "jpeg", "jpg", "gif", "ai",
    "dataframe", "series", "nan", "pat", "ide", "vscode", "linux", "windows", "macos",
    "ubuntu", "bash", "shell", "terminal", "repo", "crc", "press", "oer", "merlot",
    "creative", "commons", "british", "columbia", "amazon", "routledge", "kaggle",
    "wikipedia", "google", "twitter", "ubc", "dsci", "rss", "ibis", "openpyxl",
}


def split_front_matter(text: str) -> tuple[str, str]:
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return "", text
    return m.group(0), text[m.end():]


def strip_fences_and_code(text: str) -> str:
    """Blank out fenced blocks and front-matter-like YAML, returning readable prose lines."""
    out: list[str] = []
    open_fence = False
    fence_char = ""
    for line in text.splitlines():
        m = FENCE_OPEN_RE.match(line)
        if not open_fence:
            if m:
                open_fence = True
                fence_char = m.group(2)[0]
                out.append("")
                continue
            out.append(line)
        else:
            if m and m.group(2)[0] == fence_char:
                open_fence = False
            out.append("")
    return "\n".join(out)


def to_prose(text: str) -> str:
    """Fences/code stripped and inline non-prose (urls, math, code, tags) replaced by spaces."""
    s = strip_fences_and_code(text)
    s = HTML_TAG_RE.sub(" ", s)
    s = IMG_MD_RE.sub(" ", s)
    s = LINK_URL_RE.sub("] ", s)
    s = AUTOLINK_RE.sub(" ", s)
    s = MATH_RE.sub(" ", s.replace(ESCAPED_DOLLAR, "\\\x00"))
    s = INLINE_CODE_RE.sub(" ", s)
    s = TARGET_RE.sub("", s)
    return s


def paragraph_count(text: str) -> int:
    """Number of non-blank runs in fence-stripped prose."""
    s = strip_fences_and_code(text)
    count = 0
    prev_blank = True
    for line in s.splitlines():
        if line.strip():
            if prev_blank:
                count += 1
            prev_blank = False
        else:
            prev_blank = True
    return count


def lint(zh_body: str, allow: set[str]) -> list[dict]:
    findings: list[dict] = []
    no_roles = ROLE_SPAN_RE.sub(" ", to_prose(zh_body))
    keep_roles = to_prose(zh_body)

    # 1. untranslated English runs (italic spans exempt)
    for i, line in enumerate(no_roles.splitlines(), 1):
        # UI_GLOSS_RE must run BEFORE ITALIC_RE: ITALIC_RE pairs the inner stars of a
        # `**bold**` span, so `**中文**（English）` becomes `* *（English）` and the
        # `**...**（` adjacency this exemption needs is already gone.
        scrubbed = UI_GLOSS_RE.sub(" ", line)
        scrubbed = ITALIC_RE.sub(" ", scrubbed)
        scrubbed = BOOK_TITLE_RE.sub(" ", scrubbed)
        for m in WORDS_RE.finditer(scrubbed):
            words = [w.lower().strip("'-") for w in m.group(0).split()]
            if all(w in allow for w in words):
                continue
            findings.append({"code": "UNTRANSLATED", "line": i,
                             "text": m.group(0)[:140], "why": "疑似未翻译的英文散文"})

    # 2. AI flavour
    for i, line in enumerate(no_roles.splitlines(), 1):
        for rx, why in AI_FLAVOR:
            for m in re.finditer(rx, line):
                findings.append({"code": "AI_FLAVOR", "line": i,
                                 "text": m.group(0), "why": why})

    # 3. half-width punctuation
    for i, line in enumerate(no_roles.splitlines(), 1):
        for m in re.finditer(rf"[{CJK_RANGE}][,;:!?][{CJK_RANGE}]", line):
            findings.append({"code": "HALFWIDTH_PUNC", "line": i, "text": m.group(0),
                             "why": "中文之间应使用全角标点"})
        for m in re.finditer(rf"[{CJK_RANGE}]\.(?=\s|$)", line):
            findings.append({"code": "HALFWIDTH_PUNC", "line": i, "text": m.group(0),
                             "why": "句末应使用全角句号「。」"})
        for m in re.finditer(rf"[{CJK_RANGE}]\s*,\s*[{CJK_RANGE}]", line):
            findings.append({"code": "HALFWIDTH_PUNC", "line": i, "text": m.group(0),
                             "why": "使用了半角逗号"})

    # 4. CJK <-> Latin spacing (ideographs only; full-width punctuation needs no space)
    for i, line in enumerate(no_roles.splitlines(), 1):
        for m in re.finditer(rf"[{CJK_IDEO}][A-Za-z0-9]", line):
            findings.append({"code": "CJK_LATIN_GAP", "line": i, "text": m.group(0),
                             "why": "中文与西文之间应加一个半角空格"})
        for m in re.finditer(rf"[A-Za-z0-9][{CJK_IDEO}]", line):
            findings.append({"code": "CJK_LATIN_GAP", "line": i, "text": m.group(0),
                             "why": "西文与中文之间应加一个半角空格"})

    # 5. roles glued to CJK
    role_rx = re.compile(r"(?:\{[a-z]+(?::[a-z]+)?\}`[^`\n]*`)|(?:`[^`\n]*`)")
    for i, line in enumerate(keep_roles.splitlines(), 1):
        for m in role_rx.finditer(line):
            before = line[m.start() - 1] if m.start() > 0 else ""
            after = line[m.end()] if m.end() < len(line) else ""
            if re.match(rf"[{CJK_IDEO}]", before) or re.match(rf"[{CJK_IDEO}]", after):
                # a CJK char directly abutting a role is fine only for archetypal
                # punctuation-free cases; flag it for review
                findings.append({"code": "ROLE_GAP", "line": i,
                                 "text": (before + m.group(0) + after)[:90],
                                 "why": "角色与中文之间应加空格或标点间隔"})

    # 6/7. leftover entities
    for i, line in enumerate(no_roles.splitlines(), 1):
        for m in re.finditer(r"&(mdash|ndash|nbsp|amp|lt|gt|quot|hellip|#\d+);", line):
            findings.append({"code": "BARE_ENTITY", "line": i, "text": m.group(0),
                             "why": "正文中的 HTML 实体应改为对应的中文符号"})

    # 8. ASCII quotes around Chinese
    for i, line in enumerate(no_roles.splitlines(), 1):
        for m in re.finditer(rf"\"[{CJK_RANGE}][^\"]{{0,40}}[{CJK_RANGE}]?\"", line):
            findings.append({"code": "ASCII_QUOTE", "line": i, "text": m.group(0)[:80],
                             "why": "中文引号应使用「\" \"」全角弯引号"})
    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--zh", type=Path, required=True)
    ap.add_argument("--json", type=Path, default=None)
    ap.add_argument("--allow", default="")
    ap.add_argument("--max-show", type=int, default=6)
    args = ap.parse_args()

    allow = set(DEFAULT_ALLOW)
    allow.update(w.strip().lower() for w in args.allow.split(",") if w.strip())

    raw = args.zh.read_text(encoding="utf-8")
    _, body = split_front_matter(raw)
    findings = lint(body, allow)

    by_code: dict[str, list[dict]] = {}
    for f in findings:
        by_code.setdefault(f["code"], []).append(f)

    no_roles = ROLE_SPAN_RE.sub(" ", to_prose(body))
    stats = {
        "file": str(args.zh),
        "paragraphs": paragraph_count(body),
        "han_chars": len(re.findall(rf"[{CJK_RANGE}]", no_roles)),
        "ascii_words": len(re.findall(r"[A-Za-z]{2,}", no_roles)),
        "findings": len(findings),
        "by_code": {k: len(v) for k, v in sorted(by_code.items())},
    }
    if args.json:
        args.json.write_text(json.dumps({"stats": stats, "findings": findings},
                                       ensure_ascii=False, indent=2), encoding="utf-8")

    if not findings:
        print(f"OK   {args.zh.name}: clean ({stats['han_chars']} 汉字, "
              f"{stats['paragraphs']} 段落, {stats['ascii_words']} ASCII 词)")
        return 0

    print(f"WARN {args.zh.name}: {len(findings)} 项  {stats['by_code']}  "
          f"({stats['han_chars']} 汉字, {stats['paragraphs']} 段落)")
    for code, items in by_code.items():
        print(f"  [{code}] {len(items)}")
        for it in items[: args.max_show]:
            print(f"     L{it['line']}: {it['text']!r} -> {it['why']}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())