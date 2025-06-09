"""
Inline keyboard layouts for the Telegram Auto Renamer Bot
All interactive button menus and shortcuts
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import CAPTION_MODES, BANNER_POSITIONS

def get_main_menu_keyboard():
    """Main menu with primary bot functions"""
    keyboard = [
        [
            InlineKeyboardButton("✏️ Rename Settings", callback_data="rename_settings"),
            InlineKeyboardButton("🎨 Customization", callback_data="customization")
        ],
        [
            InlineKeyboardButton("📁 File Management", callback_data="file_management"),
            InlineKeyboardButton("📊 Analytics", callback_data="analytics")
        ],
        [
            InlineKeyboardButton("💎 Premium", callback_data="premium_menu"),
            InlineKeyboardButton("🎯 Social", callback_data="social_menu")
        ],
        [
            InlineKeyboardButton("⚙️ Settings", callback_data="settings"),
            InlineKeyboardButton("❓ Help", callback_data="help")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_rename_settings_keyboard():
    """Rename system controls"""
    keyboard = [
        [
            InlineKeyboardButton("🔧 Auto-Rename", callback_data="autorename"),
            InlineKeyboardButton("🔍 Preview", callback_data="preview")
        ],
        [
            InlineKeyboardButton("📝 Mode", callback_data="mode"),
            InlineKeyboardButton("🔄 Replace", callback_data="replace")
        ],
        [
            InlineKeyboardButton("📂 Source", callback_data="renamesource"),
            InlineKeyboardButton("📋 Metadata", callback_data="metadata")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_customization_keyboard():
    """Customization options"""
    keyboard = [
        [
            InlineKeyboardButton("🎨 Banner Control", callback_data="banner"),
            InlineKeyboardButton("📷 Thumbnails", callback_data="thumbnails")
        ],
        [
            InlineKeyboardButton("💬 Caption Mode", callback_data="caption_mode"),
            InlineKeyboardButton("📱 Media Type", callback_data="setmediatype")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_mode_keyboard():
    """Rename mode selection"""
    keyboard = [
        [InlineKeyboardButton("🤖 Autorename", callback_data="rename_mode_autorename")],
        [InlineKeyboardButton("✏️ Manual", callback_data="rename_mode_manual")],
        [InlineKeyboardButton("🔄 Replace", callback_data="rename_mode_replace")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_caption_mode_keyboard():
    """Caption formatting options - 11 styles"""
    keyboard = []
    
    # Create rows of 2 buttons each
    for i in range(0, len(CAPTION_MODES), 2):
        row = []
        for j in range(i, min(i + 2, len(CAPTION_MODES))):
            mode = CAPTION_MODES[j]
            row.append(InlineKeyboardButton(mode, callback_data=f"caption_mode_{mode.lower().replace(' ', '_')}"))
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

def get_banner_keyboard():
    """Banner control panel with position options"""
    keyboard = [
        [InlineKeyboardButton("📊 STATUS", callback_data="banner_status")],
        [InlineKeyboardButton("🖼️ IMAGE", callback_data="banner_image")],
        [InlineKeyboardButton("📍 POSITION", callback_data="banner_position_menu")],
        [InlineKeyboardButton("🔗 LINK", callback_data="banner_link")],
        [
            InlineKeyboardButton("▶️ START", callback_data="banner_position_START"),
            InlineKeyboardButton("⏹️ END", callback_data="banner_position_END")
        ],
        [
            InlineKeyboardButton("🔄 BOTH", callback_data="banner_position_BOTH"),
            InlineKeyboardButton("❌ DISABLED", callback_data="banner_position_DISABLED")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_thumbnail_mode_keyboard():
    """Thumbnail management options"""
    keyboard = [
        [InlineKeyboardButton("📷 Normal", callback_data="thumbnail_mode_normal")],
        [InlineKeyboardButton("📺 Season (s01-s10)", callback_data="thumbnail_mode_season")],
        [InlineKeyboardButton("🎬 Quality (144p-8000p)", callback_data="thumbnail_mode_quality")],
        [InlineKeyboardButton("📋 View All", callback_data="allthumb")],
        [InlineKeyboardButton("🗑️ Delete Default", callback_data="del_thumb")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_thumbnail_season_keyboard():
    """Season-specific thumbnail management (s01-s10)"""
    keyboard = []
    
    # Create season buttons in rows of 5
    for i in range(0, 10, 5):
        row = []
        for j in range(i, min(i + 5, 10)):
            season_num = f"{j+1:02d}"
            row.append(InlineKeyboardButton(f"S{season_num}", callback_data=f"thums{season_num}"))
        keyboard.append(row)
    
    # Delete season buttons
    keyboard.append([InlineKeyboardButton("🗑️ Delete Season", callback_data="delete_season_menu")])
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="thumbnails")])
    return InlineKeyboardMarkup(keyboard)

def get_thumbnail_quality_keyboard():
    """Quality-specific thumbnail management"""
    keyboard = [
        [
            InlineKeyboardButton("144p", callback_data="thum144"),
            InlineKeyboardButton("240p", callback_data="thum240"),
            InlineKeyboardButton("360p", callback_data="thum360")
        ],
        [
            InlineKeyboardButton("480p", callback_data="thum480"),
            InlineKeyboardButton("720p", callback_data="thum720"),
            InlineKeyboardButton("1080p", callback_data="thum1080")
        ],
        [
            InlineKeyboardButton("1440p", callback_data="thum1440"),
            InlineKeyboardButton("2160p", callback_data="thum2160"),
            InlineKeyboardButton("4000p", callback_data="thum4000")
        ],
        [InlineKeyboardButton("8000p", callback_data="thum8000")],
        [InlineKeyboardButton("🗑️ Delete Quality", callback_data="delete_quality_menu")],
        [InlineKeyboardButton("🔙 Back", callback_data="thumbnails")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_premium_keyboard(is_premium=False):
    """Premium features and subscription"""
    if is_premium:
        keyboard = [
            [InlineKeyboardButton("👑 Premium Status", callback_data="premium_status")],
            [InlineKeyboardButton("📊 Analytics", callback_data="premium_analytics")],
            [InlineKeyboardButton("🔧 API Access", callback_data="premium_api")],
            [InlineKeyboardButton("🎯 Elite Features", callback_data="premium_elite")],
            [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("💎 Get Premium", callback_data="get_premium")],
            [InlineKeyboardButton("🎁 Free Premium", callback_data="free_premium")],
            [InlineKeyboardButton("👑 Elite Users", callback_data="elites")],
            [InlineKeyboardButton("💰 Pricing", callback_data="premium_pricing")],
            [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
        ]
    return InlineKeyboardMarkup(keyboard)

def get_social_keyboard():
    """Social features menu"""
    keyboard = [
        [
            InlineKeyboardButton("🎯 Refer Friends", callback_data="refer"),
            InlineKeyboardButton("🏆 Leaderboard", callback_data="leaderboard")
        ],
        [
            InlineKeyboardButton("🔝 Top Referrals", callback_data="top_referrals"),
            InlineKeyboardButton("👑 Elite Users", callback_data="elites")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_file_management_keyboard():
    """File processing and dump management"""
    keyboard = [
        [
            InlineKeyboardButton("📋 Metadata", callback_data="metadata"),
            InlineKeyboardButton("🖼️ Get Thumbnail", callback_data="getthumb")
        ],
        [
            InlineKeyboardButton("📤 Dump Settings", callback_data="dumpsettings"),
            InlineKeyboardButton("🗑️ Delete Dump", callback_data="deldump")
        ],
        [
            InlineKeyboardButton("📱 Media Type", callback_data="setmediatype"),
            InlineKeyboardButton("🔄 Batch Process", callback_data="batch_process")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_metadata_keyboard():
    """Metadata editing options"""
    keyboard = [
        [
            InlineKeyboardButton("📝 Title", callback_data="meta_title"),
            InlineKeyboardButton("👤 Author", callback_data="meta_author")
        ],
        [
            InlineKeyboardButton("🎵 Artist", callback_data="meta_artist"),
            InlineKeyboardButton("💬 Subtitle", callback_data="meta_subtitle")
        ],
        [
            InlineKeyboardButton("🔊 Audio", callback_data="meta_audio"),
            InlineKeyboardButton("🎬 Video", callback_data="meta_video")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="file_management")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_dump_settings_keyboard():
    """Dump configuration options"""
    keyboard = [
        [
            InlineKeyboardButton("✅ Enable Dump", callback_data="dump_enable"),
            InlineKeyboardButton("❌ Disable Dump", callback_data="dump_disable")
        ],
        [
            InlineKeyboardButton("📢 Set Channel", callback_data="dump_channel"),
            InlineKeyboardButton("🔄 Forwarding", callback_data="dump_forwarding")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="file_management")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_delete_dump_keyboard():
    """Confirm dump deletion"""
    keyboard = [
        [
            InlineKeyboardButton("✅ Yes, Delete", callback_data="confirm_delete_dump"),
            InlineKeyboardButton("❌ Cancel", callback_data="file_management")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_mediatype_keyboard():
    """Media type selection"""
    keyboard = [
        [
            InlineKeyboardButton("📄 Document", callback_data="mediatype_document"),
            InlineKeyboardButton("🎬 Video", callback_data="mediatype_video")
        ],
        [
            InlineKeyboardButton("🎵 Audio", callback_data="mediatype_audio"),
            InlineKeyboardButton("🖼️ Photo", callback_data="mediatype_photo")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="file_management")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_autorename_keyboard():
    """Auto-rename template setup"""
    keyboard = [
        [
            InlineKeyboardButton("📝 Set Template", callback_data="set_template"),
            InlineKeyboardButton("🔍 Preview", callback_data="preview_template")
        ],
        [
            InlineKeyboardButton("📋 Variables", callback_data="template_variables"),
            InlineKeyboardButton("💡 Examples", callback_data="template_examples")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="rename_settings")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_admin_keyboard():
    """Admin control panel"""
    keyboard = [
        [
            InlineKeyboardButton("👥 Users", callback_data="admin_users"),
            InlineKeyboardButton("📊 Stats", callback_data="admin_stats")
        ],
        [
            InlineKeyboardButton("💎 Premium", callback_data="admin_premium"),
            InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")
        ],
        [
            InlineKeyboardButton("🔧 Settings", callback_data="admin_settings"),
            InlineKeyboardButton("📝 Logs", callback_data="admin_logs")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_processing_keyboard():
    """Processing file progress"""
    keyboard = [
        [InlineKeyboardButton("⏹️ Cancel", callback_data="cancel_processing")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_success_keyboard():
    """File processing success"""
    keyboard = [
        [
            InlineKeyboardButton("🔄 Process Another", callback_data="main_menu"),
            InlineKeyboardButton("⚙️ Settings", callback_data="settings")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_error_keyboard():
    """Error handling options"""
    keyboard = [
        [
            InlineKeyboardButton("🔄 Try Again", callback_data="main_menu"),
            InlineKeyboardButton("💬 Support", callback_data="support")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_settings_keyboard():
    """User settings panel"""
    keyboard = [
        [
            InlineKeyboardButton("✏️ Rename", callback_data="rename_settings"),
            InlineKeyboardButton("🎨 Style", callback_data="customization")
        ],
        [
            InlineKeyboardButton("📷 Thumbnails", callback_data="thumbnails"),
            InlineKeyboardButton("🎨 Banner", callback_data="banner")
        ],
        [
            InlineKeyboardButton("💎 Premium", callback_data="premium_menu"),
            InlineKeyboardButton("📊 Analytics", callback_data="user_analytics")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_help_keyboard():
    """Help and support options"""
    keyboard = [
        [
            InlineKeyboardButton("📚 Commands", callback_data="help_commands"),
            InlineKeyboardButton("🚀 Features", callback_data="features")
        ],
        [
            InlineKeyboardButton("💡 Examples", callback_data="help_examples"),
            InlineKeyboardButton("❓ FAQ", callback_data="help_faq")
        ],
        [
            InlineKeyboardButton("💬 Support", callback_data="support"),
            InlineKeyboardButton("ℹ️ About", callback_data="about")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_leaderboard_keyboard():
    """Leaderboard display options"""
    keyboard = [
        [
            InlineKeyboardButton("🔄 Refresh", callback_data="leaderboard"),
            InlineKeyboardButton("🎯 Referrals", callback_data="top_referrals")
        ],
        [
            InlineKeyboardButton("👑 Elite", callback_data="elites"),
            InlineKeyboardButton("📊 My Stats", callback_data="my_stats")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="social_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_refer_keyboard():
    """Referral system options"""
    keyboard = [
        [
            InlineKeyboardButton("📋 Copy Link", callback_data="copy_referral"),
            InlineKeyboardButton("📤 Share", callback_data="share_referral")
        ],
        [
            InlineKeyboardButton("📊 My Referrals", callback_data="my_referrals"),
            InlineKeyboardButton("🎁 Rewards", callback_data="referral_rewards")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="social_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_elites_keyboard():
    """Elite users display"""
    keyboard = [
        [
            InlineKeyboardButton("🔄 Refresh", callback_data="elites"),
            InlineKeyboardButton("💎 Get Premium", callback_data="get_premium")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="social_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_features_keyboard():
    """Features overview"""
    keyboard = [
        [
            InlineKeyboardButton("📝 Rename", callback_data="feature_rename"),
            InlineKeyboardButton("🎨 Custom", callback_data="feature_custom")
        ],
        [
            InlineKeyboardButton("💎 Premium", callback_data="feature_premium"),
            InlineKeyboardButton("🎯 Social", callback_data="feature_social")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="help")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_about_keyboard():
    """About bot information"""
    keyboard = [
        [
            InlineKeyboardButton("📢 Channel", callback_data="bot_channel"),
            InlineKeyboardButton("💬 Support", callback_data="bot_support")
        ],
        [
            InlineKeyboardButton("📰 Updates", callback_data="bot_updates"),
            InlineKeyboardButton("⭐ Rate Bot", callback_data="rate_bot")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="help")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_referrals_keyboard():
    """Top referrals display"""
    keyboard = [
        [
            InlineKeyboardButton("🔄 Refresh", callback_data="top_referrals"),
            InlineKeyboardButton("🎯 My Referrals", callback_data="my_referrals")
        ],
        [
            InlineKeyboardButton("🎁 Refer Now", callback_data="refer"),
            InlineKeyboardButton("🏆 Leaderboard", callback_data="leaderboard")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="social_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_replace_keyboard():
    """Text replacement setup"""
    keyboard = [
        [
            InlineKeyboardButton("📝 Set Rule", callback_data="set_replace_rule"),
            InlineKeyboardButton("👁️ View Rules", callback_data="view_replace_rules")
        ],
        [
            InlineKeyboardButton("🗑️ Clear Rules", callback_data="clear_replace_rules"),
            InlineKeyboardButton("💡 Examples", callback_data="replace_examples")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="rename_settings")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_preview_keyboard():
    """Template preview options"""
    keyboard = [
        [
            InlineKeyboardButton("✏️ Edit Template", callback_data="edit_template"),
            InlineKeyboardButton("🔄 Generate New", callback_data="generate_preview")
        ],
        [InlineKeyboardButton("🔙 Back", callback_data="rename_settings")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_keyboard():
    """Simple back button"""
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="main_menu")]]
    return InlineKeyboardMarkup(keyboard)