"""
Main bot application entry point
Handles bot initialization, webhook setup, and command routing
"""

import asyncio
import logging
from pathlib import Path
from aiohttp import web, ClientSession
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from config import *
from bot.handlers import (
    start_handler, help_handler, settings_handler,
    autorename_handler, preview_handler, mode_handler, replace_handler,
    banner_handler, thumbnail_mode_handler, caption_mode_handler,
    premium_handler, refer_handler, leaderboard_handler,
    metadata_handler, setmediatype_handler, getthumb_handler,
    dumpsettings_handler, deldump_handler, top_referrals_handler,
    elites_handler, features_handler, about_handler, admin_cmd_handler,
    file_handler, callback_query_handler
)

logger = logging.getLogger(__name__)

class AutoRenamerBot:
    def __init__(self):
        self.application = None
        self.web_app = None
        
    async def setup_application(self):
        """Initialize the telegram bot application"""
        self.application = Application.builder().token(BOT_TOKEN).build()
        
        # Register command handlers
        self.application.add_handler(CommandHandler("start", start_handler))
        self.application.add_handler(CommandHandler("help", help_handler))
        self.application.add_handler(CommandHandler("settings", settings_handler))
        
        # Rename system handlers
        self.application.add_handler(CommandHandler("autorename", autorename_handler))
        self.application.add_handler(CommandHandler("preview", preview_handler))
        self.application.add_handler(CommandHandler("mode", mode_handler))
        self.application.add_handler(CommandHandler("replace", replace_handler))
        self.application.add_handler(CommandHandler("renamesource", lambda u, c: None))  # Placeholder
        
        # File and metadata handlers
        self.application.add_handler(CommandHandler("metadata", metadata_handler))
        self.application.add_handler(CommandHandler("setmediatype", setmediatype_handler))
        self.application.add_handler(CommandHandler("getthumb", getthumb_handler))
        
        # Thumbnail management handlers
        self.application.add_handler(CommandHandler("thumbnail_mode", thumbnail_mode_handler))
        self.application.add_handler(CommandHandler("allthumb", lambda u, c: None))  # Placeholder
        self.application.add_handler(CommandHandler("del_thumb", lambda u, c: None))  # Placeholder
        
        # Season thumbnail handlers (s01-s10)
        for i in range(1, 11):
            season_num = f"{i:02d}"
            self.application.add_handler(CommandHandler(f"thums{season_num}", lambda u, c: None))
            self.application.add_handler(CommandHandler(f"delthumbs{season_num}", lambda u, c: None))
        
        # Quality thumbnail handlers
        for quality in QUALITY_OPTIONS:
            quality_num = quality.replace("p", "")
            self.application.add_handler(CommandHandler(f"thum{quality_num}", lambda u, c: None))
            self.application.add_handler(CommandHandler(f"delthum{quality_num}", lambda u, c: None))
        
        # Banner and caption handlers
        self.application.add_handler(CommandHandler("banner", banner_handler))
        self.application.add_handler(CommandHandler("caption_mode", caption_mode_handler))
        
        # Dump management handlers
        self.application.add_handler(CommandHandler("dumpsettings", dumpsettings_handler))
        self.application.add_handler(CommandHandler("deldump", deldump_handler))
        
        # Social and premium handlers
        self.application.add_handler(CommandHandler("leaderboard", leaderboard_handler))
        self.application.add_handler(CommandHandler("top_referrals", top_referrals_handler))
        self.application.add_handler(CommandHandler("refer", refer_handler))
        self.application.add_handler(CommandHandler("premium", premium_handler))
        self.application.add_handler(CommandHandler("elites", elites_handler))
        self.application.add_handler(CommandHandler("features", features_handler))
        self.application.add_handler(CommandHandler("about", about_handler))
        
        # Admin handlers
        self.application.add_handler(CommandHandler("admin_cmd", admin_cmd_handler))
        
        # File and callback handlers
        self.application.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO | filters.VIDEO | filters.AUDIO, file_handler))
        self.application.add_handler(CallbackQueryHandler(callback_query_handler))
        
        logger.info("Bot handlers registered successfully")
    
    async def setup_webhook(self):
        """Setup webhook for production deployment"""
        if WEB_SERVER and WEBHOOK_URL:
            # Create web application for webhook
            self.web_app = web.Application()
            
            # Add webhook route
            self.web_app.router.add_post(WEBHOOK_PATH, self.webhook_handler)
            
            # Add health check route
            self.web_app.router.add_get("/health", self.health_check)
            
            # Set webhook
            await self.application.bot.set_webhook(
                url=WEBHOOK_URL + WEBHOOK_PATH,
                allowed_updates=Update.ALL_TYPES
            )
            
            logger.info(f"Webhook set to: {WEBHOOK_URL + WEBHOOK_PATH}")
    
    async def webhook_handler(self, request):
        """Handle incoming webhook requests"""
        try:
            data = await request.json()
            update = Update.de_json(data, self.application.bot)
            await self.application.process_update(update)
            return web.Response(status=200)
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return web.Response(status=500)
    
    async def health_check(self, request):
        """Health check endpoint"""
        return web.json_response({"status": "healthy", "bot": "auto_renamer"})
    
    async def start_polling(self):
        """Start polling mode for development"""
        logger.info("Starting bot in polling mode...")
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        
        try:
            # Keep the bot running
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info("Stopping bot...")
        finally:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
    
    async def start_webhook(self):
        """Start webhook mode for production"""
        logger.info(f"Starting bot in webhook mode on {HOST}:{PORT}")
        await self.application.initialize()
        await self.application.start()
        
        # Create and start web server
        runner = web.AppRunner(self.web_app)
        await runner.setup()
        site = web.TCPSite(runner, HOST, PORT)
        await site.start()
        
        logger.info(f"Bot server started on http://{HOST}:{PORT}")
        
        try:
            # Keep the server running
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info("Stopping bot...")
        finally:
            await self.application.stop()
            await self.application.shutdown()
            await runner.cleanup()

async def main():
    """Main entry point"""
    # Setup logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )
    
    # Create bot instance
    bot = AutoRenamerBot()
    
    # Setup application
    await bot.setup_application()
    
    # Start bot based on configuration
    if WEB_SERVER:
        await bot.setup_webhook()
        await bot.start_webhook()
    else:
        await bot.start_polling()

if __name__ == "__main__":
    asyncio.run(main())