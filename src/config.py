import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
    REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')
    
    
    USE_GEMINI = os.getenv('USE_GEMINI', 'false').lower() == 'true'
    USE_GROQ = os.getenv('USE_GROQ', 'false').lower() == 'true'
    USE_LOCAL_LLM = os.getenv('USE_LOCAL_LLM', 'false').lower() == 'true'
    USE_HUGGINGFACE = os.getenv('USE_HUGGINGFACE', 'false').lower() == 'true'
    
    
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
    
    
    LOCAL_LLM_MODEL = os.getenv('LOCAL_LLM_MODEL', 'llama2')
    LOCAL_LLM_ENDPOINT = os.getenv('LOCAL_LLM_ENDPOINT', 'http://localhost:11434/api/generate')
    
    
    MAX_POSTS = int(os.getenv('MAX_POSTS', '50'))
    MAX_COMMENTS = int(os.getenv('MAX_COMMENTS', '100'))
    
    
    OUTPUT_DIR = 'outputs'
