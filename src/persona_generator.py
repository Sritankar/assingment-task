import json
import requests
from typing import Dict, List
from .config import Config
import google.generativeai as genai
from groq import Groq

class PersonaGenerator:
    def __init__(self):
        if Config.USE_GEMINI:
            # Google's Gemini API (free tier available)
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
        elif Config.USE_GROQ:
            # Groq API (free tier available)
            self.groq_client = Groq(api_key=Config.GROQ_API_KEY)
        elif Config.USE_LOCAL_LLM:
            # Local LLM (completely free)
            self.llm_endpoint = Config.LOCAL_LLM_ENDPOINT
    
    def generate_persona(self, user_data: Dict) -> Dict:
        """Generate user persona using LLM based on scraped data."""
        
        # Prepare content for analysis
        content_summary = self._prepare_content_summary(user_data)
        
        # Generate persona using LLM
        if Config.USE_LOCAL_LLM:
            persona = self._generate_with_local_llm(content_summary)
        else:
            persona = self._generate_with_openai(content_summary)
        
        # Add citations
        persona_with_citations = self._add_citations(persona, user_data)
        
        return persona_with_citations
    
    def _prepare_content_summary(self, user_data: Dict) -> str:
        """Prepare a summary of user content for LLM analysis."""
        summary = f"Username: {user_data['username']}\n"
        summary += f"Account age: {user_data['account_created']}\n"
        summary += f"Karma: {user_data['link_karma']} link, {user_data['comment_karma']} comment\n\n"
        
        summary += "Recent Posts:\n"
        for post in user_data['posts'][:20]:
            summary += f"- [{post['subreddit']}] {post['title']}: {post['content'][:200]}...\n"
        
        summary += "\nRecent Comments:\n"
        for comment in user_data['comments'][:30]:
            summary += f"- [{comment['subreddit']}] {comment['content'][:150]}...\n"
        
        return summary
    
    def _generate_with_openai(self, content_summary: str) -> Dict:
        """Generate persona using OpenAI API."""
        prompt = f"""Analyze the following Reddit user data and create a detailed user persona.

{content_summary}

Generate a comprehensive user persona including:
1. Demographics (estimated age range, gender if apparent, location if mentioned)
2. Interests and hobbies
3. Professional background or expertise
4. Communication style
5. Values and beliefs
6. Online behavior patterns
7. Potential needs or pain points

Format the response as a JSON object with these categories as keys."""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert at analyzing online behavior and creating detailed user personas."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        return json.loads(response.choices[0].message.content)
    
    def _add_citations(self, persona: Dict, user_data: Dict) -> Dict:
        """Add citations to persona characteristics."""
        # Implementation to match persona traits with specific posts/comments
        # This is a simplified version - you'd want more sophisticated matching
        
        cited_persona = {}
        all_content = user_data['posts'] + user_data['comments']
        
        for category, traits in persona.items():
            cited_persona[category] = {
                'traits': traits,
                'citations': self._find_supporting_content(traits, all_content)
            }
        
        return cited_persona
    
    def _find_supporting_content(self, traits: any, content: List[Dict]) -> List[Dict]:
        """Find content that supports the identified traits."""
        citations = []
        
        # Convert traits to string for searching
        traits_str = str(traits).lower()
        
        for item in content:
            item_text = (item.get('title', '') + ' ' + item.get('content', '')).lower()
            
            # Simple keyword matching - can be improved with NLP
            if any(word in item_text for word in traits_str.split()[:5]):
                citations.append({
                    'type': item['type'],
                    'url': item['url'],
                    'excerpt': item.get('content', item.get('title', ''))[:100] + '...'
                })
                
                if len(citations) >= 3:  # Limit citations per category
                    break
        
        return citations