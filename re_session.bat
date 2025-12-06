@echo off
REM =====================================================
REM NTRLI Superbot Smart Session Restore
REM Folder: C:\Users\dstav\OneDrive - Aalborg Universitet\Dokumenter\Skrivebord\CUsersdstavDesktopNTRLI-Superbot
REM =====================================================

SET BOT_FOLDER="C:\Users\dstav\OneDrive - Aalborg Universitet\Dokumenter\Skrivebord\CUsersdstavDesktopNTRLI-Superbot"
cd /d %BOT_FOLDER%

REM Run Python script to check and restore session
python restore_session.py

pause
