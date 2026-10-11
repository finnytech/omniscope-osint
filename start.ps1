# OmniScope OSINT - PowerShell Launcher
$Host.UI.RawUI.WindowTitle = "OmniScope OSINT // Master Launcher"

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "               OMNISCOPE OSINT - GEOSPATIAL INTELLIGENCE GRID" -ForegroundColor White
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Check Python
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "[FEHLER] Python wurde auf diesem Computer nicht gefunden!" -ForegroundColor Red
    Write-Host "Bitte installiere Python 3.10+ von https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "und aktiviere 'Add python.exe to PATH'."
    Read-Host "Druecke Enter zum Beenden..."
    exit 1
}

# 2. Check Virtual Environment (.venv)
$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "[SETUP] Erstelle Python Virtual Environment (.venv)..." -ForegroundColor Yellow
    python -m venv (Join-Path $PSScriptRoot ".venv")
    
    Write-Host "[SETUP] Installiere erforderliche Python-Bibliotheken..." -ForegroundColor Yellow
    & $venvPython -m pip install --upgrade pip
    
    $reqFile = Join-Path $PSScriptRoot "backend\requirements.txt"
    if (Test-Path $reqFile) {
        & $venvPython -m pip install -r $reqFile
    }
}

# 3. Check first-run setup
$envFile = Join-Path $PSScriptRoot ".env"
$dbFile = Join-Path $PSScriptRoot "backend\data\omniscope_spatial.db"

if ((-not (Test-Path $envFile)) -or (-not (Test-Path $dbFile))) {
    Write-Host "[INFO] Erster Start erkannt. Starte Setup-Assistenten..." -ForegroundColor Magenta
    & $venvPython (Join-Path $PSScriptRoot "setup_wizard.py")
}

# 4. Launch OmniScope OSINT
Write-Host ""
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "[LAUNCH] Starte OmniScope OSINT auf http://127.0.0.1:8888 ..." -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host ""

Start-Process "http://127.0.0.1:8888"
& $venvPython (Join-Path $PSScriptRoot "run_server.py")
