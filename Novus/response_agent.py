from .base_agent import BaseAgent
import json

class ResponseDraftingAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Novus Drafter")

    def draft(self, complaint_text: str, decision: dict, context: str, feedback: str = None) -> dict:
        # Novus Feedback Logic
        instruction_prefix = ""
        if feedback:
            instruction_prefix = f"⚠️ PREVIOUS DRAFT REJECTED.\nCRITIC FEEDBACK: '{feedback}'\nINSTRUCTION: Rewrite the draft to address this feedback exactly.\n"

        prompt = f"""
        {instruction_prefix}
        Draft a customer service response for the agent 'Novus'.
        
        Complaint: "{complaint_text}"
        Decision: {decision['action']}
        Target Tone: {decision['suggested_response_tone']}
        Similar Past Cases: "{context}"
        
        Output JSON format:
        {{
            "draft_content": "string (the actual email body)",
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
                return {"draft_content": "Error generating draft.", "tone_used": "Neutral", "confidence_score": 0.0}
        return {"draft_content": "Error generating draft.", "tone_used": "Neutral", "confidence_score": 0.0}