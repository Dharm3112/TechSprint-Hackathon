import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Model Configuration
# FIX 1: Use the stable 1.5 model (2.0 is experimental and causes crashes)
EMBEDDING_MODEL = "models/text-embedding-004"
GENERATIVE_MODEL = "gemini-2.0-flash"  

# Vector DB Configuration
# FIX 2: Correct the path relative to main.py
# If you run main.py from the 'sentinel_adk' folder, the memory folder is just "./memory"
CHROMA_PATH = "./memory/chroma_store"
COLLECTION_NAME = "complaint_history"