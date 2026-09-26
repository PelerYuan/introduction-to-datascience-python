"""Throwaway: exercise sanitize_paths' rules on the real leak forms (and on the JS that
must not be touched) before they are run against the build output."""
import importlib.util
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
spec = importlib.util.spec_from_file_location("sanitize_paths", TOOLS / "sanitize_paths.py")
sp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sp)

RULES = sp.build_rules()
ROOT = str(sp.ROOT)

CASES = [
    # the leak that is in the current build, verbatim from reading.html
    ('<span class="nn">File ' + ROOT + r'\.venv-build\lib\site-packages\ibis\expr\types\relations.py:1222,</span> in <span class="ni">Table.__getattr__</span>',
     '<span class="nn">File /opt/conda/lib/python3.10/site-packages/ibis/expr/types/relations.py:1222,</span> in <span class="ni">Table.__getattr__</span>'),
    # the notebook-execution path a traceback shows
    (r'File ' + ROOT + r'\source\_build\jupyter_execute\reading.ipynb:12, in <module>',
     'File /home/jovyan/work/reading.ipynb:12, in <module>'),
    # the warning paths the notebooks carry (Everything under %TEMP%)
    (r'C:\Users\peler\AppData\Local\Temp\dsh-oziGhf\ipykernel_38652\2654974267.py:1: SettingWithCopyWarning:',
     '/tmp/ipykernel_38652/2654974267.py:1: SettingWithCopyWarning:'),
    (r'C:\Users\peler\AppData\Local\Temp\ipykernel_99\123.py:5: FutureWarning: Calling int',
     '/tmp/ipykernel_99/123.py:5: FutureWarning: Calling int'),
    # a deeper traceback frame, and the pandas form
    (ROOT + r'\.venv-build\lib\site-packages\pandas\io\parsers\readers.py:1026, in read_csv',
     '/opt/conda/lib/python3.10/site-packages/pandas/io/parsers/readers.py:1026, in read_csv'),
    # forward slashes must work too
    (ROOT.replace("\\", "/") + r'/.venv-build/lib/site-packages/x.py',
     '/opt/conda/lib/python3.10/site-packages/x.py'),
    # sys.executable
    (ROOT + r'\.venv-build\Scripts\python.exe',
     '/opt/conda/bin/python'),
    # anything else under the repo root
    (ROOT + r'\.build-cache\mpl\fontlist-v390.json',
     '/home/jovyan/work/.build-cache/mpl/fontlist-v390.json'),
    # a user profile outside temp
    (r'C:\Users\peler\Documents\canlang.csv',
     '/home/jovyan/Documents/canlang.csv'),
    # mac-style and already-neutral paths are left alone
    ('/tmp/ipykernel_12/2654974267.py:1: SettingWithCopyWarning:', None),
    ('/home/jovyan/work/reading.ipynb', None),
    # chart JavaScript: vega/plotly string literals full of `X:\n`
    (r'// Assign z = 0, x = -b, y = a:\n  // a*-b + b*a + c*0 = -ba + ba + 0 = 0\n',
     None),
    (r'h=t.split("\\n"),f={},p=0;p<h.length;p++)',
     None),
    ('fromRotationTranslation:r(33606)', None),
    (r'return n.identity(t),n.fromRotationTranslation(t,s,e)',
     None),
    # prose that follows a path must not be swallowed (and its math backslashes survive)
    (r'C:\Users\peler 是路径，\(x\) 见下。', '/home/jovyan 是路径，\\(x\\) 见下。'),
]

fail = 0
for src, want in CASES:
    got, counts = sp.sanitize(src, RULES)
    if want is None:
        want = src
    ok = got == want
    # idempotence
    again, counts2 = sp.sanitize(got, RULES)
    idem = again == got and not counts2
    if not (ok and idem):
        fail += 1
        print("FAIL", repr(src))
        print("  want", repr(want))
        print("  got ", repr(got), counts)
        print("  idempotent:", idem, counts2)
    else:
        print(f"ok   {counts!s:70}  {got[:70]!r}")

# the leak patterns must not fire on the JS, and must fire on every leak above
LEAKS = [c for c in CASES if c[1] is not None]
for label, rx in sp.leak_patterns():
    for src, want in CASES:
        for m in rx.finditer(src):
            print(f"leak-pattern hit [{label}] in {src[:50]!r}: {m.group(0)[:60]!r}")

print("failures:", fail)
sys.exit(1 if fail else 0)