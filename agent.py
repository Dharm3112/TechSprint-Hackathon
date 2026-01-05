from google.adk.agents import Agent
from coordinator import CoordinatorAgent

# 1. Initialize your Sentinel Brain
# We create one instance so it keeps memory between chats
sentinel = CoordinatorAgent()

# 2. Define the Tool Function
# This function acts as the "API" that ADK calls
def resolve_complaint_tool(complaint_text: str) -> dict:
    """
    Analyzes a customer complaint, calculates risk, and drafts a response.
    
    Args:
        complaint_text: The full text of the customer's issue.
    """
    print(f"🔌 ADK is processing: {complaint_text[:20]}...")
    
    # Call your existing logic
    ticket = sentinel.process_complaint(complaint_text, "ADK-WEB-USER")
    
    # Format the output for the Web UI
    result = {
        "status": "SUCCESS",
        "risk_level": ticket.priority.risk_level.value,
        "priority_score": ticket.priority.score,
        "suggested_action": ticket.decision.action.value,
        "draft_response": "NO RESPONSE"
    }
    
    if ticket.response:
        result["draft_response"] = ticket.response.draft_content
        
    return result

# 3. Define the ADK Agent
# This is the object 'adk web' will actually load
agent = Agent(
    name="sentinel_resolver",
    # Use the model you configured in config.py or a standard one
    model="gemini-1.5-flash-001", 
    description="An enterprise-grade customer complaint resolution agent.",
    instruction="""
    You are the interface for the Sentinel Complaint System.
    
    Your goal is to help users resolve complaints by using the 'resolve_complaint_tool'.
    
    1. When the user provides a complaint, IMMEDIATELY call 'resolve_complaint_tool'.
    2. Do not try to answer it yourself. Use the tool.
    3. Once the tool returns the 'draft_response', display it clearly to the user.
    """,
    tools=[resolve_complaint_tool]
)