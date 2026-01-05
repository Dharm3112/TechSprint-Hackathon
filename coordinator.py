from agents.classification_agent import ClassificationAgent
from agents.sentiment_agent import SentimentAgent
from agents.prioritization_agent import PrioritizationAgent
from agents.decision_agent import DecisionAgent
from agents.response_agent import ResponseDraftingAgent
from memory.vector_db import MemoryAgent
from models import Complaint, ComplaintTicket
import uuid
import datetime

class CoordinatorAgent:
    def __init__(self):
        # Initialize the swarm
        self.classifier = ClassificationAgent()
        self.sentiment_analyzer = SentimentAgent()
        self.prioritizer = PrioritizationAgent()
        self.decision_maker = DecisionAgent()
        self.drafter = ResponseDraftingAgent()
        self.memory = MemoryAgent()
        
    def process_complaint(self, text: str, customer_id: str = "Unknown") -> ComplaintTicket:
        print(f"\n--- Processing Complaint: {text[:50]}... ---")
        
        # 0. Create Ticket Object
        ticket = ComplaintTicket(
            complaint=Complaint(
                customer_id=customer_id,
                text=text
            )
        )
        ticket.history.append("Ticket Created")

        # 1. Memory Check (RAG)
        print("🧠 Checking Memory...")
        similar_cases = self.memory.search_similar(text)
        ticket.history.append(f"Memory Accessed: {similar_cases[:30]}...")

        # 2. Parallel Analysis (Classification & Sentiment)
        print("🔍 Analyzing Content...")
        classification = self.classifier.analyze(text)
        sentiment = self.sentiment_analyzer.analyze(text)
        
        # Merge Analysis
        ticket.analysis = {**classification, **sentiment}
        ticket.history.append(f"Analysis Complete: {ticket.analysis['intent']}, Urgency: {ticket.analysis['urgency_score']}")

        # 3. Prioritization
        print("⚖️ Prioritizing...")
        ticket.priority = self.prioritizer.assess(ticket.analysis)
        ticket.history.append(f"Priority Set: {ticket.priority['score']}, Risk: {ticket.priority['risk_level']}")

        # 4. Decision Making
        print("🤔 Deciding Action...")
        decision_input = {
            "text": text,
            "analysis": ticket.analysis,
            "priority": ticket.priority,
            "history": similar_cases
        }
        ticket.decision = self.decision_maker.decide(text, ticket.analysis, ticket.priority, similar_cases)
        ticket.history.append(f"Decision Made: {ticket.decision['action']}")

        # 5. Drafting Response (if applicable)
        if ticket.decision['action'] in ["Reply", "Escalate", "Refund"]: # Draft even for escalation
            print("✍️ Drafting Response...")
            ticket.response = self.drafter.draft(text, ticket.decision, similar_cases)
            ticket.history.append("Response Drafted")
            
            # 6. Re-Evaluation (Self-Correction Loop)
            # If the response confidence is low or urgency is high, we might want to flag it or adjust
            if ticket.response['confidence_score'] < 0.7:
                 print("⚠️ Low Confidence Response - Flagging for Human Review")
                 ticket.decision['requires_human_approval'] = True
                 ticket.history.append("Flagged for Human Review (Low Confidence)")

        # 7. Close Loop (Save to Memory if resolved/replied) -> In a real app this happens after human approval
        # For this demo we save processed tickets to build history
        self.memory.save_complaint(
            ticket.complaint.id, 
            text, 
            ticket.decision['action'], 
            {"category": ticket.analysis['category']}
        )
        
        return ticket
