from pydantic import BaseModel
from typing import Optional

class AngleSignals(BaseModel):
    delivery_pressure: str
    product_complexity: str
    team_structure: str
    engineering_maturity: str
    decision_maker_level: str
    execution_noise_level: str
    multi_team_coordination: str
    organizational_stage_signal: str

class NormalizedLead(BaseModel):
    first_name: str
    last_name: str
    role_title: Optional[str] = None
    role_seniority: Optional[str] = None
    role_category: Optional[str] = None
    company: str
    company_size: Optional[int] = None
    company_stage: Optional[str] = None
    industry: Optional[str] = None
    company_category: Optional[str] = None
    linkedin_url: Optional[str] = None
    website_url: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    
    # Phase 5.5: New Enrichment Fields
    product_type: Optional[str] = None
    business_model: Optional[str] = None
    signal_count: Optional[int] = 0

    # NEW: Angle Signals
    angle_signals: AngleSignals

class EmailOutput(BaseModel):
    subject: str
    body: str
    angle_used: str
    tokens: int

    def to_dict(self):
        return {
            "subject": self.subject,
            "body": self.body,
            "angle_used": self.angle_used,
            "tokens": self.tokens,
            "email": f"Subject: {self.subject}\n\n{self.body}"
        }

    def dict(self, *args, **kwargs):
        return self.to_dict()
