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

Step "3/7 rendered-page gates"
$hq = & $py .translation\tools\html_qa.py --json .translation\reports\html_qa.json 2>&1
$hq | Select-Object -First 5
if (-not ($hq | Select-String 'rendered book is clean')) { throw "rendered book is not clean" }

Step "4/7 commit"
git add -A
git -c user.name="peler" -c user.email="peler@users.noreply.github.com" commit -q -m "fix: finish the read-through review (ordinals, hyperparameters, label formatting)

- regression1: the RMSPE explanation now reads 第 i 个观测 instead of keeping the
  English ordinal superscript next to 第. verify_structure normalises that one token
  on both sides, so every other formula is still compared exactly.
- classification2 and regression1: the last five places that called $K a 参数 are
  超参数 now; get_params, 参数网格 and np.random.seed keep 参数 because those really
  are function arguments.
- wrangling: categorical values are 类别取值, matching 类别型变量 elsewhere.
- Uniform UI-label formatting: the English gloss always sits outside the bold, so
  lint_zh exempts the gloss rather than forcing it inside; Run no longer renders as
  two adjacent parentheses, and quote placement is consistent.
- The two 3-D captions put their translator note at the end of the sentence instead
  of next to another parenthetical."
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