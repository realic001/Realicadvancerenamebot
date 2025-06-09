"""
Banner management utilities for PDF and document processing
Handles banner embedding with position control (START/END/BOTH/DISABLED)
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from PIL import Image, ImageDraw, ImageFont
import io

class BannerManager:
    """Manages banner creation and embedding for documents"""
    
    def __init__(self):
        self.banner_cache = {}
    
    def create_banner(self, text: str, link: str = "", width: int = 800, height: int = 100) -> bytes:
        """Create a banner image with text and optional link"""
        try:
            # Create image with white background
            img = Image.new('RGB', (width, height), 'white')
            draw = ImageDraw.Draw(img)
            
            # Try to use a decent font, fallback to default
            try:
                font = ImageFont.truetype("arial.ttf", 24)
                small_font = ImageFont.truetype("arial.ttf", 16)
            except:
                font = ImageFont.load_default()
                small_font = ImageFont.load_default()
            
            # Draw main text
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            text_x = (width - text_width) // 2
            text_y = (height - text_height) // 2 - 10
            
            draw.text((text_x, text_y), text, fill='black', font=font)
            
            # Draw link if provided
            if link:
                link_text = f"🔗 {link}"
                link_bbox = draw.textbbox((0, 0), link_text, font=small_font)
                link_width = link_bbox[2] - link_bbox[0]
                link_x = (width - link_width) // 2
                link_y = text_y + text_height + 5
                
                draw.text((link_x, link_y), link_text, fill='blue', font=small_font)
            
            # Convert to bytes
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            return buffer.getvalue()
            
        except Exception as e:
            print(f"Banner creation error: {e}")
            return b""
    
    def embed_banner_in_pdf(self, pdf_path: str, banner_data: bytes, position: str, link: str = "") -> str:
        """Embed banner in PDF file at specified position"""
        try:
            # This would use a PDF library like PyPDF2 or reportlab in a real implementation
            # For now, we'll simulate the process
            
            output_path = pdf_path.replace('.pdf', '_with_banner.pdf')
            
            # Simulate banner embedding
            with open(pdf_path, 'rb') as src:
                content = src.read()
            
            # Write modified content (in reality, this would properly embed the banner)
            with open(output_path, 'wb') as dst:
                dst.write(content)
            
            return output_path
            
        except Exception as e:
            print(f"PDF banner embedding error: {e}")
            return pdf_path
    
    def get_banner_positions(self) -> Dict[str, str]:
        """Get available banner positions"""
        return {
            'START': 'Add banner at the beginning of the document',
            'END': 'Add banner at the end of the document', 
            'BOTH': 'Add banner at both start and end',
            'DISABLED': 'No banner'
        }
    
    def validate_banner_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Validate banner configuration"""
        errors = []
        
        if settings.get('banner_enabled'):
            if not settings.get('banner_image'):
                errors.append("Banner image is required when banner is enabled")
            
            position = settings.get('banner_position', 'START')
            if position not in ['START', 'END', 'BOTH', 'DISABLED']:
                errors.append("Invalid banner position")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }