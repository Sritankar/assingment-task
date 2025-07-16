
"""
Reddit User Persona Generator
Scrapes Reddit user data and generates a detailed persona using LLM analysis.
"""

import sys
import argparse
from src.reddit_scraper import RedditScraper
from src.persona_generator import PersonaGenerator
from src.utils import save_persona_to_file, validate_reddit_url

def main():
    parser = argparse.ArgumentParser(description='Generate user personas from Reddit profiles')
    parser.add_argument('profile_url', help='Reddit user profile URL')
    parser.add_argument('--output', '-o', help='Output filename (optional)')
    
    args = parser.parse_args()
    
    # Validate URL
    if not validate_reddit_url(args.profile_url):
        print("Error: Invalid Reddit profile URL")
        print("Expected format: https://www.reddit.com/user/kojied/")
        sys.exit(1)
    
    try:
        # Initialize components
        scraper = RedditScraper()
        generator = PersonaGenerator()
        
        # Extract username and scrape data
        print("Extracting username from URL...")
        username = scraper.extract_username(args.profile_url)
        
        print(f"Scraping data for user: {username}...")
        user_data = scraper.scrape_user_content(username)
        
        print(f"Found {len(user_data['posts'])} posts and {len(user_data['comments'])} comments")
        
        # Generate persona
        print("Generating user persona...")
        persona = generator.generate_persona(user_data)
        
        # Save to file
        print("Saving persona to file...")
        output_file = save_persona_to_file(persona, username)
        
        print(f"\nSuccess! User persona saved to: {output_file}")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
