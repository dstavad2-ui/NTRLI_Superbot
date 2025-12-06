(stup_and_run.py)
#!/usr/bin/env python3
"""
NTRLI Superbot - Main Setup & Run Script
Initializes environment, loads config, and starts bot
"""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(project_root / 'logs' / 'bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def setup_environment():
    """Create necessary directories and load environment"""
    logger.info("🚀 NTRLI Superbot Starting...")
    
    # Create directories
    dirs = ['data', 'logs', '.backups']
    for dir_name in dirs:
        dir_path = project_root / dir_name
        dir_path.mkdir(exist_ok=True)
        logger.info(f"✓ Directory ready: {dir_name}")
    
    # Load .env
    env_file = project_root / '.env'
    if not env_file.exists():
        logger.warning("⚠️  .env file not found! Using .env.example")
        env_file = project_root / '.env.example'
    
    load_dotenv(env_file)
    logger.info("✓ Environment loaded")
    
    # Verify credentials
    required = ['API_ID', 'API_HASH', 'BOT_TOKEN']
    missing = [k for k in required if not os.getenv(k)]
    
    if missing:
        logger.error(f"❌ Missing credentials: {missing}")
        logger.error("Please configure .env file with Telegram API credentials")
        return False
    
    logger.info("✓ Credentials verified")
    return True

def main():
    """Main entry point"""
    try:
        if not setup_environment():
            sys.exit(1)
        
        logger.info("📡 Importing bot modules...")
        from bot import start_bot
        from self_heal import HealthMonitor
        
        logger.info("✓ Modules imported successfully")
        
        # Start health monitor
        monitor = HealthMonitor()
        monitor.start()
        logger.info("✓ Health monitor started")
        
        # Start bot
        logger.info("🤖 Starting Telegram bot...")
        start_bot()
        
    except KeyboardInterrupt:
        logger.info("\n✓ Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()