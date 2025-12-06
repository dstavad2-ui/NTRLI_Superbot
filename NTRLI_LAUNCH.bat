@echo off
REM ═══════════════════════════════════════════════════════════════
REM   NTRLI SUPERBOT - QUICK LAUNCHER
REM   Automatically navigates to project and runs finalization
REM ═══════════════════════════════════════════════════════════════

setlocal enabledelayedexpansion

REM Navigate to project directory
cd /d "C:\Users\dstav\OneDrive - Aalborg Universitet\Dokumenter\Skrivebord\CUsersdstavDesktopNTRLI-Superbot"

cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo    🌿 N T R L I   S U P E R B O T   L A U N C H E R   🌿
echo ═══════════════════════════════════════════════════════════════
echo.
echo    Current Directory: %CD%
echo.
echo ───────────────────────────────────────────────────────────────
echo.

REM Check if PowerShell script exists
if not exist "ntrli_finalizer.ps1" (
    echo  ✗ ERROR: ntrli_finalizer.ps1 not found in this directory!
    echo.
    echo    Please ensure the script is saved in:
    echo    %CD%
    echo.
    pause
    exit /b 1
)

echo  ✓ Found ntrli_finalizer.ps1
echo.
echo ───────────────────────────────────────────────────────────────
echo.
echo    Choose an option:
echo.
echo    1. Full Update + Launch (Recommended)
echo    2. Update Only (No Launch)
echo    3. Launch Only (Skip Updates)
echo    4. Health Check Only
echo    5. Exit
echo.
echo ───────────────────────────────────────────────────────────────
echo.

set /p choice="  Enter your choice (1-5): "

echo.
echo ═══════════════════════════════════════════════════════════════
echo.

if "%choice%"=="1" (
    echo  ⟳ Running Full Update + Launch...
    echo.
    powershell -ExecutionPolicy Bypass -File "ntrli_finalizer.ps1"
) else if "%choice%"=="2" (
    echo  ⟳ Running Update Only...
    echo.
    powershell -ExecutionPolicy Bypass -File "ntrli_finalizer.ps1" -UpdateOnly
) else if "%choice%"=="3" (
    echo  ⟳ Launching Bot System...
    echo.
    powershell -ExecutionPolicy Bypass -File "ntrli_finalizer.ps1" -LaunchOnly
) else if "%choice%"=="4" (
    echo  ⟳ Running Health Check...
    echo.
    powershell -ExecutionPolicy Bypass -File "ntrli_finalizer.ps1" -CheckHealth
) else if "%choice%"=="5" (
    echo  ✓ Exiting...
    exit /b 0
) else (
    echo  ✗ Invalid choice!
    echo.
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo.
pause