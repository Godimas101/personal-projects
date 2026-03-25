@echo off
setlocal
cd /d "%~dp0"

echo ==========================================
echo  Claude Usage Monitor — Build
echo ==========================================

:: ── Step 1: PyInstaller ───────────────────
echo.
echo [1/2] Building exe with PyInstaller...
python -m PyInstaller ClaudeUsageMonitor.spec --noconfirm
if errorlevel 1 (
    echo ERROR: PyInstaller failed.
    pause
    exit /b 1
)
echo       Done. dist\ClaudeUsageMonitor.exe ready.

:: ── Step 2: Inno Setup ────────────────────
echo.
echo [2/2] Building installer with Inno Setup...

set ISCC=
for %%p in (
    "C:\Program Files (x86)\Inno Setup 6\iscc.exe"
    "C:\Program Files\Inno Setup 6\iscc.exe"
) do if exist %%p set ISCC=%%p

if "%ISCC%"=="" (
    echo ERROR: Inno Setup not found.
    echo        Download from: https://jrsoftware.org/isdownload.php
    pause
    exit /b 1
)

%ISCC% installer.iss
if errorlevel 1 (
    echo ERROR: Inno Setup failed.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo  Build complete!
echo  Installer: installer\ClaudeUsageMonitorSetup-v1.0.0.exe
echo ==========================================
pause
