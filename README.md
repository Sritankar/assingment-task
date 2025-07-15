# Reddit User Persona Generator

A Python script that analyzes Reddit user profiles and generates detailed user personas using LLM technology.

## Features

- Scrapes posts and comments from Reddit user profiles
- Analyzes user behavior, interests, and communication patterns
- Generates comprehensive user personas using AI/LLM
- Provides citations for each persona characteristic
- Outputs results in an easy-to-read text format

## Setup

### 1. Clone the Repository
```bash

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

4. Run the Script
bashpython main.py https://www.reddit.com/user/username/
Usage Examples
bash# Basic usage
python main.py https://www.reddit.com/user/kojied/

# Process multiple users
python main.py https://www.reddit.com/user/Hungry-Move-6603/
Output Format
The script generates a text file in the outputs/ directory with:

User demographics and characteristics
Interests and hobbies
Communication style
Professional background
Values and beliefs
Online behavior patterns
Citations linking each trait to specific posts/comments

Using Local LLMs (Optional)
To use a local LLM instead of OpenAI:

Install and run Ollama or similar local LLM server
Set USE_LOCAL_LLM=true in your .env file
Configure LOCAL_LLM_ENDPOINT with your server URL

Code Style
This project follows PEP-8 guidelines for Python code style.
License
This code is provided for the BeyondChats internship assignment evaluation only.