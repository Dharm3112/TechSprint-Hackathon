import google.generativeai as genai
from config import GENERATIVE_MODEL, GEMINI_API_KEY
import json
import time

class BaseAgent:
    def __init__(self, name="Base Agent"):
        self.name = name
        # Configure the API Key
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GENERATIVE_MODEL)

    def _generate(self, prompt, json_mode=True):
        # Reduced sleep time from 4s to 1s for speed
        time.sleep(1.0) 
        
        try:
            full_prompt = prompt
            if json_mode:
                full_prompt += "\n\nRespond strictly in valid JSON format."
            
            response = self.model.generate_content(full_prompt)
            
            cleaned_text = response.text.strip()
            # Clean up markdown code blocks if the AI adds them
            if cleaned_text.startswith("```"):
                lines = cleaned_text.splitlines()
                # Remove first and last lines (```json and ```)
                if lines[0].startswith("```"): lines = lines[1:]
                if lines[-1].startswith("```"): lines = lines[:-1]
                cleaned_text = "\n".join(lines)
            
            return cleaned_text.strip()
        except Exception as e:
            print(f"Error in {self.name}: {e}")
            return None