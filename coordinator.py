from agents.classification_agent import ClassificationAgent
from agents.sentiment_agent import SentimentAgent
from agents.prioritization_agent import PrioritizationAgent
from agents.decision_agent import DecisionAgent
from agents.response_agent import ResponseDraftingAgent
from agents.critic import CriticAgent  # <--- IMPORT THE CRITIC
from memory.vector_db import MemoryAgent
from models import Complaint, ComplaintTicket
import sys

class CoordinatorAgent:
    def __init__(self):
        # Initialize the Novus Swarm
        self.classifier = ClassificationAgent()
        self.sentiment_analyzer = SentimentAgent()
        self.prioritizer = PrioritizationAgent()
        self.decision_maker = DecisionAgent()
        self.drafter = ResponseDraftingAgent()
        self.critic = CriticAgent()  # <--- INITIALIZE CRITIC
        self.memory = MemoryAgent()
        
    def process_complaint(self, text: str, customer_id: str = "Unknown") -> ComplaintTicket:
        print(f"\n--- 🔵 Novus Agent Processing: {text[:40]}... ---")
        
        ticket = ComplaintTicket(complaint=Complaint(customer_id=customer_id, text=text))

        # 1. Understand (Parallel Analysis)
        print("🔍 Novus: Analyzing Intent & Sentiment...")
        classification = self.classifier.analyze(text)
        sentiment = self.sentiment_analyzer.analyze(text)
        ticket.analysis = {**classification, **sentiment}
        
        # 2. Recall (Memory)
        print("🧠 Novus: Checking History...")
        similar_cases = self.memory.search_similar(text)

        # 3. Rank (Prioritization)
        ticket.priority = self.prioritizer.assess(ticket.analysis)
        print(f"⚖️ Novus: Priority Set to {ticket.priority['score']} (Risk: {ticket.priority['risk_level']})")
        
        # 4. Decide (Strategy)
        ticket.decision = self.decision_maker.decide(text, ticket.analysis, ticket.priority, similar_cases)

        # 5. Act & Refine (The Feedback Loop)
        if ticket.decision['action'] in ["Reply", "Escalate", "Refund"]:
            print("✍️ Novus: Drafting Initial Response...")
            
            # Initial Draft
            draft = self.drafter.draft(text, ticket.decision, similar_cases)
            
            # --- CRITIC LOOP ---
            max_retries = 2
            attempts = 0
            
            while attempts < max_retries:
                print(f"   🕵️ Novus Critic: Reviewing Draft (Attempt {attempts+1})...")
                critique = self.critic.review(
                    text, 
                    draft['draft_content'], 
                    ticket.analysis['urgency_score']
                )
                
                if critique['status'] == "PASS":
                    print("   ✅ Novus Critic: Approved.")
                    break
                else:
                    print(f"   ❌ Novus Critic: Rejected. Feedback: '{critique['feedback']}'")
                    print("   🔄 Novus Drafter: Rewriting...")
                    # Pass feedback back to drafter
                    draft = self.drafter.draft(
                        text, 
                        ticket.decision, 
                        similar_cases, 
                        feedback=critique['feedback']
                    )
                    attempts += 1
            
            ticket.response = draft
            
            # Final Safety Catch
            if critique.get('escalation_needed'):
                print("🚨 Novus Safety Protocol: Force Escalate triggered by Critic.")
                ticket.decision['action'] = "Escalate (Forced)"

        # 6. Memorize
        print("💾 Novus: Saving Resolution to Memory...")
        self.memory.save_complaint(
            ticket.complaint.id, 
            text, 
            ticket.decision['action'], 
            {"category": ticket.analysis['category']}
        )
        
        return ticket