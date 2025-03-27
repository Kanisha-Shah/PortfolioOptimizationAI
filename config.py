import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Ensure API keys are loaded
if not OPENAI_API_KEY or not DEEPSEEK_API_KEY:
    raise ValueError("One or more API keys are missing. Check your .env file.")

print("✅ API keys loaded successfully!")