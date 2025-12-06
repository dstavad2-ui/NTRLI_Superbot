#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NTRLI Superbot - STANDALONE LAUNCHER
Everything in ONE file - no dependencies on other scripts
Just run: python start.py
"""

import os
import sys
import json
import asyncio
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger('NTRLI')

print("\n" + "=" * 70)
print("  NTRLI SUPERBOT - STANDALONE LAUNCHER")
print("=" * 70 + "\n")

# ============ STEP 1: Check Python ============
print("[..] Checking Python version...")
version = sys.version_info
if version.major >= 3 and version.minor >= 8:
    print(f"[OK] Python {version.major}.{version.minor}.{version.micro}\n")
else:
    print(f"[XX] Python 3.8+ required, found {version.major}.{version.minor}")
    sys.exit(1)

# ============ STEP 2: Install Dependencies ============
print("[..] Checking dependencies...")
required = ['telethon', 'dotenv']
for pkg in required:
    try:
        __import__(pkg)
        print(f"[OK] {pkg}")
    except ImportError:
        print(f"[..] Installing {pkg}...")
        if pkg == 'dotenv':
            os.system('pip install -q python-dotenv')
        else:
            os.system(f'pip install -q {pkg}')
        print(f"[OK] {pkg} installed")

print()

# ============ STEP 3: Create Directories ============
print("[..] Creating directories...")
for dir_name in ['data', 'logs', '.backups']:
    Path(dir_name).mkdir(exist_ok=True)
    print(f"[OK] {dir_name}/")

print()

# ============ STEP 4: Create .env ============
print("[..] Checking .env file...")
env_file = Path('.env')
if not env_file.exists():
    print("[..] Creating .env...")
    env_content = """API_ID=33636662
API_HASH=7defa4b44a90dd22ed93ec4bf36374d4
BOT_TOKEN=8261354099:AAEewnT0GDcOl5-ARokNVuO5i3zMuLyeG7g
ADMIN_ID=8467779489
ADMIN_USERNAME=Sir_NTRLI_II
"""
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(env_content)
    print("[OK] .env created")
else:
    print("[OK] .env exists")

print()

# ============ STEP 5: Load Environment ============
print("[..] Loading environment...")
from dotenv import load_dotenv
load_dotenv()
print("[OK] Environment loaded\n")

# ============ STEP 6: Initialize Data Files ============
print("[..] Initializing data files...")
data_dir = Path('data')

bot_data_file = data_dir / 'bot_data.json'
if not bot_data_file.exists():
    with open(bot_data_file, 'w', encoding='utf-8') as f:
        json.dump({'messages': [], 'commands': [], 'nft_views': 0, 'ordrer': []}, f)
    print("[OK] bot_data.json created")
else:
    print("[OK] bot_data.json exists")

users_file = data_dir / 'users.json'
if not users_file.exists():
    with open(users_file, 'w', encoding='utf-8') as f:
        json.dump([], f)
    print("[OK] users.json created")
else:
    print("[OK] users.json exists")

nft_file = Path.home() / 'NTRLI_NFT_Data' / 'nfts.json'
nft_file.parent.mkdir(exist_ok=True)
if not nft_file.exists():
    with open(nft_file, 'w', encoding='utf-8') as f:
        json.dump([], f)
    print("[OK] nfts.json created")

print()
print("[OK] All systems ready!\n")

# ============ STEP 7: Start Master Bot ============
print("=" * 70)
print("  STARTING NTRLI MASTER BOT")
print("=" * 70 + "\n")

async def start_bot():
    """Start the master bot"""
    try:
        # Find and import the master bot
        bot_files = [
            'mater_bot.py',
            'master_bot', 
            'mater_bot.py',
            'bot.py'
        ]
        
        imported = False
        for bot_file in bot_files:
            if Path(bot_file).exists():
                print(f"[..] Found: {bot_file}\n")
                
                # Import dynamically
                import importlib.util
                spec = importlib.util.spec_from_file_location("bot_module", bot_file)
                bot_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(bot_module)
                
                # Run the bot
                if hasattr(bot_module, 'main'):
                    await bot_module.main()
                else:
                    print(f"[XX] No main() function in {bot_file}")
                
                imported = True
                break
        
        if not imported:
            print("[XX] No master bot file found!")
            print("    Expected: mater_bot.py.py, master_bot.py, or mater_bot.py")
            return False
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n[OK] Bot stopped by user")
        return True
    except Exception as e:
        print(f"\n[XX] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

# Run the bot
try:
    asyncio.run(start_bot())
except KeyboardInterrupt:
    print("\n[OK] Launcher stopped")
except Exception as e:
    print(f"[XX] Fatal error: {e}")
    sys.exit(1)