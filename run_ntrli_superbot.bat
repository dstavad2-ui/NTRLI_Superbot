@echo off
:: ==============================================
:: NTRLI Superbot runner
:: Opens PowerShell and runs bot with auto-restart
:: ==============================================

echo Starting NTRLI Superbot...
powershell -NoExit -Command "& {Start-Process powershell -ArgumentList '-NoExit','-ExecutionPolicy','Bypass','-File','run_ntrli_superbot.ps1'}"
pause
