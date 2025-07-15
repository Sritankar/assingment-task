import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Reddit API Configuration
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
    REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')
    
    # LLM Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    USE_LOCAL_LLM = os.getenv('USE_LOCAL_LLM', 'false').lower() == 'true'
    LOCAL_LLM_ENDPOINT = os.getenv('LOCAL_LLM_ENDPOINT')
    
    # Scraping Configuration
    MAX_POSTS = 50
    MAX_COMMENTS = 100
    
    # Output Configuration
    OUTPUT_DIR = 'outputs'