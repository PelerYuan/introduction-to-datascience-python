# Final gate -> rebuild -> republish chain for round 3.
# Aborts before touching the published site if any gate is red, so the live book can never
# regress to a state that failed verification.
$ErrorActionPreference = "Stop"
$env:PYTHONIOENCODING = "utf-8"
$env:DOCS_BASE_URL = "https://page.peler.top/introduction-to-datascience-python"
$py = ".\.venv-build\Scripts\python.exe"
Set-Location "D:\Translation\Data Science A First Introduction with Python"

function Step($msg) { Write-Host "== $msg" }

Step "1/7 source gates (18 chapters x 3)"
$ok = 0; $bad = @()
foreach ($f in (Get-ChildItem source\*.md | Where-Object { $_.Name -notmatch '^(_|README)' })) {
    $n = $f.BaseName
    $a = & $py .translation\tools\verify_structure.py --en ".translation\source_en\$n.md" --zh "source\$n.md" 2>&1 | Select-Object -Last 1
    $b = & $py .translation\tools\lint_zh.py --zh "source\$n.md" 2>&1 | Select-Object -Last 1
    $c = & $py .translation\tools\check_emphasis.py --path "source\$n.md" 2>&1 | Select-Object -Last 1
    if ($a -match '^OK' -and $b -match '^OK' -and $c -match '^OK') { $ok++ } else { $bad += "$n | $a | $b | $c" }
}
Write-Host "structure+lint+emphasis OK: $ok/18"
if ($bad) { $bad; throw "source gates failed - not rebuilding" }

Step "2/7 rebuild (this re-executes all 18 notebooks)"
pwsh -NoProfile -File .translation\tools\build_book.ps1 *> .translation\logs\build_r3.log
if ($LASTEXITCODE -ne 0) { throw "build failed, see build_r3.log" }
Write-Host "build exit 0"

Step "3/7 rendered-page gates (charts, paths, tracebacks)"
$hq = & $py .translation\tools\html_qa.py --json .translation\reports\html_qa.json 2>&1
$hq | Select-Object -First 5
if (-not ($hq | Select-String 'rendered book is clean')) { throw "rendered book is not clean" }

Step "4/7 commit"
git add -A
git -c user.name="peler" -c user.email="peler@users.noreply.github.com" commit -q -m "fix: keep this machine's filesystem out of the published book

- The cells that fail on purpose are executed here, so their rendered tracebacks
  named this machine: File D:...\.venv-build\lib\site-packages\ibis\... and the
  ipykernel files under AppData\Local\Temp. A new post-build tool,
  tools/sanitize_paths.py, rewrites those strings to the paths the upstream Docker
  image shows - the build venv's site-packages to /opt/conda/lib/python3.10/
  site-packages, source\_build\jupyter_execute\<name>.ipynb to
  /home/jovyan/work/<name>.ipynb, the repository root to /home/jovyan/work and the
  temp files to /tmp - and build_book.ps1 runs it right after the build, before the
  canonical links, so the sanitised HTML is what gets published. It is deterministic
  and idempotent, its --check mode exits non-zero on any leftover, and it only ever
  rewrites path strings, never chart JavaScript. No cell was touched: the code blocks
  are still byte-identical to the English source.
- html_qa.py now scans the whole rendered page instead of only its paragraphs, so
  RENDERED_PATH sees error-output and traceback blocks. That is precisely what the
  old check could not see: the ibis traceback lives in an output div, and the gate
  reported the book clean while those paths were live on the site.
- inference: the sampling-distribution sentence loses the 的样本的样本 pile-up and
  now reads 再画出样本量为 40 时样本均值的抽样分布。"
git -c http.sslBackend=openssl push "https://x-access-token:$(gh auth token)@github.com/PelerYuan/introduction-to-datascience-python.git" main 2>&1 | Select-Object -Last 1

Step "5/7 publish"
pwsh -NoProfile -File .translation\tools\publish_book.ps1 -SkipBuild *> .translation\logs\publish_r3.log
Write-Host "publish exit $LASTEXITCODE"

Step "6/7 wait for Pages, then check every reference"
Start-Sleep -Seconds 75
& $py .translation\tools\deploy_check.py 2>&1 | Select-Object -Last 3

Step "7/7 live render check"
& $py .translation\tools\check_live_render.py 2>&1 | Select-Object -Last 7
git status --short | Measure-Object | ForEach-Object { "uncommitted: $($_.Count)" }
git log --oneline -1
Write-Host "CHAIN DONE"