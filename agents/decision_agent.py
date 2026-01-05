from .base_agent import BaseAgent
from models import ActionType
import json

class DecisionAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Decision Agent")

    def decide(self, complaint_text: str, analysis: dict, priority: dict, history: str) -> dict:
        prompt = f"""
        Decide the next best action for this complaint.
        
        Complaint: "{complaint_text}"
        Analysis: {json.dumps(analysis)}
        Priority: {json.dumps(priority)}
        Similar Case History: "{history}"
        
        Available Actions: {[a.value for a in ActionType]}
        
        Output JSON format:
        {{
            "action": "string (must be one of available actions)",
            "suggested_response_tone": "string (e.g., Apologetic, Firm, Empathetic)",
            "requires_human_approval": boolean,
            "reasoning": "short explanation"
        }}
        """
        
        response_text = self._generate(prompt)
        if response_text:
            try:
                data = json.loads(response_text)
                return data
            except json.JSONDecodeError:
                print("Failed to parse Decision JSON")
                return {"action": "Reply", "suggested_response_tone": "Professional", "requires_human_approval": True, "reasoning": "Error"}
        return {"action": "Reply", "suggested_response_tone": "Professional", "requires_human_approval": True, "reasoning": "Error"}
