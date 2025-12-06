@echo off
REM ===============================
REM NTRLI Superbot Debug Runner
REM ===============================

REM Set Python path if not in system PATH
SET PYTHON=python

REM Navigate to your bot folder
cd /d "C:\Users\dstav\OneDrive - Aalborg Universitet\Dokumenter\Skrivebord\CUsersdstavDesktopNTRLI-Superbot"

REM Use PowerShell to run Python with error handling
powershell -Command ^
    "$ErrorActionPreference='Stop'; ^
    try { ^
        Write-Host 'Starting NTRLI Debug Bot...' -ForegroundColor Cyan; ^
        & '%PYTHON%' debug_bot.py; ^
    } catch { ^
        Write-Host '⚠️ ERROR: Bot crashed!' -ForegroundColor Red; ^
        Write-Host $_.Exception.Message; ^
        Pause; ^
    }"
