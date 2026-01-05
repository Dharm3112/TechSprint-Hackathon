from agents.classification_agent import ClassificationAgent
from agents.sentiment_agent import SentimentAgent
from agents.prioritization_agent import PrioritizationAgent
from agents.decision_agent import DecisionAgent
from agents.response_agent import ResponseDraftingAgent
from memory.vector_db import MemoryAgent
from models import Complaint, ComplaintTicket, Analysis, Priority, Decision, Response, Category, RiskLevel, ActionType
import datetime

class CoordinatorAgent:
    def __init__(self):
        print("   [Coordinator] Initializing agents...")
        self.classifier = ClassificationAgent()
        self.sentiment_analyzer = SentimentAgent()
        self.prioritizer = PrioritizationAgent()
        self.decision_maker = DecisionAgent()
        self.drafter = ResponseDraftingAgent()
        self.memory = MemoryAgent()
        
    def process_complaint(self, text: str, customer_id: str = "Unknown") -> ComplaintTicket:
        print(f"\n--- Processing: {text[:40]}... ---")
        
        # 0. Create Ticket
        ticket = ComplaintTicket(complaint=Complaint(customer_id=customer_id, text=text))
        ticket.history.append("Ticket Created")

        # 1. Memory Search
        print("🧠 Checking Memory...")
        similar_cases = self.memory.search_similar(text)

        # 2. Analysis (Classification + Sentiment)
        print("🔍 Analyzing...")
        cls_data = self.classifier.analyze(text)
        sent_data = self.sentiment_analyzer.analyze(text)
        
        # --- SAFE DATA CONVERSION (Prevents Crashes) ---
        category_str = cls_data.get("category", "Other")
        safe_category = next((c for c in Category if c.value.lower() == category_str.lower()), Category.OTHER)

        ticket.analysis = Analysis(
            intent=cls_data.get("intent", "Unknown"),
            category=safe_category,
            key_entities=cls_data.get("key_entities", []),
            sentiment_score=sent_data.get("sentiment_score", 0.0),
            urgency_score=sent_data.get("urgency_score", 5)
        )

        # 3. Prioritization
        print(f"⚖️ Prioritizing (Urgency: {ticket.analysis.urgency_score})...")
        analysis_dict = ticket.analysis.model_dump() 
        pri_data = self.prioritizer.assess(analysis_dict)
        
        risk_str = pri_data.get("risk_level", "Medium")
        safe_risk = next((r for r in RiskLevel if r.value.lower() == risk_str.lower()), RiskLevel.MEDIUM)

        ticket.priority = Priority(
            score=pri_data.get("score", 50),
            risk_level=safe_risk,
            reasoning=pri_data.get("reasoning", "None")
        )

        # 4. Decision
        print("🤔 Deciding next steps...")
        dec_data = self.decision_maker.decide(
            text, 
            analysis_dict, 
            ticket.priority.model_dump(), 
            similar_cases
        )
        
        action_str = dec_data.get("action", "Reply")
        safe_action = next((a for a in ActionType if a.value.lower() == action_str.lower()), ActionType.REPLY)

        ticket.decision = Decision(
            action=safe_action,
            suggested_response_tone=dec_data.get("suggested_response_tone", "Professional"),
            requires_human_approval=dec_data.get("requires_human_approval", False),
            reasoning=dec_data.get("reasoning", "None")
        )

        # 5. Drafting (Only if Reply/Escalate/Refund)
        if ticket.decision.action in [ActionType.REPLY, ActionType.ESCALATE, ActionType.REFUND]: 
            print("✍️ Drafting Response...")
            resp_data = self.drafter.draft(text, ticket.decision.model_dump(), similar_cases)
            
            ticket.response = Response(
                ticket_id=ticket.complaint.id,
                draft_content=resp_data.get("draft_content", ""),
                tone_used=resp_data.get("tone_used", "Neutral"),
                confidence_score=resp_data.get("confidence_score", 1.0)
            )
            print(f"   -> Draft generated (Confidence: {ticket.response.confidence_score})")

        # 6. Save to Memory
        self.memory.save_complaint(
            ticket.complaint.id, 
            text, 
            ticket.decision.action.value, 
            {"category": ticket.analysis.category.value}
        )
        
        return ticket