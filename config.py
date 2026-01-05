import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# FIX: Use the specific, stable Flash model version
GENERATIVE_MODEL = "gemini-1.5-flash-001"  
EMBEDDING_MODEL = "models/text-embedding-004"

# Vector DB Configuration
CHROMA_PATH = "./memory/chroma_store"
COLLECTION_NAME = "complaint_history"