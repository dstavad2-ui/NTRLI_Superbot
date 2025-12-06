#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NTRLI Superbot - MASTER BOT
Kombinerer alle 3 bots (NTRLI_sub_bot, NTRLI_Handel_bot, NTRLI_super_bot)
+ NFT Monitor + Auto-generation i ÉN bot
Kører i Command Prompt
"""

import os
import json
import logging
import asyncio
import random
import string
from pathlib import Path
from datetime import datetime
from telethon import TelegramClient, events

# ============ KONFIGURATION ============
BOT_TOKEN_MAIN = '8261354099:AAEewnT0GDcOl5-ARokNVuO5i3zMuLyeG7g'  # NTRLI_super_bot
BOT_TOKEN_SUB = '8546101037:AAHq4U1Y2s9wqHQu5g4hKulnjo-qLT7G7xA'   # NTRLI_sub_bot
BOT_TOKEN_HANDEL = '8111594234:AAHFPH7t24uNjUKI0GctwfwcPk8zKLUR9Xw' # NTRLI_Handel_bot

ADMIN_ID = 8467779489
ADMIN_USERNAME = 'Sir_NTRLI_II'

API_ID = 8546101037
API_HASH = ''

# NFT Konfiguration
NFT_CONFIG = {
    'enabled': True,
    'collection_name': 'NTRLI AI Kollektion',
    'collection_link': 'https://opensea.io/collection/ntrli-ai',
    'blockchain': 'Ethereum',
    'total_nfts': 50,
    'floor_price': '0.5 ETH',
}

RARITET_NIVEAUER = ['Almindelig', 'Ualmindellig', 'Sjælden', 'Epic', 'Legendarisk', 'Mytisk']
TRAITS = {
    'farve': ['Rød', 'Blå', 'Grøn', 'Lilla', 'Guld', 'Sølv', 'Regnbue'],
    'mønster': ['Ensfarvet', 'Gradient', 'Prikker', 'Striber', 'Geometrisk', 'Organisk'],
    'energi': ['Lav', 'Mellem', 'Høj', 'Ekstrem', 'Kosmisk'],
}

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(name)s] - %(levelname)s - %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger('NTRLI_MASTER_BOT')

# Data mapper
DATA_DIR = Path.home() / 'NTRLI_Bot_Data'
DATA_DIR.mkdir(exist_ok=True)
NFT_DIR = Path.home() / 'NTRLI_NFT_Data'
NFT_DIR.mkdir(exist_ok=True)

DATA_FILE = DATA_DIR / 'bot_data.json'
USERS_FILE = DATA_DIR / 'users.json'
NFT_FILE = NFT_DIR / 'nfts.json'
MINT_LOG = NFT_DIR / 'mint_log.json'

# ============ NFT GENERATOR KLASSE ============
class NFTGenerator:
    """Genererer og håndterer NTRLI NFT'er"""
    
    def __init__(self):
        self.nft_collection = self.load_nfts()
        self.mint_log = self.load_mint_log()
        
    def load_nfts(self):
        """Indlæs NFT'er"""
        if NFT_FILE.exists():
            with open(NFT_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_nfts(self):
        """Gem NFT'er"""
        with open(NFT_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.nft_collection, f, indent=2, ensure_ascii=False)
    
    def load_mint_log(self):
        """Indlæs mint-log"""
        if MINT_LOG.exists():
            with open(MINT_LOG, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_mint_log(self):
        """Gem mint-log"""
        with open(MINT_LOG, 'w', encoding='utf-8') as f:
            json.dump(self.mint_log, f, indent=2, ensure_ascii=False)
    
    def generate_nft(self):
        """Generer ny NFT"""
        nft_id = len(self.nft_collection) + 1
        token_id = ''.join(random.choices(string.hexdigits[:16], k=16))
        raritet = random.choices(
            RARITET_NIVEAUER,
            weights=[40, 30, 15, 10, 4, 1]
        )[0]
        
        raritet_priser = {
            'Almindelig': 0.3,
            'Ualmindellig': 0.6,
            'Sjælden': 1.2,
            'Epic': 2.5,
            'Legendarisk': 5.0,
            'Mytisk': 10.0
        }
        
        nft = {
            'id': nft_id,
            'navn': f'NTRLI Genesis #{nft_id}',
            'token_id': token_id,
            'raritet': raritet,
            'traits': {
                'farve': random.choice(TRAITS['farve']),
                'mønster': random.choice(TRAITS['mønster']),
                'energi': random.choice(TRAITS['energi']),
            },
            'pris': raritet_priser[raritet],
            'valuta': 'ETH',
            'minted': datetime.now().isoformat(),
            'ejer': None,
            'marketplace_url': f'https://opensea.io/assets/ethereum/0xNTRLI/{nft_id}',
            'image_url': f'https://nft.ntrli.ai/nft/{nft_id}.png'
        }
        
        self.nft_collection.append(nft)
        self.save_nfts()
        
        mint_entry = {
            'nft_id': nft_id,
            'token_id': token_id,
            'raritet': raritet,
            'timestamp': datetime.now().isoformat(),
            'pris': nft['pris']
        }
        self.mint_log.append(mint_entry)
        self.save_mint_log()
        
        logger.info(f"✨ NFT #{nft_id} genereret - {raritet}")
        return nft
    
    def get_stats(self):
        """Få statistik"""
        if not self.nft_collection:
            return {'total': 0, 'efter_raritet': {}, 'total_værdi': 0}
        
        stats = {
            'total': len(self.nft_collection),
            'efter_raritet': {},
            'total_værdi': 0
        }
        
        for nft in self.nft_collection:
            raritet = nft['raritet']
            stats['efter_raritet'][raritet] = stats['efter_raritet'].get(raritet, 0) + 1
            stats['total_værdi'] += nft['pris']
        
        return stats

# ============ DATA FUNKTIONER ============
def load_data():
    """Indlæs bot data"""
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {'messages': [], 'commands': [], 'nft_views': 0, 'ordrer': []}
    return {'messages': [], 'commands': [], 'nft_views': 0, 'ordrer': []}

def save_data(data):
    """Gem bot data"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Kunne ikke gemme data: {e}")

def get_users():
    """Få brugere"""
    if USERS_FILE.exists():
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def add_user(user_id, username):
    """Tilføj bruger"""
    users = get_users()
    if not any(u['id'] == user_id for u in users):
        users.append({
            'id': user_id,
            'username': username or 'Ukendt',
            'joined': datetime.now().isoformat()
        })
        try:
            with open(USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(users, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Kunne ikke tilføje bruger: {e}")

# ============ BOT SETUP ============
nft_gen = NFTGenerator()
client = TelegramClient('ntrli_master_bot_session', API_ID, API_HASH)

# ============ BOT HANDLERS ============

@client.on(events.NewMessage(pattern='^/start'))
async def start_handler(event):
    """Håndter /start"""
    add_user(event.sender_id, event.sender.username)
    
    msg = f"""
🚀 **NTRLI SUPERBOT - MASTER EDITION**

Hej {event.sender.first_name}! 👋

**Du har adgang til ALT:**
🛍️ Handel (ordrer)
📊 Sub-system
🎨 NFT Markedplads
💰 Generering af NFT'er

**Kommandoer:**
/menu - Se alle muligheder
/nft - NFT kollektion
/bestil - Bestil tjenester
/handel - Handelssystem
/hjælp - Få hjælp

**Status:** ✅ ALLE SYSTEMER ONLINE

Du forbundet til MASTER BOT!
"""
    
    await event.respond(msg, parse_mode='markdown')
    logger.info(f"✓ Bruger {event.sender_id} startet")

@client.on(events.NewMessage(pattern='^/menu'))
async def menu_handler(event):
    """Hovedmenu med alle optioner"""
    msg = """
📋 **NTRLI MASTER BOT - KOMPLET MENU**

**🎨 NFT SYSTEM**
/nft - Se NFT kollektion
/nft_list - Alle NFT'er
/nft_rare - Sjældne NFT'er
/nft_buy - Køb NFT'er
/nft_stats - NFT statistik

**🛒 BESTILLING & HANDEL**
/bestil - Bestil pakke
/ordre - Se mine ordrer
/handel - Handelssystem
/priser - Se prisliste

**📊 INFORMATION**
/status - System status
/info - Om NTRLI
/kontakt - Kontakt info

**🆘 SUPPORT**
/hjælp - Få hjælp
/faq - Ofte stillede spørgsmål

**⚙️ INDSTILLINGER**
/indstil - Dine indstillinger
/sprog - Skift sprog (DA/EN)

Vælg en option! 🎯
"""
    await event.respond(msg, parse_mode='markdown')

@client.on(events.NewMessage(pattern='^/nft'))
async def nft_handler(event):
    """NFT kollektion"""
    msg = f"""
🎨 **NTRLI AI NFT KOLLEKTION**

📊 **Kollektion Info:**
Navn: {NFT_CONFIG['collection_name']}
Blockchain: {NFT_CONFIG['blockchain']}
Antal NFT'er: {NFT_CONFIG['total_nfts']}
Floor Pris: {NFT_CONFIG['floor_price']}

🔗 **Se vores kollektion:**
[OpenSea]({NFT_CONFIG['collection_link']})

📋 **Kommandoer:**
/nft_list - Se alle NFT'er
/nft_rare - Sjældne NFT'er
/nft_buy - Køb NFT'er nu!
/nft_stats - Statistik

**Hver køb støtter NTRLI AI** ✨
"""
    
    await event.respond(msg, parse_mode='markdown')

@client.on(events.NewMessage(pattern='^/nft_stats'))
async def nft_stats_handler(event):
    """NFT statistik"""
    stats = nft_gen.get_stats()
    
    raritet_text = "\n".join([
        f"  {k}: {v} stk"
        for k, v in stats['efter_raritet'].items()
    ])
    
    msg = f"""
📈 **NFT STATISTIK**

📦 **Total NFT'er:** {stats['total']}
💰 **Total værdi:** {stats['total_værdi']:.2f} ETH

**Efter Raritet:**
{raritet_text or 'Ingen NFT'er endnu'}

🔄 **Nye NFT'er mintes hver 5. minut!**
"""
    
    await event.respond(msg, parse_mode='markdown')

@client.on(events.NewMessage(pattern='^/bestil'))
async def bestil_handler(event):
    """Bestilling"""
    msg = """
🛒 **BESTILLINGSSYSTEM**

**Tjeneste Pakker:**

1️⃣ **Standard** - 99 DKK
   ✓ Basis funktioner
   ✓ Email support
   ✓ 30 dages garant

2️⃣ **Pro** - 199 DKK
   ✓ Alle funktioner
   ✓ Prioritet support
   ✓ 90 dages garant

3️⃣ **NFT Holder**
   ✓ Rabat på alle pakker
   ✓ Premium support
   ✓ Eksklusiv adgang

**Admin bestemmer rabatter.**

Svar med **1**, **2** eller **3**
"""
    
    await event.respond(msg, parse_mode='markdown')

@client.on(events.NewMessage(pattern='^/handel'))
async def handel_handler(event):
    """Handelssystem"""
    msg = """
💼 **NTRLI HANDELSSYSTEM**

**Hvad er NTRLI Handel?**
✓ Køb og sælg NFT'er
✓ Markedsinformation
✓ Trading statistik
✓ Portefølje tracking

**Funktioner:**
/handel_stats - Din portefølje
/handel_market - Markedsinfo
/handel_trends - Trends

**Kommende features:**
- Live trading interface
- Automatisk arbitrage
- Social trading

Mere info: /handel_stats
"""
    
    await event.respond(msg, parse_mode='markdown')

@client.on(events.NewMessage(pattern='^/status'))
async def status_handler(event):
    """System status"""
    users = get_users()
    data = load_data()
    stats = nft_gen.get_stats()
    
    msg = f"""
📊 **NTRLI MASTER BOT STATUS**

✅ **System Status:** ONLINE
📡 **Forbindelse:** AKTIV
👥 **Brugere:** {len(users)}
💬 **Kommandoer:** {len(data.get('commands', []))}

**NFT Generator:**
📦 Genereret NFT'er: {stats['total']}
💰 Samlet værdi: {stats['total_værdi']:.2f} ETH
🎨 NFT Visninger: {data.get('nft_views', 0)}

**Ordrer:**
📋 I køen: {len(data.get('ordrer', []))}

**Tid:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Version:** 1.0.0 (MASTER)

🚀 ALT KØRER PERFEKT!
"""
    
    await event.respond(msg, parse_mode='markdown')

@client.on(events.NewMessage(pattern='^/hjælp'))
async def help_handler(event):
    """Hjælp"""
    msg = """
🆘 **NTRLI SUPPORT CENTER**

**Ofte Stillede Spørgsmål:**

❓ Hvordan køber jeg NFT'er?
→ /nft_buy for detaljer

❓ Hvordan bestiller jeg?
→ /bestil og vælg pakke

❓ Kan jeg få rabat?
→ Ja som NFT holder - /handel

❓ Hvad er handel?
→ /handel for info

📧 **Kontakt:**
Email: support@ntrli.dk
Telegram: @Sir_NTRLI_II
Telefon: +45 12 34 56 78

💬 **Vi hjælper 24/7!** ⏰
"""
    
    await event.respond(msg, parse_mode='markdown')

@client.on(events.NewMessage(pattern='^/users'))
async def users_handler(event):
    """Admin: Brugerlist"""
    if event.sender_id != ADMIN_ID:
        await event.respond("❌ Kun administrator")
        return
    
    users = get_users()
    user_list = "\n".join([f"👤 {u['username']} ({u['id']})" for u in users])
    
    msg = f"""
**ADMIN PANEL**

👥 **Brugere:** {len(users)}

{user_list or 'Ingen brugere'}
"""
    
    await event.respond(msg, parse_mode='markdown')

@client.on(events.NewMessage(pattern='^/stats'))
async def admin_stats_handler(event):
    """Admin: Statistik"""
    if event.sender_id != ADMIN_ID:
        await event.respond("❌ Kun administrator")
        return
    
    users = get_users()
    data = load_data()
    nft_stats = nft_gen.get_stats()
    
    msg = f"""
📈 **ADMIN STATISTIK**

👥 Brugere: {len(users)}
💬 Kommandoer: {len(data.get('commands', []))}
📨 Beskeder: {len(data.get('messages', []))}
📋 Ordrer: {len(data.get('ordrer', []))}

**NFT Data:**
📦 Total NFT'er: {nft_stats['total']}
💰 Total værdi: {nft_stats['total_værdi']:.2f} ETH

**Mapper:**
📁 Bot data: {DATA_DIR}
📁 NFT data: {NFT_DIR}
"""
    
    await event.respond(msg, parse_mode='markdown')

@client.on(events.NewMessage())
async def default_handler(event):
    """Default handler"""
    if not event.text.startswith('/'):
        await event.respond(
            "Jeg forstår ikke denne kommando 🤖\n\n"
            "Skriv /menu for at se alle muligheder!\n\n"
            "💡 Eller prøv: /nft, /bestil, /handel"
        )

# ============ NFT AUTO-GENERATION ============
async def auto_mint_loop(client):
    """Auto-mint NFT'er hver 5. minut"""
    logger.info("🔄 Auto-mint loop starter...")
    mint_interval = 300  # 5 minutter
    
    while True:
        try:
            await asyncio.sleep(mint_interval)
            nft = nft_gen.generate_nft()
            
            # Notificier admin
            traits_text = "\n".join([
                f"🎨 {k.capitalize()}: {v}"
                for k, v in nft['traits'].items()
            ])
            
            msg = f"""
✨ **NY NFT MINTET!**

🆔 ID: {nft['id']}
📛 Navn: {nft['navn']}
💎 Raritet: **{nft['raritet']}**
💰 Pris: **{nft['pris']} ETH**

**Traits:**
{traits_text}

🔧 Du har fuld kontrol - Juster pris og raritet som ønsket!
"""
            
            await client.send_message(ADMIN_ID, msg, parse_mode='markdown')
            logger.info(f"📢 Admin notificeret om NFT #{nft['id']}")
            
        except Exception as e:
            logger.error(f"Auto-mint fejl: {e}")

# ============ MAIN ============
async def main():
    """Start master bot"""
    logger.info("=" * 70)
    logger.info("🚀 NTRLI SUPERBOT - MASTER BOT STARTER")
    logger.info("=" * 70)
    
    try:
        async with client:
            logger.info("✅ BOT FORBUNDET TIL TELEGRAM!")
            logger.info(f"👤 Admin: @{ADMIN_USERNAME} (ID: {ADMIN_ID})")
            logger.info(f"🎨 NFT System: AKTIV")
            logger.info(f"💼 Handelssystem: AKTIV")
            logger.info(f"📦 Bestillingssystem: AKTIV")
            logger.info(f"💾 Data: {DATA_DIR}")
            logger.info("")
            logger.info("📋 KOMMANDOER:")
            logger.info("   /start   - Start bot")
            logger.info("   /menu    - Alle kommandoer")
            logger.info("   /nft     - NFT kollektion")
            logger.info("   /bestil  - Bestilling")
            logger.info("   /handel  - Handel")
            logger.info("   /status  - Status")
            logger.info("")
            logger.info("=" * 70)
            logger.info("BOT LYTTER PÅ BESKEDER...")
            logger.info("=" * 70)
            
            # Start auto-mint loop i baggrund
            asyncio.create_task(auto_mint_loop(client))
            
            # Lyt på beskeder
            await client.run_until_disconnected()
            
    except Exception as e:
        logger.error(f"❌ FEJL: {e}")
        logger.error("Kontrollér:")
        logger.error("  1. Bot token er korrekt")
        logger.error("  2. Internet forbindelse virker")
        logger.error("  3. pip install telethon")
        raise

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("NTRLI SUPERBOT - MASTER EDITION")
    print("=" * 70)
    print("\nInstallerer dependencies...")
    
    try:
        import telethon
    except ImportError:
        print("Installerer Telethon...")
        os.system('pip install telethon')
    
    print("\nStarter MASTER BOT...\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n✓ MASTER BOT stoppet")
        logger.info("✓ MASTER BOT stoppet")