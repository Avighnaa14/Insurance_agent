from sqlalchemy import Column, Integer, String, JSON
from database import Base

class HandoffTicket(Base):
    __tablename__ = "handoff_tickets"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, unique=True, index=True)
    customer_name = Column(String)
    phone = Column(String)
    reason = Column(String)

class QuoteHistory(Base):
    __tablename__ = "quote_history"
    id = Column(Integer, primary_key=True, index=True)
    customer_profile = Column(JSON)
    recommended_policies = Column(JSON)

class ConversationSummary(Base):
    __tablename__ = "conversation_summaries"
    id = Column(Integer, primary_key=True, index=True)
    profile = Column(JSON)
    selected_policy = Column(String)
    summary_text = Column(String)
