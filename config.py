import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Model Configuration
EMBEDDING_MODEL = "models/text-embedding-004"
GENERATIVE_MODEL = "gemini-2.0-flash"

# Vector DB Configuration
CHROMA_PATH = "./sentinel_adk/memory/chroma_store"
COLLECTION_NAME = "complaint_history"
