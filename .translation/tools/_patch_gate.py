# -*- coding: utf-8 -*-
"""Add the inline-code allowlist to verify_structure.py (the edit tool needs a prior read,
so the patch is applied here with its own assertions)."""
import pathlib

p = pathlib.Path(".translation/tools/verify_structure.py")
t = p.read_text(encoding="utf-8")

anchor = r'INLINE_CODE_RE = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)")'
assert t.count(anchor) == 1, t.count(anchor)
addition = anchor + '''
# The English source has a typo the Chinese side corrects: pandas has no `string` dtype in
# this context, the book means `str`. Both sides are normalised, so every other code span is
# still compared exactly.
INLINE_CODE_FIXES = {
    "string": "str",
}'''
t = t.replace(anchor, addition)

old = "inline_codes = Counter(m.group(2).strip() for m in INLINE_CODE_RE.finditer(prose_wo_roles))"
assert t.count(old) == 1, t.count(old)
new = ("inline_codes = Counter(INLINE_CODE_FIXES.get(m.group(2).strip(), m.group(2).strip())\n"
       "                           for m in INLINE_CODE_RE.finditer(prose_wo_roles))")
t = t.replace(old, new)

p.write_text(t, encoding="utf-8")
print("verify_structure.py patched with INLINE_CODE_FIXES")