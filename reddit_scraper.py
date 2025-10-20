"""
Reddit Scraper Module
Uses Reddit's free JSON API to scrape user data
"""

import requests
import time
import json
from datetime import datetime
from typing import Dict, List, Optional

class RedditScraper:
    """Scrapes Reddit user profiles using the free Reddit JSON API"""
    
    def __init__(self):
        self.base_url = "https://www.reddit.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_user_profile(self, username: str) -> Optional[Dict]:
        """
        Scrape a Reddit user's profile data
        
        Args:
            username: Reddit username
            
        Returns:
            Dict containing user data with posts and comments
        """
        try:
            # Get user overview (posts and comments)
            overview_data = self._get_user_overview(username)
            
            if not overview_data:
                return None
            
            # Get user info
            user_info = self._get_user_info(username)
            
            # Parse and organize data
            posts = []
            comments = []
            
            for item in overview_data:
                if item.get('kind') == 't3':  # Post
                    post_data = item['data']
                    posts.append({
                        'id': post_data.get('id'),
                        'title': post_data.get('title', ''),
                        'selftext': post_data.get('selftext', ''),
                        'subreddit': post_data.get('subreddit'),
                        'score': post_data.get('score', 0),
                        'created_utc': post_data.get('created_utc'),
                        'url': post_data.get('url', ''),
                        'permalink': f"https://www.reddit.com{post_data.get('permalink', '')}"
                    })
                
                elif item.get('kind') == 't1':  # Comment
                    comment_data = item['data']
                    comments.append({
                        'id': comment_data.get('id'),
                        'body': comment_data.get('body', ''),
                        'subreddit': comment_data.get('subreddit'),
                        'score': comment_data.get('score', 0),
                        'created_utc': comment_data.get('created_utc'),
                        'permalink': f"https://www.reddit.com{comment_data.get('permalink', '')}"
                    })
            
            return {
                'username': username,
                'user_info': user_info,
                'posts': posts,
                'comments': comments,
                'scraped_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error scraping user {username}: {str(e)}")
            return None
    
# In reddit_scraper.py, update the _get_user_overview method:
    def _get_user_overview(self, username: str) -> Optional[List]:
        """Get user's overview data (posts and comments)"""
        url = f"{self.base_url}/user/{username}.json"
        
        try:
            # Add delay to be respectful
            time.sleep(1)
            
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 429:
                print("Rate limited, waiting 10 seconds...")
                time.sleep(10)
                response = self.session.get(url, timeout=30)
                
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data and 'children' in data['data']:
                return data['data']['children']
            
            return None
            
        except requests.RequestException as e:
            print(f"Error fetching overview for {username}: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON for {username}: {str(e)}")
            return None
        
    def _get_user_info(self, username: str) -> Dict:
        """Get user's basic info"""
        url = f"{self.base_url}/user/{username}/about.json"
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data:
                user_data = data['data']
                return {
                    'created_utc': user_data.get('created_utc'),
                    'comment_karma': user_data.get('comment_karma', 0),
                    'link_karma': user_data.get('link_karma', 0),
                    'total_karma': user_data.get('total_karma', 0),
                    'is_verified': user_data.get('verified', False),
                    'has_verified_email': user_data.get('has_verified_email', False)
                }
            
            return {}
            
        except requests.RequestException as e:
            print(f"Error fetching user info for {username}: {str(e)}")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error parsing user info JSON for {username}: {str(e)}")
            return {}
    
    def get_multiple_pages(self, username: str, limit: int = 100) -> Optional[Dict]:
        """
        Get multiple pages of user data for more comprehensive analysis
        
        Args:
            username: Reddit username
            limit: Number of items to fetch per page
            
        Returns:
            Dict containing comprehensive user data
        """
        all_posts = []
        all_comments = []
        after = None
        
        # Get up to 3 pages of data
        for page in range(3):
            url = f"{self.base_url}/user/{username}.json?limit={limit}"
            if after:
                url += f"&after={after}"
            
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                
                if 'data' in data and 'children' in data['data']:
                    items = data['data']['children']
                    
                    if not items:
                        break
                    
                    for item in items:
                        if item.get('kind') == 't3':  # Post
                            post_data = item['data']
                            all_posts.append({
                                'id': post_data.get('id'),
                                'title': post_data.get('title', ''),
                                'selftext': post_data.get('selftext', ''),
                                'subreddit': post_data.get('subreddit'),
                                'score': post_data.get('score', 0),
                                'created_utc': post_data.get('created_utc'),
                                'url': post_data.get('url', ''),
                                'permalink': f"https://www.reddit.com{post_data.get('permalink', '')}"
                            })
                        
                        elif item.get('kind') == 't1':  # Comment
                            comment_data = item['data']
                            all_comments.append({
                                'id': comment_data.get('id'),
                                'body': comment_data.get('body', ''),
                                'subreddit': comment_data.get('subreddit'),
                                'score': comment_data.get('score', 0),
                                'created_utc': comment_data.get('created_utc'),
                                'permalink': f"https://www.reddit.com{comment_data.get('permalink', '')}"
                            })
                    
                    # Get next page token
                    after = data['data'].get('after')
                    if not after:
                        break
                    
                    # Rate limiting
                    time.sleep(1)
                
            except Exception as e:
                print(f"Error fetching page {page + 1}: {str(e)}")
                break
        
        user_info = self._get_user_info(username)
        
        return {
            'username': username,
            'user_info': user_info,
            'posts': all_posts,
            'comments': all_comments,
            'scraped_at': datetime.now().isoformat()
        }
        
    # Temporary debug version - add this to reddit_scraper.py
def _get_user_overview(self, username: str) -> Optional[List]:
    """Get user's overview data (posts and comments)"""
    url = f"{self.base_url}/user/{username}.json"
    
    print(f"DEBUG: Fetching URL: {url}")
    
    try:
        response = self.session.get(url, timeout=30)
        print(f"DEBUG: Response status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"DEBUG: Non-200 response: {response.text}")
            return None
            
        data = response.json()
        print(f"DEBUG: Got data with {len(data.get('data', {}).get('children', []))} items")
        
        if 'data' in data and 'children' in data['data']:
            return data['data']['children']
        
        return None
        
    except Exception as e:
        print(f"DEBUG: Exception: {str(e)}")
        return None