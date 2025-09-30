from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
import random
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import HandoffTicket, QuoteHistory, ConversationSummary

# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Insurance Bot APIs")

# -------------------------------------------------------------------
# MOCK CATALOG: 24 Policies (6 Health, 6 Life, 6 Term, 6 Motor)
# -------------------------------------------------------------------
POLICIES = [
    {
        "policy_id": "HLT_BASIC_001",
        "name": "Health Shield Basic",
        "type": "health",
        "sum_insured": [300000, 500000, 700000],
        "premium_yearly": {"300000": 8500, "500000": 11000, "700000": 14500},
        "eligibility": {"min_age": 18, "max_age": 65},
        "waiting_period_days": 30,
        "exclusions": ["cosmetic procedures", "pre-existing for 24 months"],
        "riders": [{"id": "HOS_CASH", "name": "Hospital Cash", "premium": 1200}]
    },
    # (⚡ Keep the rest of your 23 policies here)
]

# -------------------------------------------------------------------
# REQUEST MODELS
# -------------------------------------------------------------------
class QuoteRequest(BaseModel):
    age_band: str
    dependents: int
    annual_income_band: str
    existing_cover: str
    risk_tolerance: str
    preferred_premium_band: str

class HandoffRequest(BaseModel):
    name: str
    phone: str
    reason: str

class AddRiderRequest(BaseModel):
    policy_id: str
    rider_id: str

class CompareRequest(BaseModel):
    policy_ids: List[str]

class SummaryRequest(BaseModel):
    profile: Dict[str, Any]
    selected_policy: str

# -------------------------------------------------------------------
# API ENDPOINTS
# -------------------------------------------------------------------

@app.get("/policies")
def get_policies():
    """Returns all available mock policies"""
    return {"policies": POLICIES}


@app.post("/quote")
def get_quote(request: QuoteRequest, db: Session = Depends(get_db)):
    """Returns top 3 recommended policies"""
    recommended = random.sample(POLICIES, 3)
    response = []
    for policy in recommended:
        premium = list(policy["premium_yearly"].values())[0]
        reason = f"Fits {request.age_band} with {request.dependents} dependents and {request.risk_tolerance} risk profile"
        response.append({
            "policy_id": policy["policy_id"],
            "name": policy["name"],
            "sum_insured": list(policy["premium_yearly"].keys())[0],
            "premium": premium,
            "reason": reason
        })

    # Save in DB
    history = QuoteHistory(
        customer_profile=request.dict(),
        recommended_policies=response
    )
    db.add(history)
    db.commit()

    return {"recommended_plans": response}


@app.post("/handoff")
def create_handoff(request: HandoffRequest, db: Session = Depends(get_db)):
    """Creates a callback/live transfer ticket"""
    ticket_id = f"TICKET_{random.randint(1000,9999)}"

    # Save in DB
    ticket = HandoffTicket(
        ticket_id=ticket_id,
        customer_name=request.name,
        phone=request.phone,
        reason=request.reason
    )
    db.add(ticket)
    db.commit()

    return {
        "status": "handoff_created",
        "ticket_id": ticket_id,
        "assigned_to": "Human Agent",
        "customer": {"name": request.name, "phone": request.phone},
        "reason": request.reason
    }


@app.post("/add_rider")
def add_rider(request: AddRiderRequest):
    """Adds a rider to a chosen policy"""
    for policy in POLICIES:
        if policy["policy_id"] == request.policy_id:
            for rider in policy["riders"]:
                if rider["id"] == request.rider_id:
                    return {"status": "success", "policy": policy["name"], "rider_added": rider}
            return {"status": "failed", "message": "Rider not found"}
    return {"status": "failed", "message": "Policy not found"}


@app.post("/compare")
def compare_policies(request: CompareRequest):
    """Compare selected policies side by side"""
    compared = [p for p in POLICIES if p["policy_id"] in request.policy_ids]
    return {"comparison": compared}


@app.post("/summary")
def conversation_summary(request: SummaryRequest, db: Session = Depends(get_db)):
    """Summarize customer profile and selected policy"""
    policy = next((p for p in POLICIES if p["policy_id"] == request.selected_policy), None)

    summary = ConversationSummary(
        profile=request.profile,
        selected_policy=request.selected_policy,
        disclaimer="This is a mock recommendation. I do not provide legal/tax advice."
    )
    db.add(summary)
    db.commit()

    return {
        "profile": request.profile,
        "selected_policy": policy if policy else "Not found",
        "disclaimer": "This is a mock recommendation. I do not provide legal/tax advice."
    }


@app.get("/")
def root():
    return {"message": "Welcome to Insurance Bot API! Go to /docs for API details."}
