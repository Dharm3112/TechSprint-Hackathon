from coordinator import CoordinatorAgent
import sys
import time

# Force UTF-8 for Windows Console
sys.stdout.reconfigure(encoding='utf-8')

def run_demo():
    print("🚀 Starting Customer Complaint Resolver AI Agent...")
    print("Initializing Agent Swarm...")
    
    try:
        # Wrap initialization in try/except to see why it crashes
        coordinator = CoordinatorAgent()
    except Exception as e:
        print(f"\n❌ FATAL ERROR during Initialization: {e}")
        import traceback
        traceback.print_exc()
        return  # Stop execution

    print("\n✅ System Ready.")
    
    mode = input("\nChoose Mode:\n1. Run Demo Batch\n2. Interactive Chat\nEnter choice (1/2): ")
    
    if mode.strip() == "2":
        print("\n💬 Interactive Mode Enabled. Type 'exit' to quit.\n")
        while True:
            user_input = input("\nCustomer: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            
            try:
                ticket = coordinator.process_complaint(user_input, "INTERACTIVE-USER")
                response_text = "No response generated."
                if ticket.response:
                    # Handle both dict and object for safety
                    if isinstance(ticket.response, dict):
                        response_text = ticket.response.get('draft_content', 'No content')
                    else:
                        response_text = ticket.response.draft_content
                
                print(f"\n🤖 Agent: {response_text}")
                time.sleep(2) # Rate limit safety
            except Exception as e:
                print(f"❌ Error: {e}")
                
    else:
        print("\nRunning Test Batch...\n")
        # Sample Test Cases
        test_cases = [
            # Case 1: Simple Inquiry
            "I was charged twice for my subscription this month. Can you please check and refund the extra amount?",
            
            # Case 2: High Urgency / Risk
            "Your product caught fire and burned my kitchen table! I am calling my lawyer and the press if you don't fix this immediately.",
            
            # Case 3: Confused / Tech Support
            "I can't find the login button on the new update. It's very confusing.",
        ]
        
        for i, complaint in enumerate(test_cases, 1):
            print(f"\n{'='*20} CASE {i} {'='*20}")
            try:
                coordinator.process_complaint(complaint, f"CUST-{100+i}")
                time.sleep(1) # Pause for readability
            except Exception as e:
                print(f"❌ Error processing case {i}: {e}")
                import traceback
                traceback.print_exc()

    print("\n\n🎉 Session Complete.")

if __name__ == "__main__":
    run_demo()
