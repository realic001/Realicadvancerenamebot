#!/usr/bin/env python3
"""
Telegram Auto Renamer Bot
A comprehensive file renaming bot with inline keyboard shortcuts, banner control panel,
premium system, and support for files up to 5GB.

Usage: python main.py
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def main():
    """Main entry point for the Telegram Auto Renamer Bot"""
    
    # Setup logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        handlers=[
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    
    try:
        # Check for BOT_TOKEN
        bot_token = os.getenv("BOT_TOKEN")
        if not bot_token:
            print("🤖 Auto Renamer Bot - Demo Mode")
            print("=" * 50)
            print("✅ Bot structure created successfully!")
            print("📋 Features implemented:")
            print("   • 26+ Commands with inline keyboards")
            print("   • Auto-rename with custom templates")
            print("   • Banner control panel (START/END/BOTH/DISABLED)")
            print("   • Thumbnail management (Normal/Season/Quality)")
            print("   • Caption formatting (11 styles)")
            print("   • Premium system with referrals")
            print("   • 5GB file support")
            print("   • Comprehensive storage system")
            print("   • File processing pipeline")
            print("   • Template engine with variables")
            print("   • Banner manager for PDFs")
            print()
            print("🔧 To run the bot:")
            print("   1. Get a bot token from @BotFather")
            print("   2. Set environment variable: BOT_TOKEN=your_token")
            print("   3. Run: python main.py")
            print()
            print("📁 Project structure:")
            print("   • main.py - Entry point")
            print("   • config.py - Configuration")
            print("   • bot/ - Bot modules")
            print("   • utils/ - Utility functions")
            print("   • README.md - Complete documentation")
            print()
            print("🚀 Ready for deployment on:")
            print("   • Railway, Heroku, VPS")
            print("   • Koyeb, Render")
            print("   • Any Python hosting platform")
            
            # Keep the demo running
            print("\n⏳ Demo mode - Press Ctrl+C to exit")
            try:
                await asyncio.Event().wait()
            except KeyboardInterrupt:
                print("\n👋 Demo stopped")
            return
        
        # Import and run the actual bot
        from bot.main import AutoRenamerBot
        
        logger.info("Starting Telegram Auto Renamer Bot...")
        
        # Create and setup bot
        bot = AutoRenamerBot()
        await bot.setup_application()
        
        # Check if running in web server mode
        web_server = os.getenv("WEB_SERVER", "false").lower() == "true"
        
        if web_server:
            await bot.setup_webhook()
            await bot.start_webhook()
        else:
            await bot.start_polling()
            
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())