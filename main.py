from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
import random

app = FastAPI(title="Insurance Bot APIs")

# -------------------------------------------------------------------
# MOCK CATALOG: 24 Policies (6 Health, 6 Life, 6 Term, 6 Motor)
# -------------------------------------------------------------------
POLICIES = [
    # ---------------- HEALTH (6) ----------------
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
    {
        "policy_id": "HLT_ADV_002",
        "name": "Health Plus Advanced",
        "type": "health",
        "sum_insured": [500000, 1000000],
        "premium_yearly": {"500000": 15000, "1000000": 20000},
        "eligibility": {"min_age": 25, "max_age": 65},
        "waiting_period_days": 45,
        "exclusions": ["dental procedures", "pre-existing for 36 months"],
        "riders": [{"id": "CRIT_CARE", "name": "Critical Illness", "premium": 2500}]
    },
    {
        "policy_id": "HLT_FAM_003",
        "name": "Family Health Protect",
        "type": "health",
        "sum_insured": [500000, 750000, 1000000],
        "premium_yearly": {"500000": 18000, "750000": 22000, "1000000": 26000},
        "eligibility": {"min_age": 18, "max_age": 60},
        "waiting_period_days": 30,
        "exclusions": ["pre-existing for 36 months"],
        "riders": [{"id": "MAT_COV", "name": "Maternity Cover", "premium": 3000}]
    },
    {
        "policy_id": "HLT_PREM_004",
        "name": "Health Premium Care",
        "type": "health",
        "sum_insured": [1000000, 1500000],
        "premium_yearly": {"1000000": 32000, "1500000": 42000},
        "eligibility": {"min_age": 21, "max_age": 70},
        "waiting_period_days": 60,
        "exclusions": ["cosmetic procedures"],
        "riders": [{"id": "WELLNESS", "name": "Wellness Program", "premium": 1500}]
    },
    {
        "policy_id": "HLT_SENIOR_005",
        "name": "Senior Health Secure",
        "type": "health",
        "sum_insured": [200000, 500000],
        "premium_yearly": {"200000": 12000, "500000": 25000},
        "eligibility": {"min_age": 60, "max_age": 80},
        "waiting_period_days": 60,
        "exclusions": ["pre-existing for 48 months"],
        "riders": [{"id": "HOS_CASH", "name": "Hospital Cash", "premium": 2500}]
    },
    {
        "policy_id": "HLT_TOPUP_006",
        "name": "Health Top-up Saver",
        "type": "health",
        "sum_insured": [500000, 1000000],
        "premium_yearly": {"500000": 6000, "1000000": 10000},
        "eligibility": {"min_age": 18, "max_age": 65},
        "waiting_period_days": 30,
        "exclusions": ["cosmetic procedures"],
        "riders": []
    },

    # ---------------- LIFE (6) ----------------
    {
        "policy_id": "LIFE_WHOLE_001",
        "name": "Whole Life Protect",
        "type": "life",
        "sum_insured": [1000000, 2000000],
        "premium_yearly": {"1000000": 25000, "2000000": 45000},
        "eligibility": {"min_age": 18, "max_age": 55},
        "waiting_period_days": 90,
        "exclusions": ["suicide within 1 year"],
        "riders": [{"id": "CRIT_CARE", "name": "Critical Illness", "premium": 3500}]
    },
    {
        "policy_id": "LIFE_ENDOW_002",
        "name": "Endowment Plus",
        "type": "life",
        "sum_insured": [500000, 1000000],
        "premium_yearly": {"500000": 20000, "1000000": 35000},
        "eligibility": {"min_age": 21, "max_age": 50},
        "waiting_period_days": 60,
        "exclusions": [],
        "riders": [{"id": "ACC_DEATH", "name": "Accidental Death", "premium": 2500}]
    },
    {
        "policy_id": "LIFE_ULIP_003",
        "name": "Wealth Builder ULIP",
        "type": "life",
        "sum_insured": [2000000, 5000000],
        "premium_yearly": {"2000000": 40000, "5000000": 90000},
        "eligibility": {"min_age": 25, "max_age": 55},
        "waiting_period_days": 0,
        "exclusions": ["market risk disclaimer"],
        "riders": []
    },
    {
        "policy_id": "LIFE_CHILD_004",
        "name": "Child Future Plan",
        "type": "life",
        "sum_insured": [500000, 1000000],
        "premium_yearly": {"500000": 15000, "1000000": 28000},
        "eligibility": {"min_age": 18, "max_age": 50},
        "waiting_period_days": 30,
        "exclusions": [],
        "riders": [{"id": "EDU_RIDER", "name": "Education Rider", "premium": 3000}]
    },
    {
        "policy_id": "LIFE_RETIRE_005",
        "name": "Retirement Secure",
        "type": "life",
        "sum_insured": [1000000, 3000000],
        "premium_yearly": {"1000000": 22000, "3000000": 55000},
        "eligibility": {"min_age": 30, "max_age": 60},
        "waiting_period_days": 0,
        "exclusions": [],
        "riders": [{"id": "PENSION_BOOST", "name": "Pension Booster", "premium": 4000}]
    },
    {
        "policy_id": "LIFE_MONEYBACK_006",
        "name": "Money Back Saver",
        "type": "life",
        "sum_insured": [500000, 1500000],
        "premium_yearly": {"500000": 18000, "1500000": 38000},
        "eligibility": {"min_age": 21, "max_age": 55},
        "waiting_period_days": 30,
        "exclusions": [],
        "riders": []
    },

    # ---------------- TERM (6) ----------------
    {
        "policy_id": "TERM_BASIC_001",
        "name": "Term Secure Basic",
        "type": "term",
        "sum_insured": [2000000, 5000000],
        "premium_yearly": {"2000000": 6000, "5000000": 14000},
        "eligibility": {"min_age": 18, "max_age": 60},
        "waiting_period_days": 0,
        "exclusions": ["suicide within 1 year"],
        "riders": []
    },
    {
        "policy_id": "TERM_PLUS_002",
        "name": "Term Protect Plus",
        "type": "term",
        "sum_insured": [5000000, 10000000],
        "premium_yearly": {"5000000": 12000, "10000000": 22000},
        "eligibility": {"min_age": 21, "max_age": 60},
        "waiting_period_days": 0,
        "exclusions": [],
        "riders": [{"id": "ACC_DEATH", "name": "Accidental Death Benefit", "premium": 1500}]
    },
    {
        "policy_id": "TERM_PREMIUM_003",
        "name": "Term Premium Guard",
        "type": "term",
        "sum_insured": [10000000, 20000000],
        "premium_yearly": {"10000000": 25000, "20000000": 48000},
        "eligibility": {"min_age": 25, "max_age": 55},
        "waiting_period_days": 0,
        "exclusions": [],
        "riders": [{"id": "DISABILITY", "name": "Disability Cover", "premium": 3000}]
    },
    {
        "policy_id": "TERM_RETURN_004",
        "name": "Return of Premium Term",
        "type": "term",
        "sum_insured": [1000000, 3000000],
        "premium_yearly": {"1000000": 20000, "3000000": 45000},
        "eligibility": {"min_age": 21, "max_age": 55},
        "waiting_period_days": 0,
        "exclusions": [],
        "riders": []
    },
    {
        "policy_id": "TERM_SMOKER_005",
        "name": "Term Special (Smokers)",
        "type": "term",
        "sum_insured": [5000000],
        "premium_yearly": {"5000000": 30000},
        "eligibility": {"min_age": 25, "max_age": 55},
        "waiting_period_days": 0,
        "exclusions": [],
        "riders": []
    },
    {
        "policy_id": "TERM_FAM_006",
        "name": "Family Term Care",
        "type": "term",
        "sum_insured": [5000000, 10000000],
        "premium_yearly": {"5000000": 18000, "10000000": 32000},
        "eligibility": {"min_age": 21, "max_age": 60},
        "waiting_period_days": 0,
        "exclusions": [],
        "riders": []
    },

    # ---------------- MOTOR (6) ----------------
    {
        "policy_id": "MOT_BASIC_001",
        "name": "Motor Protect Basic",
        "type": "motor",
        "sum_insured": [200000, 500000],
        "premium_yearly": {"200000": 3000, "500000": 5000},
        "eligibility": {"min_age": 18, "max_age": 70},
        "waiting_period_days": 0,
        "exclusions": ["drunk driving", "racing"],
        "riders": []
    },
    {
        "policy_id": "MOT_COMP_002",
        "name": "Motor Protect Comprehensive",
        "type": "motor",
        "sum_insured": [500000, 1000000],
        "premium_yearly": {"500000": 8000, "1000000": 12000},
        "eligibility": {"min_age": 18, "max_age": 70},
        "waiting_period_days": 0,
        "exclusions": ["commercial use not covered"],
        "riders": [{"id": "ROADSIDE", "name": "Roadside Assistance", "premium": 1000}]
    },
    {
        "policy_id": "MOT_PLUS_003",
        "name": "Motor Protect Plus",
        "type": "motor",
        "sum_insured": [750000, 1500000],
        "premium_yearly": {"750000": 10000, "1500000": 15000},
        "eligibility": {"min_age": 18, "max_age": 70},
        "waiting_period_days": 0,
        "exclusions": [],
        "riders": [{"id": "PA_COV", "name": "Personal Accident Cover", "premium": 2000}]
    },
    {
        "policy_id": "MOT_PREM_004",
        "name": "Motor Protect Premium",
        "type": "motor",
        "sum_insured": [1000000, 2000000],
        "premium_yearly": {"1000000": 18000, "2000000": 25000},
        "eligibility": {"min_age": 18, "max_age": 70},
        "waiting_period_days": 0,
        "exclusions": [],
        "riders": [{"id": "ZERO_DEP", "name": "Zero Depreciation", "premium": 3000}]
    },
    {
        "policy_id": "MOT_ZERO_005",
        "name": "Motor Protect Zero Depreciation",
        "type": "motor",
        "sum_insured": [1000000, 2000000],
        "premium_yearly": {"1000000": 20000, "2000000": 30000},
        "eligibility": {"min_age": 18, "max_age": 70},
        "waiting_period_days": 0,
        "exclusions": [],
        "riders": [{"id": "ENGINE_PRO", "name": "Engine Protection", "premium": 2500}]
    },
    {
        "policy_id": "MOT_EV_006",
        "name": "Motor Protect Electric Vehicle",
        "type": "motor",
        "sum_insured": [500000, 1500000],
        "premium_yearly": {"500000": 10000, "1500000": 16000},
        "eligibility": {"min_age": 18, "max_age": 70},
        "waiting_period_days": 0,
        "exclusions": [],
        "riders": [{"id": "BAT_COV", "name": "Battery Cover", "premium": 3000}]
    }
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
def get_quote(request: QuoteRequest):
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
    return {"recommended_plans": response}

@app.post("/handoff")
def create_handoff(request: HandoffRequest):
    """Creates a callback/live transfer ticket"""
    ticket_id = f"TICKET_{random.randint(1000,9999)}"
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
def conversation_summary(request: SummaryRequest):
    """Summarize customer profile and selected policy"""
    policy = next((p for p in POLICIES if p["policy_id"] == request.selected_policy), None)
    return {
        "profile": request.profile,
        "selected_policy": policy if policy else "Not found",
        "disclaimer": "This is a mock recommendation. I do not provide legal/tax advice. Returns are guaranteed only if explicitly stated."
    }
@app.get("/")
def root():
    return {"message": "Welcome to Insurance Bot API! Go to /docs for API details."}
