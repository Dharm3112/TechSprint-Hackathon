from .base_agent import BaseAgent
from models import Analysis, Category
import json

class ClassificationAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Classification Agent")

    def analyze(self, text: str) -> dict:
        prompt = f"""
        Analyze the following customer complaint.
        
        Complaint: "{text}"
        
        Tasks:
        1. Identify the primary Intent (e.g., Request Refund, Report Outage, General Inquiry).
        2. Classify into one of these categories: {[c.value for c in Category]}.
        3. Extract key entities (product names, locations, dates).
        
        Output JSON format:
        {{
            "intent": "string",
            "category": "string (must be one of the provided categories)",
            "key_entities": ["list", "of", "strings"]
        }}
        """
        
        response_text = self._generate(prompt)
        if response_text:
            try:
                data = json.loads(response_text)
                return data
            except json.JSONDecodeError:
                print("Failed to parse Classification JSON")
                return {"intent": "Unknown", "category": "Other", "key_entities": []}
        return {"intent": "Unknown", "category": "Other", "key_entities": []}
