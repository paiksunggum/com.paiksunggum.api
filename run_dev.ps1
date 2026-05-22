# backend 폴더에서 실행: .\run_dev.ps1
Set-Location $PSScriptRoot
if (Get-Command conda -ErrorAction SilentlyContinue) {
    conda activate venv 2>$null
}
python run.py
