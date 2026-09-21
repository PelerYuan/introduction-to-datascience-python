# Publish the Chinese edition to GitHub Pages.
#
#   pwsh -NoProfile -File .translation/tools/publish_book.ps1              # rebuild + publish
#   pwsh -NoProfile -File .translation/tools/publish_book.ps1 -SkipBuild  # publish existing build
#
# Everything the site needs beyond a plain `jupyter-book build` is handled here:
# the canonical base URL, the .nojekyll marker, and pushing to the branch Pages serves.

[CmdletBinding()]
param(
    [switch]$SkipBuild,
    [string]$BaseUrl = "https://page.peler.top/introduction-to-datascience-python",
    # Overridable so the publish path itself can be exercised against a scratch branch
    # without touching the branch Pages actually serves.
    [string]$Branch = "gh-pages-zh",
    # Overwrite the remote branch even when it holds commits this deploy clone does not.
    # Never point this at the inherited upstream `gh-pages` branch: that one is the
    # original authors' English deployment and is not ours to rewrite.
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$docs = Join-Path $root "source\_build\html"
$dep  = Join-Path $root ".pages-deploy"
$repo = "PelerYuan/introduction-to-datascience-python"
$branch = $Branch

if (-not $SkipBuild) {
    $env:DOCS_BASE_URL = $BaseUrl
    & pwsh -NoProfile -File (Join-Path $PSScriptRoot "build_book.ps1")
    if ($LASTEXITCODE -ne 0) { Write-Host "build failed, not publishing" -ForegroundColor Red; exit 1 }
}

if (-not (Test-Path (Join-Path $docs "index.html"))) {
    Write-Host "no build output at $docs" -ForegroundColor Red; exit 1
}

# The build must have been produced with this base URL, otherwise the published pages
# would advertise someone else's site as canonical.
$canonical = Select-String -Path (Join-Path $docs "index.html") -Pattern 'rel="canonical" href="([^"]+)"' |
    Select-Object -First 1
if (-not $canonical -or $canonical.Matches[0].Groups[1].Value -notlike "$BaseUrl/*") {
    Write-Host "canonical in the build is not $BaseUrl/*; rebuild with DOCS_BASE_URL set" -ForegroundColor Yellow
    Write-Host "  found: $(if ($canonical) { $canonical.Matches[0].Groups[1].Value } else { 'none' })"
}

if (-not (Test-Path (Join-Path $dep ".git"))) {
    New-Item -ItemType Directory -Path $dep -Force | Out-Null
    git -C $dep init -q
    git -C $dep checkout -q -b $branch
    git -C $dep config user.email "dsh@localhost"
    git -C $dep config user.name "DSH"
}
elseif ((git -C $dep rev-parse --abbrev-ref HEAD) -ne $branch) {
    # Honour -Branch. This clone is a throwaway that is always refilled from the build
    # output, so resetting the local branch onto the current tree is the right move.
    Write-Host "switching deploy clone to branch $branch" -ForegroundColor Cyan
    git -C $dep checkout -q -B $branch
}

Copy-Item (Join-Path $docs "*") $dep -Recurse -Force
Copy-Item (Join-Path $docs ".nojekyll") $dep -Force

git -C $dep add -A
if (-not (git -C $dep status --porcelain)) {
    Write-Host "nothing to publish: the branch already matches the build" -ForegroundColor Green
    exit 0
}

$count = (git -C $dep diff --cached --name-only | Measure-Object -Line).Lines
git -C $dep -c core.autocrlf=false commit -q -m "Publish the Chinese edition"
$token = gh auth token
$pushArgs = @()
if ($Force) { $pushArgs += "--force" }
git -C $dep -c http.sslBackend=openssl push @pushArgs "https://x-access-token:$token@github.com/$repo.git" "${branch}:${branch}"
if ($LASTEXITCODE -ne 0) {
    Write-Host "push rejected. The remote branch '$branch' has commits this deploy clone" -ForegroundColor Red
    Write-Host "does not contain. Re-run with -Force to overwrite it, but check first that you" -ForegroundColor Red
    Write-Host "are not aiming at the inherited upstream gh-pages branch." -ForegroundColor Red
    exit 1
}

Write-Host "published $count changed file(s) -> $BaseUrl/" -ForegroundColor Green
Write-Host "Pages rebuilds in about a minute; verify with: python .translation/tools/deploy_check.py"