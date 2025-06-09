"""
Bot handlers for all commands and interactions
Implements the complete command set with inline keyboard support
"""

import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from config import *
from bot.keyboards import *
from bot.storage import get_user_storage
from utils.file_processor import FileProcessor
from utils.template_engine import TemplateEngine
from utils.banner_manager import BannerManager

# Command Handlers

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command with welcome image and inline keyboard"""
    user = update.effective_user
    storage = get_user_storage(user.id)
    
    # Initialize user if new
    if not storage.get_user_settings():
        storage.initialize_user(user.id, user.first_name or "User")
    
    # Send welcome image if configured
    if START_PHOTO and START_PHOTO.startswith("http"):
        try:
            await update.message.reply_photo(
                photo=START_PHOTO,
                caption=MESSAGES["start"],
                reply_markup=get_main_menu_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
        except:
            # Fallback to text if image fails
            await update.message.reply_text(
                MESSAGES["start"],
                reply_markup=get_main_menu_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
    else:
        await update.message.reply_text(
            MESSAGES["start"],
            reply_markup=get_main_menu_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(
        MESSAGES["help"],
        reply_markup=get_help_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def settings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /settings command"""
    user = update.effective_user
    storage = get_user_storage(user.id)
    settings = storage.get_user_settings()
    
    settings_text = f"""
⚙️ **Your Current Settings**

**Rename Mode:** {settings.get('rename_mode', 'autorename')}
**Template:** {settings.get('template', 'Not set')}
**Thumbnail Mode:** {settings.get('thumbnail_mode', 'normal')}
**Caption Mode:** {settings.get('caption_mode', 'Normal')}
**Banner Status:** {'Enabled' if settings.get('banner_enabled') else 'Disabled'}
**Premium Status:** {'Active' if settings.get('is_premium') else 'Free'}

Use the buttons below to modify your settings.
"""
    
    await update.message.reply_text(
        settings_text,
        reply_markup=get_settings_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

# Rename System Handlers

async def autorename_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /autorename command"""
    await update.message.reply_text(
        "🔧 **Auto-Rename Template Setup**\n\n"
        "Create a custom template using variables:\n"
        "• {title} - File title\n"
        "• {season} - Season number\n"
        "• {episode} - Episode number\n"
        "• {audio} - Audio format\n"
        "• {quality} - Video quality\n"
        "• {volume} - Volume info\n"
        "• {chapter} - Chapter number\n\n"
        "Example: `S{season} E{episode} - {title} [{audio}] {quality}`",
        reply_markup=get_autorename_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def preview_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /preview command"""
    user = update.effective_user
    storage = get_user_storage(user.id)
    settings = storage.get_user_settings()
    
    template = settings.get('template', 'Not set')
    if template == 'Not set':
        await update.message.reply_text(
            "❌ No template set. Use /autorename to create one first.",
            reply_markup=get_back_keyboard()
        )
        return
    
    # Generate preview with sample data
    engine = TemplateEngine()
    sample_data = {
        'title': 'Sample Movie',
        'season': '01',
        'episode': '01',
        'audio': 'AAC',
        'quality': '1080p',
        'volume': 'Vol1',
        'chapter': '01'
    }
    
    preview = engine.apply_template(template, sample_data)
    
    await update.message.reply_text(
        f"🔍 **Template Preview**\n\n"
        f"**Template:** `{template}`\n"
        f"**Preview:** `{preview}`\n\n"
        f"This is how your files will be renamed.",
        reply_markup=get_preview_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def mode_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /mode command"""
    await update.message.reply_text(
        "📝 **Select Rename Mode**\n\n"
        "• **Autorename** - Use your predefined template\n"
        "• **Manual** - Enter custom name for each file\n"
        "• **Replace** - Replace specific text in filenames",
        reply_markup=get_mode_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def replace_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /replace command"""
    if context.args and len(context.args) >= 1:
        # Parse replace arguments
        arg_text = " ".join(context.args)
        if "|" in arg_text:
            old_text, new_text = arg_text.split("|", 1)
            old_text = old_text.strip()
            new_text = new_text.strip()
            
            user = update.effective_user
            storage = get_user_storage(user.id)
            storage.set_replace_rule(old_text, new_text)
            
            await update.message.reply_text(
                f"✅ **Replace Rule Set**\n\n"
                f"**Replace:** `{old_text}`\n"
                f"**With:** `{new_text}`\n\n"
                f"This rule will be applied to all file renames.",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                "❌ Invalid format. Use: `/replace old_text | new_text`",
                parse_mode=ParseMode.MARKDOWN
            )
    else:
        await update.message.reply_text(
            "🔄 **Text Replacement Setup**\n\n"
            "Set up text replacement rules for automatic file renaming.\n\n"
            "**Usage:** `/replace old_text | new_text`\n"
            "**Example:** `/replace .mkv | .mp4`",
            reply_markup=get_replace_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )

# Banner and Customization Handlers

async def banner_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /banner command - Banner Control Panel"""
    user = update.effective_user
    storage = get_user_storage(user.id)
    settings = storage.get_user_settings()
    
    banner_status = "Enabled" if settings.get('banner_enabled') else "Disabled"
    banner_image = settings.get('banner_image', 'None set')
    banner_position = settings.get('banner_position', 'START')
    banner_link = settings.get('banner_link', 'None set')
    
    banner_text = f"""
🎨 **Banner Control Panel**

**STATUS:** {banner_status}
**IMAGE:** {banner_image}
**POSITION:** {banner_position}
**LINK:** {banner_link}

Use the buttons below to configure your banner settings.
Banner will be added to PDF files and other supported formats.
"""
    
    await update.message.reply_text(
        banner_text,
        reply_markup=get_banner_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def thumbnail_mode_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /thumbnail_mode command"""
    await update.message.reply_text(
        "📷 **Thumbnail Mode Selection**\n\n"
        "• **Normal** - Single thumbnail for all files\n"
        "• **Season** - Separate thumbnails per season (s01-s10)\n"
        "• **Quality** - Thumbnails by quality (144p-8000p)\n\n"
        "Choose your preferred thumbnail management mode:",
        reply_markup=get_thumbnail_mode_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def caption_mode_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /caption_mode command"""
    await update.message.reply_text(
        "💬 **Caption Formatting Options**\n\n"
        "Select how you want your file captions to be formatted:",
        reply_markup=get_caption_mode_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

# File and Metadata Handlers

async def metadata_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /metadata command"""
    await update.message.reply_text(
        "📋 **Metadata Editor**\n\n"
        "Configure metadata fields for your files:\n"
        "• Title\n"
        "• Author\n"
        "• Artist\n"
        "• Subtitle\n"
        "• Audio\n"
        "• Video\n\n"
        "Use the buttons below to edit metadata:",
        reply_markup=get_metadata_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def setmediatype_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /setmediatype command"""
    await update.message.reply_text(
        "📱 **Set Media Type**\n\n"
        "Choose the output media type for your files:",
        reply_markup=get_mediatype_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def getthumb_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /getthumb command"""
    await update.message.reply_text(
        "🖼️ **Thumbnail Extractor**\n\n"
        "Send me a media file and I'll extract its thumbnail for you.\n"
        "Supported formats: Video, Audio, Documents",
        reply_markup=get_back_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

# Dump Management Handlers

async def dumpsettings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /dumpsettings command"""
    user = update.effective_user
    storage = get_user_storage(user.id)
    settings = storage.get_user_settings()
    
    dump_enabled = settings.get('dump_enabled', False)
    dump_channel = settings.get('dump_channel', 'Not set')
    forwarding_mode = settings.get('forwarding_mode', 'Disabled')
    
    dump_text = f"""
📤 **Dump Settings**

**File-dump:** {'Enabled' if dump_enabled else 'Disabled'}
**Dump Channel:** {dump_channel}
**Forwarding Mode:** {forwarding_mode}

Configure how processed files are handled and stored.
"""
    
    await update.message.reply_text(
        dump_text,
        reply_markup=get_dump_settings_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def deldump_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /deldump command"""
    await update.message.reply_text(
        "🗑️ **Delete Dump Files**\n\n"
        "This will permanently delete all dump files and clear dump data.\n"
        "Are you sure you want to proceed?",
        reply_markup=get_delete_dump_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

# Social and Premium Handlers

async def leaderboard_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /leaderboard command"""
    storage = get_user_storage(0)  # Global storage
    leaderboard = storage.get_leaderboard()
    
    if not leaderboard:
        await update.message.reply_text(
            "📊 **Leaderboard**\n\n"
            "No data available yet. Start renaming files to appear on the leaderboard!",
            reply_markup=get_back_keyboard()
        )
        return
    
    leaderboard_text = "🏆 **Top Rename Contributors**\n\n"
    for i, (user_id, username, count) in enumerate(leaderboard[:10], 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        leaderboard_text += f"{medal} {username}: {count} files\n"
    
    await update.message.reply_text(
        leaderboard_text,
        reply_markup=get_leaderboard_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def top_referrals_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /top_referrals command"""
    storage = get_user_storage(0)  # Global storage
    top_referrals = storage.get_top_referrals()
    
    if not top_referrals:
        await update.message.reply_text(
            "🎯 **Top Referrals**\n\n"
            "No referral data available yet. Use /refer to start earning referral rewards!",
            reply_markup=get_back_keyboard()
        )
        return
    
    referrals_text = "🎯 **Top Referral Contributors**\n\n"
    for i, (user_id, username, count) in enumerate(top_referrals[:10], 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        referrals_text += f"{medal} {username}: {count} referrals\n"
    
    await update.message.reply_text(
        referrals_text,
        reply_markup=get_referrals_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def refer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /refer command"""
    user = update.effective_user
    bot_username = context.bot.username
    
    referral_link = f"https://t.me/{bot_username}?start=ref_{user.id}"
    
    refer_text = f"""
🎁 **Refer Friends & Earn Premium**

**Your Referral Link:**
`{referral_link}`

**Rewards:**
• +{REFERRAL_BONUS_HOURS} hours premium access per referral
• +{REFERRAL_POINTS_PER_USER} points per new user
• Exclusive features for top referrers

Share your link with friends to start earning!
"""
    
    await update.message.reply_text(
        refer_text,
        reply_markup=get_refer_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def premium_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /premium command"""
    user = update.effective_user
    storage = get_user_storage(user.id)
    settings = storage.get_user_settings()
    
    is_premium = settings.get('is_premium', False)
    premium_until = settings.get('premium_until', None)
    
    if is_premium and premium_until:
        premium_text = f"""
💎 **Premium Status: Active**

**Valid Until:** {premium_until}

**Your Premium Features:**
✅ Unlimited file renames
✅ Priority processing queue
✅ Custom thumbnail uploads
✅ Advanced analytics
✅ API access
✅ No watermarks
✅ Premium support

Thank you for being a premium member!
"""
    else:
        premium_text = """
💎 **Premium Membership**

**Premium Features:**
• Unlimited file renames
• Priority processing queue
• Custom thumbnail uploads
• Advanced analytics
• API access
• No watermarks
• Premium support

**Get Premium:**
• Monthly: $4.99
• Yearly: $49.99 (Save 17%)
• Lifetime: $99.99

**Free Ways to Get Premium:**
• Refer friends (+3 hours each)
• Top leaderboard positions
• Community contributions
"""
    
    await update.message.reply_text(
        premium_text,
        reply_markup=get_premium_keyboard(is_premium),
        parse_mode=ParseMode.MARKDOWN
    )

async def elites_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /elites command"""
    storage = get_user_storage(0)  # Global storage
    elites = storage.get_premium_users()
    
    if not elites:
        await update.message.reply_text(
            "👑 **Elite Premium Users**\n\n"
            "No premium users yet. Be the first to join the elite club!",
            reply_markup=get_back_keyboard()
        )
        return
    
    elites_text = "👑 **Elite Premium Members**\n\n"
    for i, (user_id, username, tier) in enumerate(elites[:20], 1):
        crown = "👑" if tier == "lifetime" else "💎" if tier == "yearly" else "⭐"
        elites_text += f"{crown} {username} ({tier.title()})\n"
    
    await update.message.reply_text(
        elites_text,
        reply_markup=get_elites_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def features_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /features command"""
    features_text = """
🚀 **Bot Features Overview**

**🔧 Rename System:**
• Auto-rename with custom templates
• Manual rename mode
• Text replacement rules
• Variable support

**🎨 Customization:**
• Banner control panel
• Thumbnail management (Normal/Season/Quality)
• Caption formatting (11 styles)
• Metadata editing

**📁 File Support:**
• Up to 5GB file size
• All media formats
• Document processing
• Thumbnail extraction

**💎 Premium Features:**
• Unlimited processing
• Priority queue
• Advanced analytics
• API access

**🎯 Social Features:**
• Referral system
• Leaderboards
• Premium community
• Elite status

**🛠️ Advanced:**
• Dump management
• Batch processing
• Progress tracking
• Admin controls
"""
    
    await update.message.reply_text(
        features_text,
        reply_markup=get_features_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def about_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /about command"""
    about_text = """
🤖 **About Auto Renamer Bot**

**Version:** 2.0.0
**Developer:** @AutoRenamerBot
**Support:** @AutoRenamerSupport

**Statistics:**
• Files processed: 1M+
• Active users: 50K+
• Premium members: 5K+
• Uptime: 99.9%

**Features:**
• 26+ Commands
• Inline keyboard interface
• 5GB file support
• Advanced templates
• Premium system

**Links:**
• Channel: @AutoRenamerChannel
• Support: @AutoRenamerSupport
• Updates: @AutoRenamerNews

Thank you for using our bot! ❤️
"""
    
    await update.message.reply_text(
        about_text,
        reply_markup=get_about_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

async def admin_cmd_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /admin_cmd command - Admin only"""
    user = update.effective_user
    
    if user.id not in ADMIN_IDS:
        await update.message.reply_text("❌ Access denied. Admin only command.")
        return
    
    await update.message.reply_text(
        "🔐 **Admin Control Panel**\n\n"
        "Welcome to the admin interface.",
        reply_markup=get_admin_keyboard(),
        parse_mode=ParseMode.MARKDOWN
    )

# File Handler

async def file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle file uploads for renaming"""
    user = update.effective_user
    message = update.message
    
    # Check file size
    file_size = 0
    file_obj = None
    
    if message.document:
        file_obj = message.document
        file_size = file_obj.file_size
    elif message.photo:
        file_obj = message.photo[-1]  # Largest photo
        file_size = file_obj.file_size or 0
    elif message.video:
        file_obj = message.video
        file_size = file_obj.file_size
    elif message.audio:
        file_obj = message.audio
        file_size = file_obj.file_size
    
    if not file_obj:
        await message.reply_text(MESSAGES["no_file"])
        return
    
    if file_size > MAX_FILE_SIZE:
        await message.reply_text(MESSAGES["file_too_large"])
        return
    
    # Send processing message
    processing_msg = await message.reply_text(
        MESSAGES["processing"],
        reply_markup=get_processing_keyboard()
    )
    
    try:
        # Initialize file processor
        processor = FileProcessor(user.id)
        
        # Process the file
        result = await processor.process_file(file_obj, message.caption or "")
        
        if result["success"]:
            # Update processing message
            await processing_msg.edit_text(
                MESSAGES["rename_success"],
                reply_markup=get_success_keyboard()
            )
            
            # Send renamed file
            with open(result["output_path"], 'rb') as f:
                await message.reply_document(
                    document=InputFile(f),
                    filename=result["new_name"],
                    caption=f"✅ Renamed: `{result['new_name']}`",
                    parse_mode=ParseMode.MARKDOWN
                )
        else:
            await processing_msg.edit_text(
                MESSAGES["error"].format(error=result["error"]),
                reply_markup=get_error_keyboard()
            )
    
    except Exception as e:
        await processing_msg.edit_text(
            MESSAGES["error"].format(error=str(e)),
            reply_markup=get_error_keyboard()
        )

# Callback Query Handler

async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline keyboard button callbacks"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user = update.effective_user
    storage = get_user_storage(user.id)
    
    if data.startswith("rename_mode_"):
        mode = data.replace("rename_mode_", "")
        storage.set_setting('rename_mode', mode)
        await query.edit_message_text(
            f"✅ Rename mode set to: **{mode.title()}**",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_back_keyboard()
        )
    
    elif data.startswith("caption_mode_"):
        mode = data.replace("caption_mode_", "")
        storage.set_setting('caption_mode', mode)
        await query.edit_message_text(
            f"✅ Caption mode set to: **{mode}**",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_back_keyboard()
        )
    
    elif data.startswith("thumbnail_mode_"):
        mode = data.replace("thumbnail_mode_", "")
        storage.set_setting('thumbnail_mode', mode)
        await query.edit_message_text(
            f"✅ Thumbnail mode set to: **{mode.title()}**",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_back_keyboard()
        )
    
    elif data.startswith("banner_position_"):
        position = data.replace("banner_position_", "")
        storage.set_setting('banner_position', position)
        if position == "DISABLED":
            storage.set_setting('banner_enabled', False)
        else:
            storage.set_setting('banner_enabled', True)
        
        await query.edit_message_text(
            f"✅ Banner position set to: **{position}**",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_banner_keyboard()
        )
    
    elif data == "main_menu":
        await query.edit_message_text(
            MESSAGES["start"],
            reply_markup=get_main_menu_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data == "back":
        await query.edit_message_text(
            "🔙 Returned to main menu",
            reply_markup=get_main_menu_keyboard()
        )
    
    else:
        await query.edit_message_text(
            "⚠️ Feature coming soon!",
            reply_markup=get_back_keyboard()
        )