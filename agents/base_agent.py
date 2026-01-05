import google.generativeai as genai
from config import GENERATIVE_MODEL, GEMINI_API_KEY
import json
import time

class BaseAgent:
    def __init__(self, name="Base Agent"):
        self.name = name
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GENERATIVE_MODEL)

    def _generate(self, prompt, json_mode=True):
        """Helper to generate content with Gemini"""
        # Rate Limiting for Free Tier (approx 15 RPM = ~4s delay)
        # We add a small buffer to be safe.
        time.sleep(10.0) 
        
        try:
            full_prompt = prompt
            if json_mode:
                full_prompt += "\n\nRespond strictly in valid JSON format."
            
            response = self.model.generate_content(full_prompt)
            
            cleaned_text = response.text.strip()
            # Remove markdown code blocks if present
            if cleaned_text.startswith("```"):
                cleaned_text = cleaned_text.strip("`")
                if cleaned_text.startswith("json"):
                    cleaned_text = cleaned_text[4:]
            
            return cleaned_text.strip()
        except Exception as e:
            print(f"Error in {self.name}: {e}")
            return None
