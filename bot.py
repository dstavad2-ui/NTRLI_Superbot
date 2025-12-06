# bot.py — NTRLI Superbot with live AI/web stubs and console input

import os
import sys
import asyncio
import logging
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv

# Safely import Telethon — mock if unavailable
try:
    from telethon import TelegramClient, events, Button
except ModuleNotFoundError:
    TelegramClient = events = Button = None
    sys.stderr.write("Warning: 'telethon' module not found. Bot functionality will be limited.\n")

# Load .env
load_dotenv()

# Paths (use cwd, not __file__)
ROOT = Path(os.getcwd()).resolve()
LOGS = ROOT / "logs"
IMAGES = ROOT / "images"
SESSIONS = ROOT / "sessions"
DATA = ROOT / "data"
for d in (LOGS, IMAGES, SESSIONS, DATA):
    d.mkdir(exist_ok=True)

# UTF-8
os.environ.setdefault("PYTHONUTF8", "1")
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOGS / "bot.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("ntrli")

# Environment variables
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY", "")
SESSION_NAME = os.getenv("SESSION_NAME", "ntrli_superbot")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Database setup
DB = ROOT / "ntrli_superbot.db"
conn = sqlite3.connect(DB, check_same_thread=False)
cur = conn.cursor()

# In-memory state
PENDING: Dict[int, Dict[str, Any]] = {}
PENDING_TIMEOUT = 300

# Helpers
def is_admin(uid: int) -> bool:
    return uid == ADMIN_ID

def normalize_buttons(btns: Any) -> List[List[Any]]:
    if not btns:
        return []
    if isinstance(btns, str):
        return [[btns]]
    out = []
    for row in btns:
        if isinstance(row, str):
            out.append([row])
        else:
            out.append(list(row))
    return out

def clean_pending():
    now = time.time()
    stale = [uid for uid, v in PENDING.items() if now - v.get("ts", 0) > PENDING_TIMEOUT]
    for uid in stale:
        del PENDING[uid]

# --- AI helper (stub) ---
async def call_ai_summary(prompt: str, timeout: int = 20) -> str:
    logger.info("AI summary requested: %s", prompt)
    return f"(AI stub response for: {prompt})"

# --- Web search / validation stub ---
async def web_search(query: str) -> Dict[str, Any]:
    logger.info("Web search requested: %s", query)
    return {"query": query, "results": [f"Result 1 for {query}", f"Result 2 for {query}"]}

# --- Telegram bot logic ---
async def handle_buttons(ev):
    clean_pending()
    data = getattr(ev, 'data', '')
    if isinstance(data, (bytes, bytearray)):
        data = data.decode('utf-8')
    uid = getattr(ev, 'sender_id', 0)
    logger.info(f"Button press from {uid}: {data}")

    if data == 'start':
        btns = [["🛒 Fysiske varer"], ["🎨 NFTs"], ["💊 Apotekvarer AI info"]]
        if is_admin(uid):
            btns.append(["⚙️ Admin Panel"])
        try:
            if hasattr(ev, 'edit'):
                await ev.edit("Velkommen! Vælg en mulighed ⬇️", buttons=normalize_buttons(btns))
            else:
                await ev.respond("Velkommen! Vælg en mulighed ⬇️", buttons=normalize_buttons(btns))
        except Exception as e:
            logger.warning(f"EditMessage failed, sending new message: {e}")
            await getattr(ev, 'respond', lambda *a, **k: None)("Velkommen! Vælg en mulighed ⬇️", buttons=normalize_buttons(btns))
        return

    # AI / web commands
    if data.startswith('ai:'):
        prompt = data[3:]
        response = await call_ai_summary(prompt)
        await getattr(ev, 'answer', lambda *a, **k: None)(response, alert=True)
        return

    if data.startswith('web:'):
        query = data[4:]
        results = await web_search(query)
        text = '\n'.join(results.get('results', []))
        await getattr(ev, 'answer', lambda *a, **k: None)(text, alert=True)
        return

    await getattr(ev, 'answer', lambda *a, **k: None)("Ugyldig valg", alert=True)

async def register_handlers(client):
    if TelegramClient is None:
        logger.warning("Cannot register handlers, Telethon not available.")
        return

    @client.on(events.CallbackQuery)
    async def callback(ev):
        await handle_buttons(ev)

async def main():
    if TelegramClient is None:
        logger.warning("Telegram unavailable — running console-only mode.")
        # console-only loop
        while True:
            msg = await asyncio.to_thread(input, "[Console] > ")
            if msg.lower() == 'quit':
                break
            elif msg.startswith('ai '):
                res = await call_ai_summary(msg[3:])
                logger.info(f"AI console response: {res}")
            elif msg.startswith('web '):
                res = await web_search(msg[4:])
                logger.info(f"Web console results: {res}")
        return

    client = TelegramClient(str(SESSIONS / f"{SESSION_NAME}.session"), API_ID, API_HASH)
    await client.start(bot_token=BOT_TOKEN)
    logger.info("✅ NTRLI Superbot running (Telegram mode)")

    await register_handlers(client)

    # Optional console input to send messages directly
    async def console_input():
        while True:
            msg = await asyncio.to_thread(input, "[Console] > ")
            if msg.lower() == 'quit':
                await client.disconnect()
                break
            elif msg.startswith('ai '):
                res = await call_ai_summary(msg[3:])
                logger.info(f"AI console response: {res}")
            elif msg.startswith('web '):
                res = await web_search(msg[4:])
                logger.info(f"Web console results: {res}")

    await asyncio.gather(client.run_until_disconnected(), console_input())(client.run_until_disconnected(), console_input())

# --- Safe async entrypoint ---
if __name__ == '__main__':
    try:
        try:
            loop = asyncio.get_running_loop()
            stop_event = asyncio.Event()
            asyncio.create_task(main())
            logger.info("NTRLI Superbot started in existing event loop.")
            loop.run_until_complete(stop_event.wait())
        except RuntimeError:
            asyncio.run(main())
    except Exception as e:
        logger.exception("Fatal error in main: %s", e)

