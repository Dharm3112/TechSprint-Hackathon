from coordinator import CoordinatorAgent
import sys
import time

# Force UTF-8 for Windows Console
sys.stdout.reconfigure(encoding='utf-8')

def run_demo():
    print("🚀 Starting Customer Complaint Resolver AI Agent...")
    print("Initializing Agent Swarm...")
    
    coordinator = CoordinatorAgent()
    
    # Sample Test Cases
    test_cases = [
        # Case 1: Simple Inquiry
        "I was charged twice for my subscription this month. Can you please check and refund the extra amount?",
        
        # Case 2: High Urgency / Risk
        "Your product caught fire and burned my kitchen table! I am calling my lawyer and the press if you don't fix this immediately.",
        
        # Case 3: Confused / Tech Support
        "I can't find the login button on the new update. It's very confusing.",
    ]
    
    print("\n✅ System Ready. Running Test Batch...\n")
    
    for i, complaint in enumerate(test_cases, 1):
        print(f"\n{'='*20} CASE {i} {'='*20}")
        try:
            coordinator.process_complaint(complaint, f"CUST-{100+i}")
            time.sleep(1) # Pause for readability
        except Exception as e:
            print(f"❌ Error processing case {i}: {e}")
            import traceback
            traceback.print_exc()

    print("\n\n🎉 Demo Complete.")

if __name__ == "__main__":
    run_demo()
