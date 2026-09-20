$ErrorActionPreference = 'Continue'
$py = ".\.venv-build\Scripts\python.exe"

function Install-Stage {
    param(
        [string]$Name,
        [string[]]$Packages
    )
    Write-Host "=== $Name ($($Packages.Count) packages) ==="
    & $py -m pip install --disable-pip-version-check --no-input --only-binary :all: @Packages
    Write-Host "=== $Name exit: $LASTEXITCODE ==="
}

# Stage 1: build toolchain (jupyter-book + sphinx stack). Small, conflict-free.
Install-Stage -Name "stage1-toolchain" -Packages @(
    "numpy", "jinja2", "click", "lxml", "referencing", "docutils==0.17.1",
    "pyyaml", "jsonschema", "jupytext", "jupyter-book==0.15.1"
)

# Stage 2: data stack needed to execute the notebooks
Install-Stage -Name "stage2-data" -Packages @(
    "pandas>=2.1.3", "scikit-learn>=1.3.2", "openpyxl", "ghp-import"
)

# Stage 3: visualization stack
Install-Stage -Name "stage3-viz" -Packages @(
    "altair>=5.1.2", "vl-convert-python>=0.14", "plotly"
)

# Stage 4: vegafusion (used by chapter_preamble.py for the HTML build)
Install-Stage -Name "stage4-vegafusion" -Packages @("vegafusion")

Write-Host "=== VERIFY ==="
& $py -c "import jupyter_book, pandas, altair, sklearn, numpy; print('jupyter-book', jupyter_book.__version__); print('pandas', pandas.__version__); print('altair', altair.__version__); print('sklearn', sklearn.__version__); print('numpy', numpy.__version__)"
Write-Host "=== verify exit: $LASTEXITCODE ==="
& $py -c "import vegafusion; print('vegafusion OK')"
Write-Host "=== INSTALL PHASE COMPLETE ==="