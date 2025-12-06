#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NTRLI Superbot - Launch Script
Starts the master bot system
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger('NTRLI_LAUNCHER')

def check_env():
    """Verify .env file exists and has required values"""
    logger.info("📋 Checking environment configuration...")
    
    env_file = Path('.env')
    if not env_file.exists():
        logger.error("❌ .env file not found!")
        logger.error("Create .env with:")
        logger.error("  API_ID=8546101037")
        logger.error("  API_HASH=7defa4b44a90dd22ed93ec4bf36374d4")
        logger.error("  BOT_TOKEN=8261354099:AAEewnT0GDcOl5-ARokNVuO5i3zMuLyeG7g")
        logger.error("  ADMIN_ID=8467779489")
        logger.error("  ADMIN_USERNAME=Sir_NTRLI_II")
        return False
    
    logger.info("✓ .env file found")
    return True

def check_dependencies():
    """Verify Python packages are installed"""
    logger.info("📦 Checking dependencies...")
    
    required = ['telethon', 'dotenv']
    missing = []
    
    for pkg in required:
        try:
            __import__(pkg)
            logger.info(f"✓ {pkg} installed")
        except ImportError:
            missing.append(pkg)
    
    if missing:
        logger.warning(f"⚠️  Missing packages: {missing}")
        logger.info("Installing dependencies...")
        os.system('pip install telethon python-dotenv')
    
    return True

def create_directories():
    """Create required directories"""
    logger.info("📁 Creating directories...")
    
    dirs = ['data', 'logs', '.backups']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        logger.info(f"✓ {dir_name}/")
    
    return True

def load_env():
    """Load environment variables"""
    from dotenv import load_dotenv
    load_dotenv()
    logger.info("✓ Environment variables loaded")

async def start_bot():
    """Import and start the master bot"""
    logger.info("")
    logger.info("=" * 70)
    logger.info("🚀 STARTING NTRLI SUPERBOT")
    logger.info("=" * 70)
    logger.info("")
    
    try:
        # Import master bot
        from mater_bot import main as start_master_bot
        
        logger.info("✓ Master bot imported")
        logger.info("")
        logger.info("📡 Connecting to Telegram...")
        logger.info("")
        
        # Start the bot
        await start_master_bot()
        
    except ImportError as e:
        logger.error(f"❌ Could not import master bot: {e}")
        logger.error("Make sure mater_bot.py exists in current directory")
        return False
    except KeyboardInterrupt:
        logger.info("\n✓ Bot stopped by user")
        return True
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False

def main():
    """Main launcher function"""
    print("\n" + "=" * 70)
    print("   NTRLI SUPERBOT - LAUNCHER")
    print("=" * 70 + "\n")
    
    # Check environment
    if not check_env():
        return False
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Create directories
    if not create_directories():
        return False
    
    # Load environment
    load_env()
    
    logger.info("✓ All checks passed!\n")
    
    # Start bot
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        logger.info("\n✓ Launcher stopped")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)