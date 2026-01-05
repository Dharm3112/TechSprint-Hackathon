import chromadb
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class MemoryAgent:
    def __init__(self):
        # Initialize local database (saves to disk)
        self.client = chromadb.PersistentClient(path="./sentinel_adk/memory/chroma_store")
        self.collection = self.client.get_or_create_collection(name="complaint_history")
        self.embedding_model = "models/text-embedding-004"

    def _get_embedding(self, text):
        """Generates vector using Gemini API"""
        result = genai.embed_content(
            model=self.embedding_model,
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']

    def save_complaint(self, ticket_id, text, resolution):
        """Saves a resolved complaint to memory"""
        vector = self._get_embedding(text)
        self.collection.add(
            ids=[ticket_id],
            embeddings=[vector],
            documents=[text],
            metadatas=[{"resolution": resolution}]
        )
        print(f"💾 Memory: Saved ticket {ticket_id}")

    def search_similar(self, current_complaint):
        """Finds past similar complaints"""
        query_vector = self._get_embedding(current_complaint)
        
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=1
        )
        
        if results['documents'][0]:
            best_match = results['documents'][0][0]
            resolution = results['metadatas'][0][0]['resolution']
            return f"FOUND SIMILAR CASE: '{best_match}' \nRESOLUTION WAS: {resolution}"
        else:
            return "No similar past cases found."

# --- Quick Test ---
if __name__ == "__main__":
    mem = MemoryAgent()
    # 1. Teach it something
    mem.save_complaint("TKT-001", "My internet is down", "Reboot router")
    # 2. Ask it something similar
    print(mem.search_similar("Wifi not working"))
