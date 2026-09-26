#!/usr/bin/env python3
"""Download wheels without pip's network stack, then install them from disk.

In this sandbox pip hangs indefinitely on the index (it produces no output at all, even
with -v, while plain `urllib` reaches pypi.org in under a second). Rather than fight it,
this resolves a package's wheel URL from the PyPI JSON API and downloads it directly with
urllib, which works. The wheels are then installed with `--no-index`, so pip never has to
touch the network.

Usage:
    python fetch_wheel.py pyarrow altair==5.5.0
    python fetch_wheel.py --install-dir .wheels --dest .wheels pyarrow
"""
import argparse
import json
import platform
import re
import sys
import urllib.request
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

UA = {"User-Agent": "fetch-wheel/1.0"}


def tags() -> tuple[str, str, str]:
    v = sys.version_info
    py = f"cp{v.major}{v.minor}"
    machine = platform.machine().lower()
    arch = {"amd64": "win_amd64", "x86_64": "manylinux", "arm64": "win_arm64"}.get(machine, machine)
    return py, arch, platform.system().lower()


def score(filename: str, py: str, arch: str) -> int | None:
    """Rank a candidate wheel; None means 'not usable here'. Lower score wins.

    The platform tag is compared **exactly**. Matching on a substring accepts
    `...-cp310-cp310-win32.whl` for a 64-bit interpreter, because the string "win" occurs
    in "win32" — which is how a 32-bit numpy was downloaded once. pip refuses to install
    such a wheel, so the failure is loud, but the download was still wasted.
    """
    if not filename.endswith(".whl"):
        return None
    parts = filename[:-4].split("-")
    if len(parts) < 5:
        return None
    pytag, abitag, plat = parts[-3].lower(), parts[-2].lower(), parts[-1].lower()
    if plat == "any":
        return 100 if (py in pytag or "py3" in pytag) else None
    if plat != arch:
        return None
    if py in pytag:
        return 0
    # A stable-ABI wheel (`cp39-abi3-win_amd64`) also imports on this interpreter.
    if "abi3" in abitag and py.startswith("cp"):
        return 1
    return None


def resolve(spec: str) -> tuple[str, str, str]:
    """(package, version, url) for one requirement spec like `altair==5.5.0`."""
    m = re.match(r"^([A-Za-z0-9_.\-]+)\s*(?:==\s*([^\s]+))?$", spec.strip())
    if not m:
        raise SystemExit(f"cannot parse requirement: {spec!r}")
    name, want = m.group(1), m.group(2)
    url = f"https://pypi.org/pypi/{name}/json" if not want else f"https://pypi.org/pypi/{name}/{want}/json"
    data = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())
    version = data["info"]["version"]
    py, arch, _ = tags()
    best = None
    for entry in data["urls"]:
        s = score(entry["filename"], py, arch)
        if s is not None and (best is None or s < best[0]):
            best = (s, entry["filename"], entry["url"])
    if best is None:
        raise SystemExit(f"{name} {version}: no wheel for {py}/{arch}")
    return name, version, best[2]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("requirements", nargs="+")
    ap.add_argument("--dest", type=Path, default=Path(".wheels"))
    ap.add_argument("--install", action="store_true", help="pip install the downloads afterwards")
    args = ap.parse_args()

    args.dest.mkdir(parents=True, exist_ok=True)
    paths = []
    for spec in args.requirements:
        name, version, url = resolve(spec)
        target = args.dest / url.rsplit("/", 1)[-1]
        if target.exists() and target.stat().st_size > 0:
            print(f"cached  {name} {version}  {target.name}")
        else:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r:
                blob = r.read()
            target.write_bytes(blob)
            print(f"fetched {name} {version}  {target.name}  ({len(blob) / 1e6:.1f} MB)")
        paths.append(target)

    if args.install:
        import subprocess

        cmd = [sys.executable, "-m", "pip", "install", "--no-index", "--no-deps"] + [str(p) for p in paths]
        print("+", " ".join(cmd))
        return subprocess.call(cmd)
    print("\ninstall with: pip install --no-index --no-deps " + " ".join(str(p) for p in paths))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())