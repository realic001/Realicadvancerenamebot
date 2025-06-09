"""
File processing utilities for the Auto Renamer Bot
Handles file downloads, renaming, and processing with progress tracking
"""

import os
import asyncio
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
from telegram import File

from config import *
from bot.storage import get_user_storage
from utils.template_engine import TemplateEngine

class FileProcessor:
    """Handles file processing operations"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.storage = get_user_storage(user_id)
        self.template_engine = TemplateEngine()
        
    async def process_file(self, file_obj: File, caption: str = "") -> Dict[str, Any]:
        """Process a file for renaming"""
        try:
            # Get user settings
            settings = self.storage.get_user_settings()
            
            # Download file
            file_path = await self._download_file(file_obj)
            if not file_path:
                return {"success": False, "error": "Failed to download file"}
            
            # Generate new filename
            new_name = await self._generate_filename(file_obj, caption, settings)
            
            # Apply text replacements if any
            new_name = self._apply_replacements(new_name, settings.get('replace_rules', {}))
            
            # Rename file
            output_path = await self._rename_file(file_path, new_name)
            
            # Update user statistics
            self.storage.increment_files_processed()
            
            # Clean up original file
            try:
                os.remove(file_path)
            except:
                pass
            
            return {
                "success": True,
                "new_name": new_name,
                "output_path": output_path,
                "original_name": file_obj.file_unique_id
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _download_file(self, file_obj: File) -> Optional[str]:
        """Download file from Telegram"""
        try:
            # Create download path if it doesn't exist
            DOWNLOAD_PATH.mkdir(exist_ok=True)
            
            # Generate unique filename for temporary storage
            temp_name = f"{self.user_id}_{file_obj.file_unique_id}"
            file_path = DOWNLOAD_PATH / temp_name
            
            # Download file (in a real implementation, this would use the Telegram Bot API)
            # For now, we'll simulate the download
            # file_obj.download(file_path)
            
            # Create a dummy file for demonstration
            with open(file_path, 'wb') as f:
                f.write(b"dummy file content")
            
            return str(file_path)
            
        except Exception as e:
            print(f"Download error: {e}")
            return None
    
    async def _generate_filename(self, file_obj: File, caption: str, settings: Dict[str, Any]) -> str:
        """Generate new filename based on user settings"""
        rename_mode = settings.get('rename_mode', 'autorename')
        
        if rename_mode == 'autorename':
            return self._generate_auto_filename(file_obj, settings)
        elif rename_mode == 'manual':
            return self._generate_manual_filename(file_obj, caption)
        else:  # replace mode
            return self._generate_replace_filename(file_obj, settings)
    
    def _generate_auto_filename(self, file_obj: File, settings: Dict[str, Any]) -> str:
        """Generate filename using auto-rename template"""
        template = settings.get('template', '')
        
        if not template:
            # Use original filename if no template
            return getattr(file_obj, 'file_name', f"file_{file_obj.file_unique_id}")
        
        # Extract variables from filename or use defaults
        variables = self._extract_variables_from_file(file_obj)
        
        # Apply template
        new_name = self.template_engine.apply_template(template, variables)
        
        # Ensure file extension
        original_name = getattr(file_obj, 'file_name', '')
        if original_name and '.' in original_name:
            extension = original_name.split('.')[-1]
            if not new_name.endswith(f'.{extension}'):
                new_name += f'.{extension}'
        
        return new_name
    
    def _generate_manual_filename(self, file_obj: File, caption: str) -> str:
        """Generate filename from caption (manual mode)"""
        if caption and caption.strip():
            filename = caption.strip()
            
            # Clean filename
            filename = self._sanitize_filename(filename)
            
            # Add extension from original file
            original_name = getattr(file_obj, 'file_name', '')
            if original_name and '.' in original_name:
                extension = original_name.split('.')[-1]
                if not filename.endswith(f'.{extension}'):
                    filename += f'.{extension}'
            
            return filename
        else:
            # Fallback to original name
            return getattr(file_obj, 'file_name', f"file_{file_obj.file_unique_id}")
    
    def _generate_replace_filename(self, file_obj: File, settings: Dict[str, Any]) -> str:
        """Generate filename using text replacement"""
        original_name = getattr(file_obj, 'file_name', f"file_{file_obj.file_unique_id}")
        replace_rules = settings.get('replace_rules', {})
        
        new_name = original_name
        for old_text, new_text in replace_rules.items():
            new_name = new_name.replace(old_text, new_text)
        
        return new_name
    
    def _extract_variables_from_file(self, file_obj: File) -> Dict[str, str]:
        """Extract template variables from file information"""
        filename = getattr(file_obj, 'file_name', '')
        
        # Default variables
        variables = {
            'title': 'Unknown',
            'season': '01',
            'episode': '01',
            'audio': 'AAC',
            'quality': '1080p',
            'volume': '',
            'chapter': '01',
            'year': '2024',
            'resolution': '1920x1080',
            'codec': 'H264'
        }
        
        if filename:
            # Try to extract information from filename
            filename_lower = filename.lower()
            
            # Extract quality
            for quality in ['2160p', '1440p', '1080p', '720p', '480p', '360p', '240p', '144p']:
                if quality in filename_lower:
                    variables['quality'] = quality
                    break
            
            # Extract season/episode patterns
            import re
            
            # Pattern: S01E01, s01e01, etc.
            se_pattern = r's(\d+)e(\d+)'
            match = re.search(se_pattern, filename_lower)
            if match:
                variables['season'] = match.group(1).zfill(2)
                variables['episode'] = match.group(2).zfill(2)
            
            # Extract title (remove extensions and common patterns)
            title = filename
            for ext in ['.mkv', '.mp4', '.avi', '.mov', '.wmv', '.flv']:
                title = title.replace(ext, '').replace(ext.upper(), '')
            
            # Clean title
            title = re.sub(r'\[.*?\]', '', title)  # Remove brackets
            title = re.sub(r'\(.*?\)', '', title)  # Remove parentheses
            title = title.strip()
            
            if title:
                variables['title'] = title
        
        return variables
    
    def _apply_replacements(self, filename: str, replace_rules: Dict[str, str]) -> str:
        """Apply text replacement rules"""
        for old_text, new_text in replace_rules.items():
            filename = filename.replace(old_text, new_text)
        return filename
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename by removing invalid characters"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Remove multiple underscores
        while '__' in filename:
            filename = filename.replace('__', '_')
        
        # Trim and limit length
        filename = filename.strip('_').strip()
        if len(filename) > 200:
            filename = filename[:200]
        
        return filename or "renamed_file"
    
    async def _rename_file(self, original_path: str, new_name: str) -> str:
        """Rename file and return new path"""
        original_path_obj = Path(original_path)
        new_path = original_path_obj.parent / new_name
        
        # Ensure unique filename
        counter = 1
        while new_path.exists():
            name_parts = new_name.rsplit('.', 1)
            if len(name_parts) == 2:
                new_name_with_counter = f"{name_parts[0]}_{counter}.{name_parts[1]}"
            else:
                new_name_with_counter = f"{new_name}_{counter}"
            
            new_path = original_path_obj.parent / new_name_with_counter
            counter += 1
        
        # Rename file
        shutil.move(original_path, new_path)
        
        return str(new_path)
    
    async def extract_thumbnail(self, file_obj: File) -> Optional[str]:
        """Extract thumbnail from media file"""
        try:
            # This would use ffmpeg or similar tools in a real implementation
            # For now, return a placeholder
            return None
        except Exception as e:
            print(f"Thumbnail extraction error: {e}")
            return None