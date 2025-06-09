"""
Configuration file for Telegram Auto Renamer Bot
Environment variables for customization and deployment
"""

import os
from pathlib import Path

# Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required")

# Bot Appearance
START_PHOTO = os.getenv("START_PHOTO", "https://via.placeholder.com/800x400?text=Auto+Renamer+Bot")
CUSTOM_WELCOME_MSG = os.getenv("CUSTOM_WELCOME_MSG", 
    "🤖 Welcome to Auto Renamer Bot!\n\n"
    "I can help you rename files up to 5GB with advanced features:\n"
    "• Custom templates with variables\n"
    "• Banner control for PDFs\n"
    "• Advanced thumbnail management\n"
    "• Premium features available\n\n"
    "Use /help to see all commands or the menu below to get started!"
)

# Server Configuration
WEB_SERVER = os.getenv("WEB_SERVER", "true").lower() == "true"
PORT = int(os.getenv("PORT", 8080))
HOST = "0.0.0.0" if WEB_SERVER else "127.0.0.1"

# Webhook Configuration (for deployment)
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"

# File Configuration
MAX_FILE_SIZE = 5 * 1024 * 1024 * 1024  # 5GB in bytes
DOWNLOAD_PATH = Path("downloads")
TEMP_PATH = Path("temp")
THUMBNAILS_PATH = Path("thumbnails")

# Create directories
DOWNLOAD_PATH.mkdir(exist_ok=True)
TEMP_PATH.mkdir(exist_ok=True)
THUMBNAILS_PATH.mkdir(exist_ok=True)

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bot_data.db")

# Premium System
PREMIUM_FEATURES = {
    "unlimited_renames": True,
    "priority_processing": True,
    "custom_thumbnails": True,
    "advanced_analytics": True,
    "api_access": True
}

# Referral System
REFERRAL_BONUS_HOURS = 3
REFERRAL_POINTS_PER_USER = 10

# Admin Configuration
ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "bot.log")

# Rate Limiting
MAX_REQUESTS_PER_MINUTE = 30
MAX_FILE_UPLOADS_PER_HOUR = 50

# Template Variables
DEFAULT_VARIABLES = [
    "title", "season", "episode", "audio", "quality", 
    "volume", "chapter", "year", "resolution", "codec"
]

# Caption Modes
CAPTION_MODES = [
    "Normal", "No Cap", "Quote", "Bold", "Italic", 
    "Underline", "Mono", "Strikethrough", "Spoiler", 
    "Reverse", "Link"
]

# Thumbnail Modes
THUMBNAIL_MODES = {
    "normal": "Single thumbnail for all files",
    "season": "Separate thumbnails per season (s01-s10)",
    "quality": "Thumbnails by quality (144p-8000p)"
}

# Quality Options
QUALITY_OPTIONS = [
    "144p", "240p", "360p", "480p", "720p", "1080p", 
    "1440p", "2160p", "4000p", "8000p"
]

# Season Options
SEASON_OPTIONS = [f"s{i:02d}" for i in range(1, 11)]  # s01 to s10

# Banner Positions
BANNER_POSITIONS = ["START", "END", "BOTH", "DISABLED"]

# File Extensions
SUPPORTED_VIDEO_EXTENSIONS = [
    ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", 
    ".webm", ".m4v", ".3gp", ".ts", ".mts"
]

SUPPORTED_AUDIO_EXTENSIONS = [
    ".mp3", ".flac", ".wav", ".aac", ".ogg", ".wma", 
    ".m4a", ".opus", ".aiff"
]

SUPPORTED_DOCUMENT_EXTENSIONS = [
    ".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", 
    ".xls", ".xlsx", ".ppt", ".pptx", ".zip", ".rar"
]

SUPPORTED_IMAGE_EXTENSIONS = [
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", 
    ".webp", ".svg", ".ico"
]

# API Configuration
API_TIMEOUT = 30
CHUNK_SIZE = 1024 * 1024  # 1MB chunks for file processing

# Feature Flags
FEATURES = {
    "file_renaming": True,
    "banner_control": True,
    "thumbnail_management": True,
    "premium_system": True,
    "referral_system": True,
    "analytics": True,
    "leaderboards": True,
    "dump_management": True,
    "metadata_editing": True,
    "batch_processing": True
}

# Messages
MESSAGES = {
    "start": CUSTOM_WELCOME_MSG,
    "help": "📚 **Available Commands:**\n\n"
            "🔧 **Basic Commands:**\n"
            "/start - Start the bot\n"
            "/help - Show this help message\n"
            "/settings - View your settings\n\n"
            "✏️ **Rename Commands:**\n"
            "/autorename - Set auto-rename template\n"
            "/preview - Preview rename format\n"
            "/mode - Change rename mode\n"
            "/replace - Set text replacement\n\n"
            "🎨 **Customization:**\n"
            "/banner - Banner control panel\n"
            "/thumbnail_mode - Thumbnail settings\n"
            "/caption_mode - Caption formatting\n\n"
            "💎 **Premium & Social:**\n"
            "/premium - Premium features\n"
            "/refer - Refer friends\n"
            "/leaderboard - Top users\n\n"
            "Send me any file to start renaming!",
    
    "no_file": "❌ Please send me a file to rename.",
    "file_too_large": f"❌ File too large! Maximum size is {MAX_FILE_SIZE // (1024**3)}GB.",
    "processing": "⏳ Processing your file...",
    "download_progress": "📥 Downloading... {progress}%",
    "upload_progress": "📤 Uploading... {progress}%",
    "rename_success": "✅ File renamed successfully!",
    "error": "❌ An error occurred: {error}",
    "premium_required": "💎 This feature requires premium membership.\nUse /premium to upgrade!",
    "rate_limited": "⏳ Please wait before sending another request.",
}