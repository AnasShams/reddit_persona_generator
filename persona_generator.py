"""
Persona Generator Module
Generates user personas from Reddit data using text analysis
"""

import re
import json
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List, Set, Tuple
import statistics

class PersonaGenerator:
    """Generates user personas from Reddit data"""
    
    def __init__(self):
        self.interests_keywords = {
            'technology': ['tech', 'programming', 'code', 'software', 'developer', 'computer', 'AI', 'machine learning'],
            'gaming': ['game', 'gaming', 'xbox', 'playstation', 'nintendo', 'steam', 'esports'],
            'fitness': ['gym', 'workout', 'exercise', 'fitness', 'health', 'running', 'lifting'],
            'food': ['cooking', 'recipe', 'food', 'restaurant', 'meal', 'diet', 'nutrition'],
            'travel': ['travel', 'trip', 'vacation', 'country', 'city', 'flight', 'hotel'],
            'music': ['music', 'song', 'album', 'artist', 'concert', 'band', 'listen'],
            'movies': ['movie', 'film', 'cinema', 'actor', 'director', 'netflix', 'series'],
            'books': ['book', 'read', 'author', 'novel', 'literature', 'story', 'chapter'],
            'sports': ['sport', 'football', 'basketball', 'soccer', 'baseball', 'hockey', 'tennis'],
            'politics': ['politics', 'political', 'government', 'election', 'vote', 'policy', 'democracy']
        }
        
        self.sentiment_positive = ['good', 'great', 'awesome', 'amazing', 'love', 'like', 'best', 'excellent', 'fantastic']
        self.sentiment_negative = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'worst', 'horrible', 'sucks']
        
        self.personality_indicators = {
            'extrovert': ['social', 'party', 'meeting', 'friends', 'crowd', 'public', 'group'],
            'introvert': ['alone', 'quiet', 'home', 'solitude', 'private', 'solo', 'myself'],
            'analytical': ['analyze', 'data', 'logic', 'reason', 'think', 'research', 'study'],
            'creative': ['creative', 'art', 'design', 'music', 'write', 'create', 'imagine'],
            'practical': ['practical', 'useful', 'efficient', 'work', 'solution', 'fix', 'build']
        }
    
    def generate_persona(self, user_data: Dict) -> str:
        """
        Generate a comprehensive user persona
        
        Args:
            user_data: Dict containing user's posts and comments
            
        Returns:
            String containing the formatted persona
        """
        username = user_data['username']
        posts = user_data['posts']
        comments = user_data['comments']
        user_info = user_data.get('user_info', {})
        
        # Combine all text content
        all_text = []
        citations = []
        
        for post in posts:
            text = f"{post.get('title', '')} {post.get('selftext', '')}"
            all_text.append(text.lower())
            citations.append({
                'type': 'post',
                'text': text,
                'subreddit': post.get('subreddit'),
                'permalink': post.get('permalink'),
                'score': post.get('score', 0)
            })
        
        for comment in comments:
            text = comment.get('body', '')
            all_text.append(text.lower())
            citations.append({
                'type': 'comment',
                'text': text,
                'subreddit': comment.get('subreddit'),
                'permalink': comment.get('permalink'),
                'score': comment.get('score', 0)
            })
        
        # Generate persona components
        basic_info = self._generate_basic_info(username, user_info, posts, comments)
        interests = self._analyze_interests(all_text, citations)
        personality = self._analyze_personality(all_text, citations)
        behavior = self._analyze_behavior(posts, comments, citations)
        goals = self._analyze_goals(all_text, citations)
        frustrations = self._analyze_frustrations(all_text, citations)
        
        # Format persona
        persona = self._format_persona(
            basic_info, interests, personality, behavior, goals, frustrations
        )
        
        return persona
    
    def _generate_basic_info(self, username: str, user_info: Dict, posts: List, comments: List) -> Dict:
        """Generate basic user information"""
        account_age = "Unknown"
        if user_info.get('created_utc'):
            created_date = datetime.fromtimestamp(user_info['created_utc'])
            account_age = f"{(datetime.now() - created_date).days} days"
        
        total_karma = user_info.get('total_karma', 0)
        comment_karma = user_info.get('comment_karma', 0)
        link_karma = user_info.get('link_karma', 0)
        
        # Most active subreddits
        subreddits = []
        for post in posts:
            if post.get('subreddit'):
                subreddits.append(post['subreddit'])
        for comment in comments:
            if comment.get('subreddit'):
                subreddits.append(comment['subreddit'])
        
        top_subreddits = Counter(subreddits).most_common(5)
        
        return {
            'username': username,
            'account_age': account_age,
            'total_karma': total_karma,
            'comment_karma': comment_karma,
            'link_karma': link_karma,
            'total_posts': len(posts),
            'total_comments': len(comments),
            'top_subreddits': top_subreddits
        }
    
    def _analyze_interests(self, all_text: List[str], citations: List[Dict]) -> Dict:
        """Analyze user interests based on text content"""
        interest_scores = defaultdict(int)
        interest_citations = defaultdict(list)
        
        combined_text = ' '.join(all_text)
        
        for interest, keywords in self.interests_keywords.items():
            for keyword in keywords:
                count = combined_text.count(keyword)
                interest_scores[interest] += count
                
                # Find citations for this interest
                for i, citation in enumerate(citations):
                    if keyword in citation['text'].lower():
                        interest_citations[interest].append(citation)
        
        # Get top interests
        top_interests = sorted(interest_scores.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'top_interests': top_interests,
            'citations': dict(interest_citations)
        }
    
    def _analyze_personality(self, all_text: List[str], citations: List[Dict]) -> Dict:
        """Analyze personality traits"""
        personality_scores = defaultdict(int)
        personality_citations = defaultdict(list)
        
        combined_text = ' '.join(all_text)
        
        for trait, keywords in self.personality_indicators.items():
            for keyword in keywords:
                count = combined_text.count(keyword)
                personality_scores[trait] += count
                
                # Find citations
                for citation in citations:
                    if keyword in citation['text'].lower():
                        personality_citations[trait].append(citation)
        
        # Determine dominant traits
        dominant_traits = sorted(personality_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            'dominant_traits': dominant_traits,
            'citations': dict(personality_citations)
        }
    
    def _analyze_behavior(self, posts: List, comments: List, citations: List[Dict]) -> Dict:
        """Analyze user behavior patterns"""
        behaviors = []
        behavior_citations = []
        
        # Posting frequency
        if len(posts) > len(comments):
            behaviors.append("More likely to create original posts than comment")
        elif len(comments) > len(posts):
            behaviors.append("More active in commenting than posting")
        
        # Average scores
        if posts:
            avg_post_score = statistics.mean([p.get('score', 0) for p in posts])
            if avg_post_score > 10:
                behaviors.append("Creates engaging content with good community response")
        
        if comments:
            avg_comment_score = statistics.mean([c.get('score', 0) for c in comments])
            if avg_comment_score > 5:
                behaviors.append("Provides valuable comments that receive positive feedback")
        
        # Most active subreddits
        subreddits = []
        for post in posts:
            if post.get('subreddit'):
                subreddits.append(post['subreddit'])
        for comment in comments:
            if comment.get('subreddit'):
                subreddits.append(comment['subreddit'])
        
        if subreddits:
            top_subreddit = Counter(subreddits).most_common(1)[0]
            behaviors.append(f"Most active in r/{top_subreddit[0]} with {top_subreddit[1]} interactions")
        
        return {
            'behaviors': behaviors,
            'citations': behavior_citations
        }
    
    def _analyze_goals(self, all_text: List[str], citations: List[Dict]) -> Dict:
        """Analyze user goals and motivations"""
        goal_keywords = ['want', 'need', 'goal', 'hope', 'wish', 'trying', 'learning', 'improve']
        goals = []
        goal_citations = []
        
        combined_text = ' '.join(all_text)
        
        for citation in citations:
            text = citation['text'].lower()
            for keyword in goal_keywords:
                if keyword in text:
                    # Extract sentence containing the goal
                    sentences = text.split('.')
                    for sentence in sentences:
                        if keyword in sentence:
                            goals.append(sentence.strip())
                            goal_citations.append(citation)
                            break
        
        return {
            'goals': goals[:5],  # Top 5 goals
            'citations': goal_citations[:5]
        }
    
    def _analyze_frustrations(self, all_text: List[str], citations: List[Dict]) -> Dict:
        """Analyze user frustrations"""
        frustration_keywords = ['frustrated', 'annoying', 'hate', 'problem', 'issue', 'difficult', 'hard', 'struggle']
        frustrations = []
        frustration_citations = []
        
        for citation in citations:
            text = citation['text'].lower()
            for keyword in frustration_keywords:
                if keyword in text:
                    sentences = text.split('.')
                    for sentence in sentences:
                        if keyword in sentence:
                            frustrations.append(sentence.strip())
                            frustration_citations.append(citation)
                            break
        
        return {
            'frustrations': frustrations[:5],  # Top 5 frustrations
            'citations': frustration_citations[:5]
        }
    
    def _format_persona(self, basic_info: Dict, interests: Dict, personality: Dict, 
                       behavior: Dict, goals: Dict, frustrations: Dict) -> str:
        """Format the persona into a readable text file"""
        
        persona = f"""
USER PERSONA: {basic_info['username']}
{'=' * 60}

BASIC INFORMATION:
• Username: {basic_info['username']}
• Account Age: {basic_info['account_age']}
• Total Karma: {basic_info['total_karma']}
• Posts Created: {basic_info['total_posts']}
• Comments Made: {basic_info['total_comments']}

TOP SUBREDDITS:
"""
        
        for subreddit, count in basic_info['top_subreddits']:
            persona += f"• r/{subreddit} ({count} interactions)\n"
        
        persona += f"""
INTERESTS & HOBBIES:
"""
        
        for interest, score in interests['top_interests']:
            if score > 0:
                persona += f"• {interest.title()}: {score} mentions\n"
                # Add citations
                if interest in interests['citations']:
                    citations = interests['citations'][interest][:3]  # Top 3 citations
                    for citation in citations:
                        persona += f"  - Citation: r/{citation.get('subreddit', 'unknown')} - {citation['text'][:100]}...\n"
                        persona += f"    Link: {citation.get('permalink', 'N/A')}\n"
        
        persona += f"""
PERSONALITY TRAITS:
"""
        
        for trait, score in personality['dominant_traits']:
            if score > 0:
                persona += f"• {trait.title()}: {score} indicators\n"
                # Add citations
                if trait in personality['citations']:
                    citations = personality['citations'][trait][:2]  # Top 2 citations
                    for citation in citations:
                        persona += f"  - Citation: r/{citation.get('subreddit', 'unknown')} - {citation['text'][:100]}...\n"
                        persona += f"    Link: {citation.get('permalink', 'N/A')}\n"
        
        persona += f"""
BEHAVIOR PATTERNS:
"""
        
        for behavior_item in behavior['behaviors']:
            persona += f"• {behavior_item}\n"
        
        persona += f"""
GOALS & MOTIVATIONS:
"""
        
        for goal in goals['goals']:
            if goal:
                persona += f"• {goal}\n"
        
        if goals['citations']:
            persona += "Citations:\n"
            for citation in goals['citations']:
                persona += f"  - r/{citation.get('subreddit', 'unknown')}: {citation.get('permalink', 'N/A')}\n"
        
        persona += f"""
FRUSTRATIONS & PAIN POINTS:
"""
        
        for frustration in frustrations['frustrations']:
            if frustration:
                persona += f"• {frustration}\n"
        
        if frustrations['citations']:
            persona += "Citations:\n"
            for citation in frustrations['citations']:
                persona += f"  - r/{citation.get('subreddit', 'unknown')}: {citation.get('permalink', 'N/A')}\n"
        
        persona += f"""
{'=' * 60}
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return persona