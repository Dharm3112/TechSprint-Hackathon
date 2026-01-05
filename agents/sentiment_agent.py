from .base_agent import BaseAgent
import json

class SentimentAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Sentiment Agent")

    def analyze(self, text: str) -> dict:
        prompt = f"""
        Analyze the sentiment and urgency of the following complaint.
        
        Complaint: "{text}"
        
        Tasks:
        1. specific Sentiment Score from -1.0 (very negative) to 1.0 (very positive).
        2. Urgency Score from 1 (low) to 10 (critical immediate action required).
        
        Output JSON format:
        {{
            "sentiment_score": float,
            "urgency_score": int
        }}
        """
        
        response_text = self._generate(prompt)
        if response_text:
            try:
                data = json.loads(response_text)
                return data
            except json.JSONDecodeError:
                print("Failed to parse Sentiment JSON")
                return {"sentiment_score": 0.0, "urgency_score": 5}
        return {"sentiment_score": 0.0, "urgency_score": 5}
