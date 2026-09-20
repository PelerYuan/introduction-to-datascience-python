#!/usr/bin/env python3
"""Run `jupyter-book build` without Jupyter's Windows ACL hardening.

`jupyter_core.paths.secure_write()` calls `SetFileSecurityW(..., DACL_SECURITY_INFORMATION)`
to restrict the kernel connection file to the current user. This environment denies that
call with WinError 5 (the process token has no WRITE_DAC), so *every* notebook execution
died at kernel startup even though the file itself was creatable.

Jupyter reaches that path through `jupyter_core.paths.win32_restrict_file_to_user` on all
platforms (`secure_write` is a no-op on POSIX). Replacing `secure_write` with a plain
open-succeeding context manager removes the only sandbox-incompatible call while leaving
everything else — kernels, execution, caching, HTML output — exactly as upstream.

Usage (normally invoked by tools/build_book.ps1):
    python build_runner.py build source --keep-going
"""
from __future__ import annotations

import contextlib
import sys

import jupyter_core.paths as jp


@contextlib.contextmanager
def _secure_write(fname, binary=False):
    """Drop-in for jupyter_core.paths.secure_write that does no ACL hardening."""
    if binary:
        handle = open(fname, "wb")
    else:
        handle = open(fname, "w", encoding="utf-8", newline="\n")
    with handle:
        yield handle


# jupyter_client does `from jupyter_core.paths import secure_write`, so the name must be
# replaced in both modules before jupyter_client is imported.
jp.win32_restrict_file_to_user = lambda *a, **k: None
jp.secure_write = _secure_write
jp._win32_restrict_file_to_user_ctypes = lambda *a, **k: None

import jupyter_client.connect  # noqa: E402

jupyter_client.connect.secure_write = _secure_write

try:  # newer jupyter_client also imports it here
    import jupyter_client.provisioning.local_provisioner as _lp  # noqa: E402

    if hasattr(_lp, "secure_write"):
        _lp.secure_write = _secure_write
except Exception:  # pragma: no cover - module layout varies by version
    pass

from jupyter_book.cli.main import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))