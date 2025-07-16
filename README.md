Reddit User Persona Generator
A Python tool that analyzes Reddit user profiles and generates detailed user personas using LLM analysis. This tool scrapes public Reddit data and creates comprehensive user profiles with cited sources.
🚀 Features

Scrapes Reddit posts and comments using official Reddit API
Generates detailed user personas using various LLM options (Gemini, Groq, Local LLMs, Hugging Face)
Provides citations for every trait identified
Exports personas in readable text format
Supports multiple free LLM options

📋 Prerequisites

Python 3.8+
Reddit API credentials (free)
At least one LLM API key (free options available)

🛠️ Setup
1. Clone the Repository
bashgit clone https://github.com/Sritankar/assingment-task.git
cd reddit-user-persona
2. Install Dependencies
bashpip install -r requirements.txt
3. Configure API Keys
Create a .env file based on .env.example:
bashcp .env.example .env
Edit .env and add your credentials:
Reddit API Setup:

Go to https://www.reddit.com/prefs/apps
Click "Create App" or "Create Another App"
Fill in the details:

Name: Your app name
App type: Select "script"
Description: Brief description
About URL: Can be left blank
Redirect URI: http://localhost:8080


Copy the Client ID and Client Secret

LLM Configuration:
Choose one of these free options:
Option 1: Google Gemini (Recommended)
envUSE_GEMINI=true
GEMINI_API_KEY=your_gemini_api_key_here
Get your free API key from: https://makersuite.google.com/app/apikey
Option 2: Groq
envUSE_GROQ=true
GROQ_API_KEY=your_groq_api_key_here
Get your free API key from: https://console.groq.com/keys
Option 3: Local LLM with Ollama
envUSE_LOCAL_LLM=true
LOCAL_LLM_MODEL=llama2
Install Ollama from: https://ollama.ai
Option 4: Hugging Face
envUSE_HUGGINGFACE=true
HUGGINGFACE_API_KEY=your_hf_api_key_here
Get your free API key from: https://huggingface.co/settings/tokens
4. Run the Script
bashpython main.py https://www.reddit.com/user/username/
📚 Usage Examples
bash# Basic usage
python main.py https://www.reddit.com/user/kojied/

# With custom output filename
python main.py https://www.reddit.com/user/kojied/ --output kojied_analysis

# Process multiple users
python main.py https://www.reddit.com/user/Hungry-Move-6603/
python main.py https://www.reddit.com/user/techie_wanderer/
📄 Output Format
The script generates a text file in the outputs/ directory with:

User demographics and characteristics
Interests and hobbies
Communication style
Professional background
Values and beliefs
Online behavior patterns
Citations linking each trait to specific posts/comments

Sample Output Structure:
USER PERSONA: username
Generated on: 2024-01-15 14:32:45
================================================================================

DEMOGRAPHICS:
----------------------------------------
Age Range: 25-35 years old
Location: San Francisco, CA
[Citations with links to supporting posts/comments]

INTERESTS AND HOBBIES:
----------------------------------------
- Software Development
- Photography
- Gaming
[Citations with links to supporting posts/comments]

[... additional sections ...]
🤖 Using Local LLMs (Optional)
To use a local LLM instead of cloud APIs:

Install and run Ollama:
bash# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama2

Set USE_LOCAL_LLM=true in your .env file
Configure LOCAL_LLM_MODEL with your preferred model

📁 Project Structure
reddit-user-persona/
│
├── src/
│   ├── reddit_scraper.py      # Reddit API integration
│   ├── persona_generator.py   # LLM persona generation
│   ├── utils.py              # Helper functions
│   └── config.py             # Configuration management
│
├── outputs/                   # Generated personas
├── main.py                   # Main script
├── requirements.txt          # Dependencies
├── .env.example             # Environment template
└── README.md                # This file
🔒 Privacy & Ethics

Only analyzes publicly available Reddit data
Respects Reddit's API rate limits
Does not store or share personal information
Generated personas are for analysis purposes only

🐛 Troubleshooting
Common Issues:

"Invalid Reddit profile URL": Ensure URL format is https://www.reddit.com/user/username/
"No LLM configured": Make sure at least one LLM option is set to true in .env
Rate limiting: Reddit API has rate limits. Wait a few minutes between requests
Authentication errors: Double-check your API credentials in .env

📝 Code Style
This project follows PEP-8 guidelines for Python code style.
📜 License
This code is provided for the BeyondChats internship assignment evaluation only.
🤝 Contributing
This is an assignment project. For the production version, contributions would be welcome via pull requests.
📧 Contact
For questions about this assignment implementation, please contact [your-email@example.com]
