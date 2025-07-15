"""
Configuration settings for Reddit Persona Generator
"""

# Reddit API settings
REDDIT_BASE_URL = "https://www.reddit.com"
REQUEST_TIMEOUT = 30
RATE_LIMIT_DELAY = 1  # seconds between requests

# User agent for requests
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Scraping limits
MAX_PAGES = 3
ITEMS_PER_PAGE = 100

# Persona generation settings
MAX_INTERESTS = 5
MAX_PERSONALITY_TRAITS = 3
MAX_GOALS = 5
MAX_FRUSTRATIONS = 5
MAX_CITATIONS_PER_ITEM = 3