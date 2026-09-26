"""Check every local asset referenced by the deployed book, over HTTP.

Guessing paths proves nothing; this pulls the actual src/href references out of the built
pages and requests each distinct one. It is the check that catches a missing .nojekyll,
because that failure shows up as every asset under _static/_images/_sources returning 404.
"""
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

BASE = "http://page.peler.top/introduction-to-datascience-python"
DOCS = Path("source/_build/html")

REF = re.compile(r'(?:src|href)="([^"#?]+)"')
# Any URI scheme at all, not just http(s): the theme embeds a base64 GIF spacer as a
# `data:` URI, and requesting that as a path reports a 404 that does not exist.
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.\-]*:")
# Chart output embeds its whole runtime, and that JavaScript contains `href="..."` strings
# that are not page references — scraping them produced an `InvalidURL` finding that pointed
# at minified Vega code. Script and style bodies are removed before extraction.
SCRIPT_STYLE = re.compile(r"<(script|style)\b.*?</\1\s*>", re.DOTALL | re.IGNORECASE)
# References that 404 on purpose, recorded rather than silently tolerated. These are
# Wikipedia's own site-relative links inside the HTML example the reading chapter displays
# to show what scraped markup looks like (`<a href="/wiki/London,_Ontario">`). They resolve
# against whatever host serves the book, so they 404 on the English site too — the same
# string sits at `.translation/source_en/reading.md:1316`.
KNOWN_BROKEN_REFS = {
    "/wiki/Greater_Montreal",
    "/wiki/Greater_Toronto_Area",
    "/wiki/London,_Ontario",
}
pages = sorted(DOCS.glob("*.html"))

refs: set[str] = set()
for page in pages:
    blob = SCRIPT_STYLE.sub(" ", page.read_text(encoding="utf-8"))
    for m in REF.finditer(blob):
        ref = m.group(1)
        if SCHEME.match(ref) or ref.startswith("//") or ref in KNOWN_BROKEN_REFS:
            continue
        refs.add(ref)

print(f"{len(pages)} pages, {len(refs)} distinct local references")

bad = []
for ref in sorted(refs):
    url = f"{BASE}/{ref}"
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            if r.status != 200:
                bad.append((ref, r.status))
    except urllib.error.HTTPError as e:
        bad.append((ref, e.code))
    except Exception as e:  # noqa: BLE001
        bad.append((ref, type(e).__name__))

if bad:
    print(f"\n{len(bad)} BROKEN reference(s):")
    for ref, code in bad:
        print(f"  {code}  {ref}")
else:
    print("\nall local references resolve (200)")

by_dir: dict[str, int] = {}
for ref in refs:
    by_dir[ref.split("/")[0] if "/" in ref else "(page)"] = by_dir.get(
        ref.split("/")[0] if "/" in ref else "(page)", 0) + 1
print("\nby directory:", dict(sorted(by_dir.items())))
sys.exit(1 if bad else 0)