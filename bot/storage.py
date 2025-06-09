"""
User data storage and management for the Telegram Auto Renamer Bot
Handles user settings, preferences, and statistics
"""

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

from config import DATABASE_URL

class UserStorage:
    """Individual user storage manager"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.db_path = "bot_data.db"
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                settings TEXT,
                is_premium BOOLEAN DEFAULT 0,
                premium_until TIMESTAMP,
                files_processed INTEGER DEFAULT 0,
                referrals INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Settings table for detailed configuration
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_settings (
                user_id INTEGER PRIMARY KEY,
                rename_mode TEXT DEFAULT 'autorename',
                template TEXT DEFAULT '',
                thumbnail_mode TEXT DEFAULT 'normal',
                caption_mode TEXT DEFAULT 'Normal',
                banner_enabled BOOLEAN DEFAULT 0,
                banner_image TEXT DEFAULT '',
                banner_position TEXT DEFAULT 'START',
                banner_link TEXT DEFAULT '',
                dump_enabled BOOLEAN DEFAULT 0,
                dump_channel TEXT DEFAULT '',
                forwarding_mode TEXT DEFAULT 'disabled',
                replace_rules TEXT DEFAULT '{}',
                metadata TEXT DEFAULT '{}',
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)
        
        # Analytics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_analytics (
                user_id INTEGER PRIMARY KEY,
                total_files INTEGER DEFAULT 0,
                files_today INTEGER DEFAULT 0,
                last_file_date DATE,
                favorite_format TEXT DEFAULT '',
                processing_time REAL DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)
        
        # Referrals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS referrals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                referrer_id INTEGER,
                referred_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (referrer_id) REFERENCES users (user_id),
                FOREIGN KEY (referred_id) REFERENCES users (user_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def initialize_user(self, user_id: int, first_name: str, username: str = ""):
        """Initialize a new user in the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Insert user
            cursor.execute("""
                INSERT OR IGNORE INTO users (user_id, username, first_name)
                VALUES (?, ?, ?)
            """, (user_id, username, first_name))
            
            # Insert default settings
            cursor.execute("""
                INSERT OR IGNORE INTO user_settings (user_id)
                VALUES (?)
            """, (user_id,))
            
            # Insert default analytics
            cursor.execute("""
                INSERT OR IGNORE INTO user_analytics (user_id)
                VALUES (?)
            """, (user_id,))
            
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()
    
    def get_user_settings(self) -> Dict[str, Any]:
        """Get user settings and preferences"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT us.*, u.is_premium, u.premium_until, u.files_processed
                FROM user_settings us
                LEFT JOIN users u ON us.user_id = u.user_id
                WHERE us.user_id = ?
            """, (self.user_id,))
            
            row = cursor.fetchone()
            if not row:
                return {}
            
            # Convert row to dictionary
            columns = [desc[0] for desc in cursor.description]
            settings = dict(zip(columns, row))
            
            # Parse JSON fields
            settings['replace_rules'] = json.loads(settings.get('replace_rules', '{}'))
            settings['metadata'] = json.loads(settings.get('metadata', '{}'))
            
            return settings
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return {}
        finally:
            conn.close()
    
    def set_setting(self, key: str, value: Any):
        """Set a specific user setting"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Handle JSON fields
            if key in ['replace_rules', 'metadata']:
                value = json.dumps(value)
            
            cursor.execute(f"""
                UPDATE user_settings
                SET {key} = ?
                WHERE user_id = ?
            """, (value, self.user_id))
            
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()
    
    def set_replace_rule(self, old_text: str, new_text: str):
        """Set a text replacement rule"""
        settings = self.get_user_settings()
        replace_rules = settings.get('replace_rules', {})
        replace_rules[old_text] = new_text
        self.set_setting('replace_rules', replace_rules)
    
    def increment_files_processed(self):
        """Increment the user's file processing counter"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Update user stats
            cursor.execute("""
                UPDATE users
                SET files_processed = files_processed + 1,
                    last_active = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """, (self.user_id,))
            
            # Update analytics
            today = datetime.now().date()
            cursor.execute("""
                UPDATE user_analytics
                SET total_files = total_files + 1,
                    files_today = CASE 
                        WHEN last_file_date = ? THEN files_today + 1
                        ELSE 1
                    END,
                    last_file_date = ?
                WHERE user_id = ?
            """, (today, today, self.user_id))
            
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()
    
    def add_premium_time(self, hours: int):
        """Add premium time to user account"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get current premium status
            cursor.execute("""
                SELECT premium_until FROM users WHERE user_id = ?
            """, (self.user_id,))
            
            row = cursor.fetchone()
            current_premium = row[0] if row and row[0] else datetime.now()
            
            # Add hours to premium time
            if isinstance(current_premium, str):
                current_premium = datetime.fromisoformat(current_premium)
            
            new_premium_until = current_premium + timedelta(hours=hours)
            
            cursor.execute("""
                UPDATE users
                SET is_premium = 1,
                    premium_until = ?
                WHERE user_id = ?
            """, (new_premium_until, self.user_id))
            
            conn.commit()
            return new_premium_until
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            conn.close()

class GlobalStorage:
    """Global storage for leaderboards and statistics"""
    
    def __init__(self):
        self.db_path = "bot_data.db"
    
    def get_leaderboard(self, limit: int = 10) -> List[Tuple[int, str, int]]:
        """Get top users by files processed"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT user_id, COALESCE(first_name, username, 'User'), files_processed
                FROM users
                WHERE files_processed > 0
                ORDER BY files_processed DESC
                LIMIT ?
            """, (limit,))
            
            return cursor.fetchall()
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            conn.close()
    
    def get_top_referrals(self, limit: int = 10) -> List[Tuple[int, str, int]]:
        """Get top users by referrals"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT u.user_id, COALESCE(u.first_name, u.username, 'User'), u.referrals
                FROM users u
                WHERE u.referrals > 0
                ORDER BY u.referrals DESC
                LIMIT ?
            """, (limit,))
            
            return cursor.fetchall()
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            conn.close()
    
    def get_premium_users(self, limit: int = 20) -> List[Tuple[int, str, str]]:
        """Get premium users list"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT user_id, COALESCE(first_name, username, 'User'),
                       CASE 
                           WHEN premium_until > datetime('now', '+365 days') THEN 'lifetime'
                           WHEN premium_until > datetime('now', '+30 days') THEN 'yearly'
                           ELSE 'monthly'
                       END as tier
                FROM users
                WHERE is_premium = 1 AND premium_until > datetime('now')
                ORDER BY premium_until DESC
                LIMIT ?
            """, (limit,))
            
            return cursor.fetchall()
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            conn.close()
    
    def add_referral(self, referrer_id: int, referred_id: int):
        """Add a referral relationship"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Check if referral already exists
            cursor.execute("""
                SELECT id FROM referrals 
                WHERE referrer_id = ? AND referred_id = ?
            """, (referrer_id, referred_id))
            
            if cursor.fetchone():
                return False  # Referral already exists
            
            # Add referral
            cursor.execute("""
                INSERT INTO referrals (referrer_id, referred_id)
                VALUES (?, ?)
            """, (referrer_id, referred_id))
            
            # Update referrer's count
            cursor.execute("""
                UPDATE users
                SET referrals = referrals + 1
                WHERE user_id = ?
            """, (referrer_id,))
            
            conn.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
        finally:
            conn.close()
    
    def get_total_stats(self) -> Dict[str, int]:
        """Get global bot statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_users,
                    SUM(files_processed) as total_files,
                    COUNT(CASE WHEN is_premium = 1 THEN 1 END) as premium_users,
                    SUM(referrals) as total_referrals
                FROM users
            """)
            
            row = cursor.fetchone()
            if row:
                return {
                    'total_users': row[0] or 0,
                    'total_files': row[1] or 0,
                    'premium_users': row[2] or 0,
                    'total_referrals': row[3] or 0
                }
            
            return {'total_users': 0, 'total_files': 0, 'premium_users': 0, 'total_referrals': 0}
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return {'total_users': 0, 'total_files': 0, 'premium_users': 0, 'total_referrals': 0}
        finally:
            conn.close()

# Storage instances
_user_storages: Dict[int, UserStorage] = {}
_global_storage = GlobalStorage()

def get_user_storage(user_id: int) -> UserStorage:
    """Get or create user storage instance"""
    if user_id == 0:  # Special case for global storage
        return _global_storage
    
    if user_id not in _user_storages:
        _user_storages[user_id] = UserStorage(user_id)
    
    return _user_storages[user_id]