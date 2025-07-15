import os
import json
from datetime import datetime
from typing import Dict

def ensure_output_dir():
    """Ensure the output directory exists."""
    os.makedirs('outputs', exist_ok=True)

def save_persona_to_file(persona_data: Dict, username: str):
    """Save persona data to a text file with proper formatting."""
    ensure_output_dir()
    
    filename = f"outputs/{username}_persona.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"USER PERSONA: {username}\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        for category, data in persona_data.items():
            f.write(f"{category.upper()}:\n")
            f.write("-" * 40 + "\n")
            
            if isinstance(data, dict) and 'traits' in data:
                # Handle cited format
                f.write(f"{data['traits']}\n\n")
                
                if data['citations']:
                    f.write("Citations:\n")
                    for citation in data['citations']:
                        f.write(f"  - {citation['type']}: {citation['excerpt']}\n")
                        f.write(f"    URL: {citation['url']}\n")
            else:
                # Handle simple format
                f.write(f"{data}\n")
            
            f.write("\n")
    
    return filename

def validate_reddit_url(url: str) -> bool:
    """Validate if the URL is a valid Reddit user profile URL."""
    return 'reddit.com/user/' in url or 'reddit.com/u/' in url