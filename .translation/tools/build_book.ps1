# Build the Chinese edition of the book.
#
# The upstream project builds in a Docker image (ubcdsci/py-intro-to-ds). Docker is not
# available here, so this script uses the equivalent native virtualenv in .venv-build.
#
# Every cache/temp directory is pinned inside the repository: the file sandbox denies
# writes outside the workspace, and tools such as matplotlib and Jupyter default to the
# user profile, which would make the build fail with a confusing permission error.
param(
    [string]$Target = "source",
    [switch]$Offline,
    [switch]$KeepGoing = $true
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $root

$env:PYTHONIOENCODING   = "utf-8"
$env:UV_CACHE_DIR       = Join-Path $root ".uv-cache"
$env:MPLCONFIGDIR       = Join-Path $root ".build-cache\mpl"
$env:JUPYTER_CONFIG_DIR = Join-Path $root ".build-cache\jupyter-config"
$env:JUPYTER_DATA_DIR   = Join-Path $root ".build-cache\jupyter-data"
$env:JUPYTER_RUNTIME_DIR= Join-Path $root ".build-cache\jupyter-runtime"
$env:IPYTHONDIR         = Join-Path $root ".build-cache\ipython"
$env:XDG_CACHE_HOME     = Join-Path $root ".build-cache\xdg"
$env:PYDEVD_DISABLE_FILE_VALIDATION = "1"

# Several chapters call GridSearchCV(n_jobs=-1). joblib then spins up a loky process
# pool, whose workers talk to the parent over OS IPC that this sandbox denies, so the
# cell dies with PermissionError inside joblib's backend initialisation and its figure
# never registers (the {numref} then renders as raw text). loky caps its detected CPU
# count from this variable, which makes n_jobs=-1 resolve to a single in-process worker:
# identical numbers, no subprocesses.
$env:LOKY_MAX_CPU_COUNT = "1"

foreach ($d in @($env:MPLCONFIGDIR, $env:JUPYTER_CONFIG_DIR, $env:JUPYTER_DATA_DIR,
                 $env:JUPYTER_RUNTIME_DIR, $env:IPYTHONDIR, $env:XDG_CACHE_HOME)) {
    New-Item -ItemType Directory -Force -Path $d | Out-Null
}

$py = Join-Path $root ".venv-build\Scripts\python.exe"
if (-not (Test-Path $py)) { throw "No build venv at $py - run tools/install_build_env.ps1 first" }

# build_runner.py wraps the jupyter-book CLI and removes Jupyter's Windows ACL hardening,
# which this sandbox denies (WinError 5) and which would otherwise kill every kernel start.
$runner = Join-Path $root ".translation\tools\build_runner.py"

$jbArgs = @($runner, "build", $Target)
if ($KeepGoing) { $jbArgs += "--keep-going" }
if ($Offline)   { $jbArgs += "-n" }

Write-Host "=== jupyter-book build $Target ===" -ForegroundColor Cyan
& $py @jbArgs
$code = $LASTEXITCODE
Write-Host "=== build exit code: $code ===" -ForegroundColor $(if ($code -eq 0) { "Green" } else { "Yellow" })

$canonical = Join-Path $root "add_canonical_links.py"
if ($code -eq 0 -and (Test-Path $canonical)) {
    Write-Host "=== add_canonical_links.py ===" -ForegroundColor Cyan
    & $py $canonical
}

exit $code