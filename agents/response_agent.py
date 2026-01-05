from .base_agent import BaseAgent
import json

class ResponseDraftingAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Response Drafting Agent")

    def draft(self, complaint_text: str, decision: dict, context: str) -> dict:
        prompt = f"""
        Draft a customer service response.
        
        Complaint: "{complaint_text}"
        Decision/Action: {decision['action']}
        Tone: {decision['suggested_response_tone']}
        Context/History: "{context}"
        
        Output JSON format:
        {{
            "draft_content": "string (the actual email/message body)",
            "tone_used": "string",
            "confidence_score": float (0.0 - 1.0)
        }}
        """
        
        response_text = self._generate(prompt)
        if response_text:
            try:
                data = json.loads(response_text)
                return data
            except json.JSONDecodeError:
                print("Failed to parse Response Draft JSON")
                return {"draft_content": "We received your message and will get back to you.", "tone_used": "Neutral", "confidence_score": 0.0}
        return {"draft_content": "We received your message and will get back to you.", "tone_used": "Neutral", "confidence_score": 0.0}
