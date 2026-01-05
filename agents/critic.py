import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
import json

# Initialize Vertex AI (Ensure you run 'gcloud auth login' first)
vertexai.init(project="your-gcp-project-id", location="us-central1")

class CriticAgent:
    def __init__(self):
        # Using Pro model for better reasoning capabilities
        self.model = GenerativeModel("gemini-1.5-pro-001")
        
        # Load the system instruction defined above
        self.system_prompt = """
        You are the Quality Assurance Supervisor. 
        Evaluate the draft. Output strictly in JSON.
        Criteria: Tone Match, Policy Check, Empathy.
        """

    def review_draft(self, complaint_text, risk_score, draft_response):
        user_prompt = f"""
        ### INPUT DATA
        User Complaint: "{complaint_text}"
        Risk Score: {risk_score}
        Draft Response: "{draft_response}"
        
        ### INSTRUCTION
        Review the draft now. Provide JSON output.
        """

        # Enforce JSON mode for reliable parsing
        response = self.model.generate_content(
            [self.system_prompt, user_prompt],
            generation_config=GenerationConfig(
                response_mime_type="application/json",
                temperature=0.2  # Low temperature for consistent evaluation
            )
        )

        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            # Fallback if model hallucinates format
            return {"verdict": "FAIL", "feedback": "JSON parsing error in Critic Agent"}

# --- Usage Example ---
if __name__ == "__main__":
    critic = CriticAgent()
    
    # Scenario: Furious user, but draft is too happy
    complaint = "You double charged me! I want my money back NOW!"
    bad_draft = "Hey there! We are super excited to help you with your billing!"
    
    result = critic.review_draft(complaint, 90, bad_draft)
    print(json.dumps(result, indent=2))