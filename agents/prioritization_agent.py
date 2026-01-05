from .base_agent import BaseAgent
from models import Analysis, Priority, RiskLevel
import json

class PrioritizationAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Prioritization Agent")

    def assess(self, analysis: dict) -> dict:
        prompt = f"""
        Determine the Priority Score and Risk Level based on the analysis.
        
        Analysis Data:
        {json.dumps(analysis, indent=2)}
        
        Rules:
        - Critical Risk: Legal threats, safety issues, severe financial loss.
        - High Risk: Service outages, recurring billing issues.
        - Priority Score: 0-100. (100 is highest priority).
        
        Output JSON format:
        {{
            "score": int,
            "risk_level": "string (Low, Medium, High, Critical)",
            "reasoning": "string"
        }}
        """
        
        response_text = self._generate(prompt)
        if response_text:
            try:
                data = json.loads(response_text)
                # Validation to ensure risk_level matches Enum
                if data["risk_level"] not in [e.value for e in RiskLevel]:
                     data["risk_level"] = "Medium" # Fallback
                return data
            except json.JSONDecodeError:
                print("Failed to parse Prioritization JSON")
                return {"score": 50, "risk_level": "Medium", "reasoning": "Parsing Error"}
        return {"score": 50, "risk_level": "Medium", "reasoning": "Generation Error"}
