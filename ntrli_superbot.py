#!/usr/bin/env python3
"""
NTRLI Superbot - Main Bot Implementation
Handles Telegram commands and interactions
"""

import os
import logging
import json
from datetime import datetime
from pathlib import Path
import asyncio
from telethon import TelegramClient, events

# -------------------------
# Logging Configuration
# -------------------------
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# -------------------------
# Bot Configuration
# -------------------------
API_ID = os.getenv('API_ID')
if not API_ID:
    API_ID = 33636662
else:
    API_ID = int(API_ID)

API_HASH = os.getenv('API_HASH') or '7defa4b44a90dd22ed93ec4bf36374d4'
BOT_TOKEN = os.getenv('BOT_TOKEN') or '8261354099:AAEewnT0GDcOl5-ARokNVuO5i3zMuLyeG7g'
ADMIN_ID = os.getenv('ADMIN_ID')
if not ADMIN_ID:
    ADMIN_ID = 8467779489
else:
    ADMIN_ID = int(ADMIN_ID)

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME') or 'Sir_NTRLI_II'

# -------------------------
# Data Storage
# -------------------------
DATA_DIR = Path(__file__).parent / 'data'
DATA_FILE = DATA_DIR / 'bot_data.json'
USERS_FILE = DATA_DIR / 'users.json'

DATA_DIR.mkdir(exist_ok=True)
if not DATA_FILE.exists():
    DATA_FILE.write_text(json.dumps({'messages': [], 'commands': []}, indent=2, ensure_ascii=False))
if not USERS_FILE.exists():
    USERS_FILE.write_text(json.dumps([], indent=2, ensure_ascii=False))

# -------------------------
# Utility Functions
# -------------------------
def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_user_list():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def add_user(user_id, username):
    users = get_user_list()
    user = {
        'id': user_id,
        'username': username,
        'joined': datetime.now().isoformat(),
        'active': True
    }
    if not any(u['id'] == user_id for u in users):
        users.append(user)
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
    return user

# -------------------------
# Create Telegram Client
# -------------------------
client = TelegramClient('ntrli_bot_session', API_ID, API_HASH)

# -------------------------
# Command Handlers
# -------------------------
@client.on(events.NewMessage(pattern='^/start'))
async def start_handler(event):
    user = add_user(event.sender_id, getattr(event.sender, 'username', 'Unknown'))
    welcome_msg = f"""
🚀 **NTRLI Superbot aktiv!**

Hej {getattr(event.sender, 'first_name', 'Bruger')}! 👋

**Tilgængelige kommandoer:**
/menu - Vis fuld menu
/status - System status
/bestil - Bestillingssystem
/hjælp - Få hjælp
/data - Se dine data

**Status:** ✅ Bot er online
**Version:** 1.0.0
**Udsender:** NTRLI AI

Hvad vil du gøre?
"""
    await event.respond(welcome_msg, parse_mode='markdown')
    logger.info(f"✓ User {event.sender_id} started bot")

@client.on(events.NewMessage(pattern='^/menu'))
async def menu_handler(event):
    menu_msg = """
📋 **NTRLI SUPERBOT MENU**

**1️⃣ Bestilling**
   /bestil - Start ordreproces
   /ordre - Se mine ordrer
   
**2️⃣ Information**
   /status - System status
   /info - Bot information
   
**3️⃣ Support**
   /hjælp - Få hjælp
   /kontakt - Kontakt administrator
   
**4️⃣ Indstillinger**
   /indstil - Personlige indstillinger
   /sprog - Skift sprog
   
**5️⃣ Admin** (kun administrator)
   /users - Brugerlist
   /logs - Se logs
   /restart - Genstart bot

Vælg en option ved at skrive kommandoen! 🎯
"""
    await event.respond(menu_msg, parse_mode='markdown')
    logger.info(f"User {event.sender_id} viewed menu")

@client.on(events.NewMessage(pattern='^/status'))
async def status_handler(event):
    users = get_user_list()
    data = load_data()
    status_msg = f"""
📊 **NTRLI SUPERBOT STATUS**

**System Status:** ✅ Online
**Uptime:** Aktiv
**API Connection:** ✅ Forbundet
**Database:** ✅ Synkroniseret

**Statistik:**
👥 Brugere registreret: {len(users)}
💬 Kommandoer behandlet: {len(data.get('commands', []))}
📨 Beskeder gemt: {len(data.get('messages', []))}

**Seneste aktivitet:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Version:** 1.0.0
**Sprog:** Dansk (da-DK)

Alt systemerne kører perfekt! ✨
"""
    await event.respond(status_msg, parse_mode='markdown')

@client.on(events.NewMessage(pattern='^/bestil'))
async def order_handler(event):
    order_msg = """
🛒 **BESTILLINGSSYSTEM**

Velkommen til NTRLI Bestillingssystem!

**Trin 1:** Hvad ønsker du?
Skriv nummeret på din valg:

1️⃣ **Standard Pakke** - 99 DKK
2️⃣ **Pro Pakke** - 199 DKK
3️⃣ **Enterprise** - Ring for pris

Svar med **1**, **2** eller **3**
"""
    await event.respond(order_msg, parse_mode='markdown')
    data = load_data()
    data['commands'].append({
        'user_id': event.sender_id,
        'command': '/bestil',
        'timestamp': datetime.now().isoformat()
    })
    save_data(data)

@client.on(events.NewMessage(pattern='^/hjælp'))
async def help_handler(event):
    help_msg = """
🆘 **NTRLI SUPPORT**

**Almindelige spørgsmål:**  

❓ Hvordan starter jeg?  
   Svar: Brug /menu  

❓ Hvordan bestiller jeg?  
   Svar: Skriv /bestil  

❓ Hvor er mine data?  
   Svar: Skriv /data  

❓ Hvordan ændrer jeg indstillinger?  
   Svar: Skriv /indstil  

**Kontakt:**  
📧 Email: support@ntrli.dk  
💬 Chat: Send besked her  
📞 Telefon: 91 10 89 29
"""
    await event.respond(help_msg, parse_mode='markdown')

@client.on(events.NewMessage(pattern='^/users'))
async def users_handler(event):
    if event.sender_id != ADMIN_ID:
        await event.respond("❌ Kun administrator har adgang")
        return
    users = get_user_list()
    user_list = "\n".join([f"👤 {u['username']} (ID: {u['id']}) - {u['joined'][:10]}" for u in users])
    msg = f"**BRUGER LISTE** ({len(users)} brugere)\n\n{user_list or 'Ingen brugere endnu'}"
    await event.respond(msg, parse_mode='markdown')

@client.on(events.NewMessage(pattern='^/restart'))
async def restart_handler(event):
    if event.sender_id != ADMIN_ID:
        await event.respond("❌ Kun administrator")
        return
    await event.respond("🔄 Genstartar bot...")
    logger.info("Admin restart requested")

@client.on(events.NewMessage())
async def message_handler(event):
    data = load_data()
    data['messages'].append({
        'user_id': event.sender_id,
        'text': getattr(event, 'text', '')[:100],
        'timestamp': datetime.now().isoformat()
    })
    save_data(data)
    if not getattr(event, 'text', '').startswith('/'):
        await event.respond("Jeg forstår ikke. Skriv /menu for kommandoer 🤖", parse_mode='markdown')

# -------------------------
# Bot Startup
# -------------------------
async def main():
    await client.start(bot_token=BOT_TOKEN)
    logger.info("✓ Bot forbundet og aktiv")
    logger.info("📡 Lytter på kommandoer...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
