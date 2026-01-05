import json
import numpy as np
import os
import google.generativeai as genai
from dotenv import load_dotenv
from config import GEMINI_API_KEY, EMBEDDING_MODEL

# Load API Key
load_dotenv()
genai.configure(api_key=GEMINI_API_KEY)

class MemoryAgent:
    def __init__(self):
        self.memory_file = "./sentinel_adk/memory/simple_store.json"
        self.embedding_model = EMBEDDING_MODEL
        self._load_memory()
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)

    def _load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                self.store = json.load(f)
        else:
            self.store = {"ids": [], "documents": [], "embeddings": [], "metadatas": []}

    def _save_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump(self.store, f)

    def _get_embedding(self, text):
        """Generates vector using Gemini API"""
        try:
            result = genai.embed_content(
                model=self.embedding_model,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"Embedding Error: {e}")
            return [0.0] * 768 # Fallback empty vector

    def save_complaint(self, ticket_id, text, resolution, meta_tags=None):
        """Saves a resolved complaint to memory"""
        vector = self._get_embedding(text)
        
        metadata = {"resolution": resolution}
        if meta_tags:
            metadata.update(meta_tags)
            
        self.store["ids"].append(ticket_id)
        self.store["documents"].append(text)
        self.store["embeddings"].append(vector)
        self.store["metadatas"].append(metadata)
        
        self._save_memory()
        print(f"💾 Memory: Saved ticket {ticket_id}")

    def search_similar(self, current_complaint, n_results=1):
        """Finds past similar complaints using Cosine Similarity"""
        if not self.store["embeddings"]:
            return "No similar past cases found."

        query_vector = np.array(self._get_embedding(current_complaint))
        
        # Calculate Cosine Similarity manually or with numpy
        stored_vectors = np.array(self.store["embeddings"])
        
        # Cosine Sim: (A . B) / (||A|| * ||B||)
        norm_query = np.linalg.norm(query_vector)
        norm_stored = np.linalg.norm(stored_vectors, axis=1)
        
        # Avoid division by zero
        if norm_query == 0 or np.any(norm_stored == 0):
            return "No valid embeddings found."

        similarities = np.dot(stored_vectors, query_vector) / (norm_stored * norm_query)
        
        # Find best match
        best_idx = np.argmax(similarities)
        best_score = similarities[best_idx]
        
        if best_score > 0.6: # Threshold
            best_match = self.store["documents"][best_idx]
            metadata = self.store["metadatas"][best_idx]
            resolution = metadata.get('resolution', 'No resolution record')
            return f"FOUND SIMILAR CASE (Score: {best_score:.2f}): '{best_match}' \nRESOLUTION WAS: {resolution}"
        else:
            return "No similar past cases found."

# --- Quick Test ---
if __name__ == "__main__":
    mem = MemoryAgent()
    # 1. Teach it something if empty
    if not mem.store["ids"]:
        mem.save_complaint("TKT-001", "My internet is down", "Reboot router")
    # 2. Ask it something similar
    print(mem.search_similar("Wifi not working"))
