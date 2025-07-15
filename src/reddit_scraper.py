import praw
from typing import Dict, List, Optional
from datetime import datetime
from .config import Config

class RedditScraper:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=Config.REDDIT_CLIENT_ID,
            client_secret=Config.REDDIT_CLIENT_SECRET,
            user_agent=Config.REDDIT_USER_AGENT
        )
    
    def extract_username(self, profile_url: str) -> str:
        """Extract username from Reddit profile URL."""
        parts = profile_url.strip('/').split('/')
        if 'user' in parts:
            user_index = parts.index('user')
            if user_index + 1 < len(parts):
                return parts[user_index + 1]
        raise ValueError(f"Invalid Reddit profile URL: {profile_url}")
    
    def scrape_user_content(self, username: str) -> Dict:
        """Scrape posts and comments from a Reddit user."""
        try:
            user = self.reddit.redditor(username)
            
            # Get user's posts
            posts = []
            for submission in user.submissions.new(limit=Config.MAX_POSTS):
                post_data = {
                    'id': submission.id,
                    'title': submission.title,
                    'content': submission.selftext,
                    'subreddit': str(submission.subreddit),
                    'created_utc': datetime.fromtimestamp(submission.created_utc).isoformat(),
                    'score': submission.score,
                    'url': f"https://reddit.com{submission.permalink}",
                    'type': 'post'
                }
                posts.append(post_data)
            
            # Get user's comments
            comments = []
            for comment in user.comments.new(limit=Config.MAX_COMMENTS):
                comment_data = {
                    'id': comment.id,
                    'content': comment.body,
                    'subreddit': str(comment.subreddit),
                    'created_utc': datetime.fromtimestamp(comment.created_utc).isoformat(),
                    'score': comment.score,
                    'url': f"https://reddit.com{comment.permalink}",
                    'type': 'comment'
                }
                comments.append(comment_data)
            
            # Get user metadata
            user_data = {
                'username': username,
                'account_created': datetime.fromtimestamp(user.created_utc).isoformat(),
                'link_karma': user.link_karma,
                'comment_karma': user.comment_karma,
                'posts': posts,
                'comments': comments
            }
            
            return user_data
            
        except Exception as e:
            raise Exception(f"Error scraping user {username}: {str(e)}")