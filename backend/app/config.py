import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "nutrilens")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI is not configured in .env")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is not configured in .env")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not configured in .env")