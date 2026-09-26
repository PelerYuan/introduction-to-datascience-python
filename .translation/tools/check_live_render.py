"""Check the *deployed* site: do the charts actually render at the public URL?"""
import re
import urllib.request

BASE = "https://page.peler.top/introduction-to-datascience-python/"
VEGA = re.compile(r"vegaEmbed\(")
PLOTLY = re.compile(r"Plotly\.newPlot|plotly-graph-div|cdn\.plot\.ly/plotly-")
PAGES = ["index.html", "viz.html", "classification1.html", "regression1.html", "wrangling.html"]

total_vega = total_plotly = 0
for page in PAGES:
    try:
        blob = urllib.request.urlopen(BASE + page, timeout=60).read().decode("utf-8", "replace")
    except Exception as exc:
        print("%-24s ERR %s %s" % (page, type(exc).__name__, str(exc)[:60]))
        continue
    nv, np_ = len(VEGA.findall(blob)), len(PLOTLY.findall(blob))
    total_vega += nv
    total_plotly += np_
    print("%-24s vegaEmbed=%3d  plotly=%2d  %6.0f KB" % (page, nv, np_, len(blob) / 1024))
print("sampled totals: altair=%d plotly=%d" % (total_vega, total_plotly))

# A canonical link proves the deployed HTML came from the DOCS_BASE_URL build rather than
# the earlier one that had canonical tags stripped.
idx = urllib.request.urlopen(BASE + "index.html", timeout=60).read().decode("utf-8", "replace")
m = re.search(r'<link rel="canonical" href="([^"]+)"', idx)
print("canonical:", m.group(1) if m else "MISSING")