#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NTRLI Superbot - Setup & Run Script (Dansk)
Initialiserer miljø, indlæser config, starter bot
"""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Føj projekt til path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup logging med Unicode support
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(project_root / 'logs' / 'bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ],
    encoding='utf-8'
)
logger = logging.getLogger(__name__)

def setup_environment():
    """Opret nødvendige mapper og indlæs miljø"""
    logger.info("🚀 NTRLI Superbot starter...")
    
    # Opret mapper
    dirs = ['data', 'logs', '.backups']
    for dir_name in dirs:
        dir_path = project_root / dir_name
        dir_path.mkdir(exist_ok=True)
        logger.info(f"✓ Mappe klar: {dir_name}")
    
    # Indlæs .env
    env_file = project_root / '.env'
    if not env_file.exists():
        logger.warning("⚠️  .env fil ikke fundet! Bruger .env.example")
        env_file = project_root / '.env.example'
    
    load_dotenv(env_file)
    logger.info("✓ Miljø indlæst")
    
    # Verificer credentials
    required = ['API_ID', 'API_HASH', 'BOT_TOKEN']
    missing = [k for k in required if not os.getenv(k)]
    
    if missing:
        logger.error(f"❌ Manglende credentials: {missing}")
        logger.error("Konfigurér venligst .env fil med Telegram API credentials")
        return False
    
    logger.info("✓ Credentials verificeret")
    return True

def main():
    """Hoved indgangspunkt"""
    try:
        if not setup_environment():
            sys.exit(1)
        
        logger.info("📡 Importerer bot moduler...")
        from bot_nft import main as start_bot
        
        logger.info("✓ Moduler importeret med succes")
        
        # Start bot
        logger.info("🤖 Starter Telegram bot...")
        
        import asyncio
        asyncio.run(start_bot())
        
    except KeyboardInterrupt:
        logger.info("\n✓ Bot stoppet af bruger")
    except Exception as e:
        logger.error(f"❌ Fatal fejl: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()