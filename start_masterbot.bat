@echo on
cls
cd /d "C:\Users\dstav\OneDrive - Aalborg Universitet\Dokumenter\Skrivebord\CUsersdstavDesktopNTRLI-Superbot"
echo =====================================================
echo  NTRLI MASTER BOT - ALLE 3 BOTS + NFT GENERATOR
echo =====================================================
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python ikke fundet!
    echo Installer fra: https://www.python.org/downloads
    echo Husk: Add Python to PATH
    pause
    exit /b 1
)
echo [OK] Python fundet
echo Kontrollerer dependencies...
pip show telethon >nul 2>&1
if errorlevel 1 (
    echo Installerer Telethon...
    pip install telethon python-dotenv
)
echo [OK] Dependencies klar
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist ".backups" mkdir .backups
echo [OK] Mapper oprettet
if not exist ".env" (
    echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    echo WARNING: .env fil ikke fundet!
    echo Opret .env fil med:
    echo API_ID=8546101037
    echo API_HASH=7defa4b44a90dd22ed93ec4bf36374d4
    echo BOT_TOKEN=8261354099:AAEewnT0GDcOl5-ARokNVuO5i3zMuLyeG7g
    echo ADMIN_ID=8467779489
    echo ADMIN_USERNAME=Sir_NTRLI_II
    echo !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    pause
)
echo STARTER MASTER BOT
python master_bot.py
pause
