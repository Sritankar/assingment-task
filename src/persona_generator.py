import json
import requests
from typing import Dict, List
from .config import Config
import os

class PersonaGenerator:
    def __init__(self):
        # Check environment variables properly
        self.USE_GEMINI = os.getenv('USE_GEMINI', 'false').lower() == 'true'
        self.USE_GROQ = os.getenv('USE_GROQ', 'false').lower() == 'true'
        self.USE_LOCAL_LLM = os.getenv('USE_LOCAL_LLM', 'false').lower() == 'true'
        self.USE_HUGGINGFACE = os.getenv('USE_HUGGINGFACE', 'false').lower() == 'true'
        
        if self.USE_GEMINI:
            # Google's Gemini API (free tier available)
            import google.generativeai as genai
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            # Updated model name - use gemini-1.5-flash for free tier
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        elif self.USE_GROQ:
            # Groq API (free tier available)
            from groq import Groq
            self.groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        elif self.USE_LOCAL_LLM:
            # Local LLM (completely free)
            self.llm_endpoint = os.getenv('LOCAL_LLM_ENDPOINT', 'http://localhost:11434/api/generate')
        elif self.USE_HUGGINGFACE:
            # Hugging Face API
            self.hf_api_key = os.getenv('HUGGINGFACE_API_KEY')
    
    def generate_persona(self, user_data: Dict) -> Dict:
        """Generate user persona using LLM based on scraped data."""
        
        # Prepare content for analysis
        content_summary = self._prepare_content_summary(user_data)
        
        # Generate persona using appropriate LLM
        if self.USE_GEMINI:
            persona = self._generate_with_gemini(content_summary)
        elif self.USE_GROQ:
            persona = self._generate_with_groq(content_summary)
        elif self.USE_LOCAL_LLM:
            persona = self._generate_with_local_llm(content_summary)
        elif self.USE_HUGGINGFACE:
            persona = self._generate_with_huggingface(content_summary)
        else:
            raise ValueError("No LLM configured. Please set one of USE_GEMINI, USE_GROQ, USE_LOCAL_LLM, or USE_HUGGINGFACE to true in your .env file")
        
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
    
    def _generate_with_gemini(self, content_summary: str) -> Dict:
        """Generate persona using Google Gemini API."""
        prompt = self._get_analysis_prompt(content_summary)
        
        response = self.model.generate_content(prompt)
        
        # Parse the response - Gemini might return plain text
        try:
            return json.loads(response.text)
        except:
            # If not JSON, create a structured response
            return {"analysis": response.text}
    
    def _generate_with_groq(self, content_summary: str) -> Dict:
        """Generate persona using Groq API."""
        prompt = self._get_analysis_prompt(content_summary)
        
        chat_completion = self.groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at analyzing online behavior and creating detailed user personas. Always respond with valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="mixtral-8x7b-32768",  # Free model
            temperature=0.7,
            max_tokens=1500
        )
        
        return json.loads(chat_completion.choices[0].message.content)
    
    def _generate_with_local_llm(self, content_summary: str) -> Dict:
        """Generate persona using local LLM (Ollama)."""
        import ollama
        
        prompt = self._get_analysis_prompt(content_summary)
        
        response = ollama.chat(model=os.getenv('LOCAL_LLM_MODEL', 'llama2'), messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ])
        
        try:
            return json.loads(response['message']['content'])
        except:
            return {"analysis": response['message']['content']}
    
    def _generate_with_huggingface(self, content_summary: str) -> Dict:
        """Generate persona using Hugging Face Inference API."""
        API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
        headers = {"Authorization": f"Bearer {self.hf_api_key}"}
        
        prompt = self._get_analysis_prompt(content_summary)
        
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        result = response.json()
        
        try:
            return json.loads(result[0]['generated_text'])
        except:
            return {"analysis": result[0]['generated_text']}
    
    def _get_analysis_prompt(self, content_summary: str) -> str:
        """Get the analysis prompt for LLM."""
        return f"""Analyze the following Reddit user data and create a detailed user persona.

{content_summary}

Generate a comprehensive user persona including:
1. Demographics (estimated age range, gender if apparent, location if mentioned)
2. Interests and hobbies
3. Professional background or expertise
4. Communication style
5. Values and beliefs
6. Online behavior patterns
7. Potential needs or pain points

Format the response as a JSON object with these categories as keys. If you cannot determine certain aspects, indicate "unknown" or "not apparent"."""
    
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
