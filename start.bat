@echo off
setlocal enabledelayedexpansion
title OmniScope OSINT // Master Launcher

echo ===============================================================================
echo                OMNISCOPE OSINT - GEOSPATIAL INTELLIGENCE GRID
echo ===============================================================================
echo.

:: 1. Check for Python installation
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python wurde auf diesem Computer nicht gefunden!
    echo Bitte installiere Python 3.10+ von https://www.python.org/downloads/
    echo und stelle sicher, dass die Option "Add python.exe to PATH" aktiviert ist.
    echo.
    pause
    exit /b 1
)

:: 2. Check virtual environment (.venv)
if not exist ".venv\Scripts\python.exe" (
    echo [SETUP] Erstelle Python Virtual Environment (.venv)...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERROR] Konnte Virtual Environment nicht erstellen.
        pause
        exit /b 1
    )
    echo [SETUP] Installiere erforderliche Python-Bibliotheken...
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    if exist "backend\requirements.txt" (
        pip install -r backend\requirements.txt
    ) else if exist "requirements.txt" (
        pip install -r requirements.txt
    )
) else (
    call .venv\Scripts\activate.bat
)

:: 3. Check if first-run setup is required
if not exist ".env" (
    echo [INFO] Erster Start erkannt. Starte Setup-Assistenten...
    python setup_wizard.py
) else if not exist "backend\data\omniscope_spatial.db" (
    echo [INFO] Spatial-Datenbank nicht gefunden. Starte Setup-Assistenten...
    python setup_wizard.py
)

:: 4. Launch OmniScope OSINT Server
echo.
echo ===============================================================================
echo [LAUNCH] Starte OmniScope OSINT Server auf http://127.0.0.1:8888 ...
echo ===============================================================================
echo.

start "" "http://127.0.0.1:8888"
python run_server.py

pause
