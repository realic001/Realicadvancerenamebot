"""
Template engine for auto-renaming files
Handles variable substitution and template processing
"""

import re
from typing import Dict, List, Any

class TemplateEngine:
    """Template processing engine for file renaming"""
    
    def __init__(self):
        self.variable_pattern = re.compile(r'\{([^}]+)\}')
    
    def apply_template(self, template: str, variables: Dict[str, str]) -> str:
        """Apply variables to template string"""
        if not template:
            return "renamed_file"
        
        result = template
        
        # Replace all variables in the template
        for var_name, var_value in variables.items():
            placeholder = f"{{{var_name}}}"
            result = result.replace(placeholder, str(var_value))
        
        # Clean up any remaining unreplaced variables
        result = self.variable_pattern.sub('', result)
        
        # Clean up the result
        result = self._clean_filename(result)
        
        return result or "renamed_file"
    
    def extract_variables(self, template: str) -> List[str]:
        """Extract variable names from template"""
        matches = self.variable_pattern.findall(template)
        return list(set(matches))
    
    def validate_template(self, template: str) -> Dict[str, Any]:
        """Validate template syntax"""
        if not template:
            return {"valid": False, "error": "Empty template"}
        
        # Check for balanced braces
        open_braces = template.count('{')
        close_braces = template.count('}')
        
        if open_braces != close_braces:
            return {"valid": False, "error": "Unbalanced braces"}
        
        # Extract variables
        variables = self.extract_variables(template)
        
        # Check for invalid characters in variable names
        for var in variables:
            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', var):
                return {"valid": False, "error": f"Invalid variable name: {var}"}
        
        return {"valid": True, "variables": variables}
    
    def _clean_filename(self, filename: str) -> str:
        """Clean and sanitize filename"""
        # Remove multiple spaces
        filename = re.sub(r'\s+', ' ', filename)
        
        # Remove leading/trailing spaces and dashes
        filename = filename.strip(' -_')
        
        # Replace invalid filename characters (but preserve hyphens for normal use)
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Remove multiple underscores but keep single ones and hyphens
        filename = re.sub(r'_{2,}', '_', filename)
        
        # Limit length
        if len(filename) > 200:
            filename = filename[:200]
        
        return filename
    
    def get_sample_preview(self, template: str) -> str:
        """Generate sample preview of template"""
        sample_vars = {
            'title': 'Sample Movie',
            'season': '01',
            'episode': '05',
            'audio': 'AAC',
            'quality': '1080p',
            'volume': 'Vol1',
            'chapter': '01',
            'year': '2024',
            'resolution': '1920x1080',
            'codec': 'H264'
        }
        
        return self.apply_template(template, sample_vars)