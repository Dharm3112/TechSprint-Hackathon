from google.adk.agents import Agent
from coordinator import CoordinatorAgent
from dotenv import load_dotenv
import os

# 1. LOAD API KEYS (Crucial for ADK Web)
load_dotenv() 

# 2. Initialize the Brain
print("🔌 Initializing Sentinel Coordinator...")
try:
    sentinel_system = CoordinatorAgent()
except Exception as e:
    print(f"❌ CRITICAL ERROR: Coordinator failed to start. Check config.py! Error: {e}")
    sentinel_system = None

# 3. Define the Tool
def solve_complaint(complaint_text: str) -> dict:
    """
    Analyzes a customer complaint and drafts a response using the Sentinel System.
    
    Args:
        complaint_text: The full text of the customer's issue.
    """
    print(f"⚡ ADK Processing: {complaint_text}")
    
    if not sentinel_system:
        return {"error": "System failed to initialize. Check terminal logs."}

    try:
        # Run the pipeline
        ticket = sentinel_system.process_complaint(complaint_text, "ADK-USER")
        
        return {
            "status": "SUCCESS",
            "priority_score": ticket.priority.score,
            "risk_level": ticket.priority.risk_level.value,
            "suggested_action": ticket.decision.action.value,
            "draft_response": ticket.response.draft_content if ticket.response else "No response required."
        }
    except Exception as e:
        return {"error": f"Processing failed: {str(e)}"}

# 4. Define the ADK Agent
agent = Agent(
    name="Novus",
    # MUST MATCH config.py model
    model="gemini-2.5-flash-tts",
    description="Customer Complaint Resolver Agent",
    instruction="""
    You are the interface for the Novus.
    
    Your ONLY goal is to help users by using the 'solve_complaint' tool.
    
    RULES:
    1. When the user types ANYTHING, immediately call 'solve_complaint'.
    2. Do not answer from your own knowledge.
    3. Once the tool finishes, show the 'draft_response' to the user.
    """,
    tools=[solve_complaint]
)