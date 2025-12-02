"""
CSE Schema Module
Defines mandatory raw fields each agent MUST output.
Enforces "Fail Fast" validation.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict

# ===== AGENT OUTPUT SCHEMAS =====

class BrightDataOutput(BaseModel):
    """Raw output from BrightDataEnrichmentAgent"""
    raw_description: Optional[str] = None
    raw_headcount: Optional[int] = None
    raw_headcount_history: Optional[List[int]] = None
    raw_open_roles: Optional[int] = None
    raw_industry: Optional[str] = None
    raw_tech_stack: Optional[List[str]] = None
    raw_org_structure: Optional[Dict] = None

class AngleRouterOutput(BaseModel):
    """Raw output from AngleRouter"""
    candidate_angles: List[str] = Field(default_factory=list)
    rejected_angles: List[str] = Field(default_factory=list)
    raw_patterns: Optional[Dict] = None
    selected_angle: Optional[str] = None  # Final choice for backward compat

class PainProfilerOutput(BaseModel):
    """Raw output from PainProfiler"""
    pain_candidates: List[str] = Field(default_factory=list)
    raw_fragments: List[str] = Field(default_factory=list)
    pattern_matches: Optional[Dict] = None
    primary_pain: Optional[str] = None  # Final choice for backward compat

class EmailWriterOutput(BaseModel):
    """Raw output from EmailWriter"""
    personalization_depth: Optional[float] = None
    tone: Optional[str] = None
    structure: Optional[str] = None
    length: Optional[int] = None
    email_body: Optional[str] = None  # The actual email

class EnrichmentOutput(BaseModel):
    """Raw output from EnrichmentAgent"""
    raw_company_category: Optional[str] = None
    raw_product_type: Optional[str] = None
    raw_business_model: Optional[str] = None
    raw_role_signals: Optional[Dict] = None

# ===== AGGREGATED RAW CONTEXT =====

class RawContext(BaseModel):
    """Complete raw context from all agents"""
    lead_name: str
    lead_company: str
    lead_title: str
    
    brightdata: Optional[BrightDataOutput] = None
    enrichment: Optional[EnrichmentOutput] = None
    pain: Optional[PainProfilerOutput] = None
    angle: Optional[AngleRouterOutput] = None
    email: Optional[EmailWriterOutput] = None
    
    # Metadata
    agent_versions: Dict[str, str] = Field(default_factory=dict)
