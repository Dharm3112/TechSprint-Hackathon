import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# MUST BE THIS MODEL:
GENERATIVE_MODEL = "gemini-1.5-flash"  
EMBEDDING_MODEL = "models/text-embedding-004"

CHROMA_PATH = "./memory/chroma_store"
COLLECTION_NAME = "complaint_history"