import os
import sqlite3
import shutil

# ==============================
# Paths
# ==============================
BOT_FOLDER = r"C:\Users\dstav\OneDrive - Aalborg Universitet\Dokumenter\Skrivebord\CUsersdstavDesktopNTRLI-Superbot"
SESSION_FILE = os.path.join(BOT_FOLDER, "ntrli_superbot_session.session")
BACKUP_FILE = os.path.join(BOT_FOLDER, "ntrli_superbot_session_backup.session")

# ==============================
# Step 1: Check session file
# ==============================
if os.path.exists(SESSION_FILE):
    print("[INFO] Session file exists. Checking integrity...")

    try:
        conn = sqlite3.connect(SESSION_FILE)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = c.fetchall()
        print(f"[INFO] SQLite tables found: {tables}")
        conn.close()

        size_mb = os.path.getsize(SESSION_FILE) / (1024 * 1024)
        print(f"[INFO] Session file size: {size_mb:.2f} MB")

        if size_mb > 50:
            print("[WARNING] Session file too large. Backing up and recreating...")
            shutil.copy2(SESSION_FILE, BACKUP_FILE)
            os.remove(SESSION_FILE)

    except sqlite3.DatabaseError:
        print("[ERROR] Session file corrupted. Backing up and recreating...")
        shutil.copy2(SESSION_FILE, BACKUP_FILE)
        os.remove(SESSION_FILE)

else:
    print("[INFO] No session file found. A new one will be created automatically.")

# ==============================
# Step 2: Clean temp SQLite cache
# ==============================
TEMP_DIR = os.getenv('TEMP', '/tmp')
for f in os.listdir(TEMP_DIR):
    if f.startswith("sqlite"):
        try:
            os.remove(os.path.join(TEMP_DIR, f))
        except Exception:
            pass

print("[INFO] Cleanup complete. Starting NTRLI Superbot...")

# ==============================
# Step 3: Start the bot
# ==============================
os.system(f"python \"{os.path.join(BOT_FOLDER, 'bot.py')}\"")
