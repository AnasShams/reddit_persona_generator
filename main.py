#!/usr/bin/env python3
"""
Reddit User Persona Generator
Main script to generate user personas from Reddit profiles
"""

import sys
import os
import json
import time
from datetime import datetime
from reddit_scraper import RedditScraper
from persona_generator import PersonaGenerator

def main():
    """Main function to orchestrate the persona generation process"""
    
    if len(sys.argv) != 2:
        print("Usage: python main.py <reddit_profile_url>")
        print("Example: python main.py https://www.reddit.com/user/kojied/")
        sys.exit(1)
    
    profile_url = sys.argv[1]
    
    # Validate URL format
    if not profile_url.startswith("https://www.reddit.com/user/"):
        print("Error: Please provide a valid Reddit user profile URL")
        print("Format: https://www.reddit.com/user/username/")
        sys.exit(1)
    
    # Extract username from URL
    username = profile_url.split("/user/")[1].rstrip("/")
    
    print(f"🚀 Starting persona generation for user: {username}")
    print("=" * 50)
    
    try:
        # Initialize scraper
        scraper = RedditScraper()
        
        # Scrape user data
        print("📊 Scraping Reddit data...")
        user_data = scraper.scrape_user_profile(username)
        
        if not user_data:
            print("❌ Failed to scrape user data. User might not exist or profile is private.")
            sys.exit(1)
        
        print(f"✅ Successfully scraped {len(user_data['comments'])} comments and {len(user_data['posts'])} posts")
        
        # Generate persona
        print("🧠 Generating user persona...")
        persona_generator = PersonaGenerator()
        persona = persona_generator.generate_persona(user_data)
        
        # Create sample_outputs directory if it doesn't exist
        output_dir = "sample_outputs"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Save to file in sample_outputs folder
        output_filename = os.path.join(output_dir, f"{username}_persona.txt")
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(persona)
        
        print(f"✅ Persona generated successfully!")
        print(f"📄 Output saved to: {output_filename}")
        
        # Also save raw data for reference in sample_outputs folder
        data_filename = os.path.join(output_dir, f"{username}_raw_data.json")
        with open(data_filename, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Raw data saved to: {data_filename}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()