As the SDR-MVP system,
I need to convert messy raw lead data into a clean, consistent, structured NormalizedLead object including angle-relevant fields,
so that downstream agents can deterministically select the correct messaging angle.

🎯 Goal

Before any enrichment, pain-profiling, or angle-router logic runs, the system must guarantee:

Clean names

Standardized roles

Clear company size + stage

Clear company category

Extracted location

Clean URLs

AND a set of angle features:

New Angle Features:

delivery_pressure

product_complexity

team_structure

engineering_maturity

decision_maker_level

execution_noise_level

multi_team_coordination

organizational_stage_signal

These act as inputs to the ANGLE router, ensuring accuracy.

🧩 Why ANGLES Must Be Part of Normalization

Right now, the ANGLE router depends on vague signals (company category, pains).
That’s fragile — a VP R&D with:

“Head of Engineering”
“R&D Director”
“VP Delivery”
“CTO (acting)”

…receives wildly different interpretations.

Normalization layer must classify them into predictable buckets.

This enables the router to choose the correct angle (Execution OS, Velocity, Technical Debt, Cross-Team Flow, Predictability, etc.).

📝 User Story Acceptance Criteria (including ANGLES)
1. Name Normalization

Same as before.

2. Role Normalization

Add deterministic classification for ANGLE logic:

role_seniority:

"executive"

"senior-lead"

"manager"

"ic"

role_category:

"engineering"

"rd"

"product"

"data"

"cto-track"

angle-impact:

"strategic" if executive

"tactical" if senior lead

"operational" if manager

"observational" if IC

3. Company Size → Company Stage Mapping

Same as before plus angle signal:

organizational_stage_signal:

startup → "chaos"

small scaleup → "growing"

scaleup → "breaking"

growth → "complex"

enterprise → "bureaucratic"

These map directly to certain angles (e.g., "Execution OS" is ideal for breaking-stage scaleups).

4. Industry / Category Normalization

Add angle-impact hooks:

If category contains:

cyber → high “complexity”

AI → high “product_complexity”

mobile/services → high “execution_noise”

b2b saas → balanced

Output angle features:

product_complexity: "low"|"medium"|"high"

delivery_pressure: "low"|"medium"|"high"

5. URL Normalization

Same.

6. Location Normalization

Same.

7. New Angle Feature Extraction (Critical)

Based on:

role

company size

industry

domain

title

Normalization outputs deterministic values:

Example mapping:

Role:

VP R&D → decision_maker_level = "high"

Head of Engineering → "medium"

Team Lead → "low"

Company Stage:

scaleup → engineering_maturity = "medium"

growth → "high"

startup → "low"

Industry:

AI / Data → product_complexity = "high"

enterprise IT → multi_team_coordination = "high"

These become part of:

AngleSignals:
class AngleSignals(BaseModel):
    delivery_pressure: str
    product_complexity: str
    team_structure: str
    engineering_maturity: str
    decision_maker_level: str
    execution_noise_level: str
    multi_team_coordination: str
    organizational_stage_signal: str

📦 Deliverable: NormalizedLead (with AngleSignals)
class NormalizedLead(BaseModel):
    first_name: str
    last_name: str
    role_title: Optional[str]
    role_seniority: Optional[str]
    role_category: Optional[str]
    company: str
    company_size: Optional[int]
    company_stage: Optional[str]
    industry: Optional[str]
    company_category: Optional[str]
    linkedin_url: Optional[str]
    website_url: Optional[str]
    country: Optional[str]
    region: Optional[str]

    # NEW
    angle_signals: AngleSignals

🧪 Acceptance Tests (Angle-Oriented)
Test A: VP R&D @ 100-person scaleup

Expect:

decision_maker_level = "high"
engineering_maturity = "medium"
organizational_stage_signal = "breaking"
product_complexity = "medium/high"


ANGLE router can now choose:

Predictability

Execution OS

Engineering Velocity

Test B: Head of Engineering @ 300-person growth company

Expect:

decision_maker_level = "medium"
engineering_maturity = "high"
multi_team_coordination = "high"
organizational_stage_signal = "complex"


ANGLE router chooses:

Cross-team Flow

Alignment & Planning

Reducing Noise

Test C: Startup CTO

Expect:

execution_noise_level = "high"
delivery_pressure = "high"
engineering_maturity = "low"


ANGLE router chooses:

Focus

Prioritization

Stabilizing Delivery