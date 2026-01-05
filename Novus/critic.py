from .base_agent import BaseAgent
import json

class CriticAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Novus Critic")

    def review(self, complaint_text: str, current_draft: str, risk_score: int) -> dict:
        prompt = f"""
        You are the 'Novus' Quality Assurance Supervisor. 
        Review the draft response below.
        
        Customer Complaint: "{complaint_text}"
        Calculated Risk Score: {risk_score}/10
        Current Draft: "{current_draft}"
        
        STRICT CRITERIA:
        1. Tone Mismatch: If Risk > 7, tone MUST be Formal & Apologetic. No "Hey there!" or emojis.
        2. Empathy: Does it explicitly acknowledge the specific issue (e.g., "I see you were double-charged")?
        3. Compliance: If the user mentions "lawsuit" or "court", ensure we promised an escalation/investigation.
        
        Output strictly in JSON format:
        {{
            "status": "PASS" or "FAIL",
            "feedback": "Short, specific instruction on what to fix (e.g., 'Remove emojis, sound more serious').",
            "escalation_needed": boolean (true if the draft missed a critical legal threat)
        }}
        """
        
        response_text = self._generate(prompt)
        if response_text:
            try:
                data = json.loads(response_text)
                # Fail-safe defaults
                if "status" not in data: data["status"] = "PASS"
                return data
            except json.JSONDecodeError:
                return {"status": "PASS", "feedback": "", "escalation_needed": False}
        return {"status": "PASS", "feedback": "", "escalation_needed": False}