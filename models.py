from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from enum import Enum
import uuid
from datetime import datetime

# Enums for consistent classification
class Category(str, Enum):
    BILLING = "Billing"
    SERVICE = "Service"
    PRODUCT = "Product"
    COMPLIANCE = "Compliance"
    SAFETY = "Safety"
    OTHER = "Other"

class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class ActionType(str, Enum):
    REPLY = "Reply"
    ESCALATE = "Escalate"
    REFUND = "Refund"
    INVESTIGATE = "Investigate"

# 1. Raw Input
class Complaint(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    customer_id: str
    text: str
    source: str = "Unknown"
    timestamp: datetime = Field(default_factory=datetime.now)

# 2. Agent Analysis Output
class Analysis(BaseModel):
    intent: str
    category: Category
    sentiment_score: float = Field(..., description="Score between -1.0 (negative) and 1.0 (positive)")
    urgency_score: int = Field(..., description="Score between 1 (low) and 10 (critical)")
    key_entities: List[str] = []
    is_recurring: bool = False

# 3. Prioritization Output
class Priority(BaseModel):
    score: int = Field(..., description="Calculated priority score 0-100")
    risk_level: RiskLevel
    reasoning: str

# 4. Decision/Action
class Decision(BaseModel):
    action: ActionType
    suggested_response_tone: str
    requires_human_approval: bool
    reasoning: str

# 5. Final Response Draft
class Response(BaseModel):
    ticket_id: str
    draft_content: str
    tone_used: str
    confidence_score: float

# 6. Full Ticket State (Memory Object)
class ComplaintTicket(BaseModel):
    complaint: Complaint
    analysis: Optional[Analysis] = None
    priority: Optional[Priority] = None
    decision: Optional[Decision] = None
    response: Optional[Response] = None
    status: str = "Open"
    history: List[str] = [] # Audit log of agent actions
