from contracts import NormalizedLead, AngleSignals
import json
import traceback
from mock_llm_provider import MockLLMProvider

class EnrichmentAgent:
    def __init__(self):
        # SRD-01 Phase 1: Use MockLLMProvider exclusively
        self.provider = MockLLMProvider()

    def run(self, row):
        """
        SRD-01 Compliant Enrichment:
        - Direct call to MockLLMProvider._mock_enrichment()
        - No LLMAdapter
        - Deterministic signal extraction
        """

        # ----------------------------------------------------
        # 1. BASIC FIELDS
        # ----------------------------------------------------
        name = row.get("name", "")
        parts = name.split()
        first_name = parts[0] if parts else ""
        last_name = " ".join(parts[1:]) if len(parts) > 1 else ""

        company = row.get("company", "")
        title = (row.get("title") or "")
        bio = (row.get("linkedin_bio") or "")
        employees = int(row.get("employees", 0))

        # ----------------------------------------------------
        # 2. CALL MOCK LLM ENRICHMENT (DIRECT)
        # ----------------------------------------------------
        try:
            # Direct call to mock provider
            # SRD-01 Fix: Pass title + company + bio to ensure keywords (e.g. "CTO") are detected
            # even if bio is just a URL.
            enrichment_prompt = f"{title} at {company}. {bio}"
            raw_response = self.provider._mock_enrichment(enrichment_prompt)

            # Parse JSON response
            if isinstance(raw_response, str):
                data = json.loads(raw_response)
            else:
                data = raw_response

            # Extract angle signals
            signals_data = data.get("angle_signals", {})
            
            # SRD-01: Map fields exactly, apply safe defaults if missing
            angle_signals = AngleSignals(
                delivery_pressure=signals_data.get("delivery_pressure", "medium"),
                product_complexity=signals_data.get("product_complexity", "medium"),
                team_structure=signals_data.get("team_structure", "functional"),
                engineering_maturity=signals_data.get("engineering_maturity", "medium"),
                decision_maker_level=signals_data.get("decision_maker_level", "low"),
                execution_noise_level=signals_data.get("execution_noise_level", "low"),
                multi_team_coordination=signals_data.get("multi_team_coordination", "low"),
                organizational_stage_signal=signals_data.get("organizational_stage_signal", "growing")
            )

            # ----------------------------------------------------
            # 3. DERIVED ROLE SIGNALS
            # ----------------------------------------------------
            title_l = title.lower()
            if any(k in title_l for k in ["cto", "vp", "chief", "founder", "head of"]):
                role_seniority = "executive"
                role_category = "leadership"
            elif any(k in title_l for k in ["director", "principal", "architect"]):
                role_seniority = "senior-lead"
                role_category = "architecture"
            elif any(k in title_l for k in ["manager", "lead"]):
                role_seniority = "manager"
                role_category = "management"
            else:
                role_seniority = "ic"
                role_category = "individual"

            # ----------------------------------------------------
            # 4. COMPANY STAGE
            # ----------------------------------------------------
            if employees < 50:
                company_stage = "startup"
            elif employees < 200:
                company_stage = "scaleup"
            elif employees < 1000:
                company_stage = "growth"
            else:
                company_stage = "enterprise"

            # ----------------------------------------------------
            # 5. BUILD NORMALIZED LEAD
            # ----------------------------------------------------
            lead = NormalizedLead(
                first_name=first_name,
                last_name=last_name,
                role_title=title,
                role_seniority=role_seniority,
                role_category=role_category,
                company=company,
                company_size=employees,
                company_stage=company_stage,
                industry=data.get("company_category", "Technology"),
                company_category=data.get("company_category", "Technology"),
                product_type=data.get("product_type", "Unknown"),
                business_model=data.get("business_model", "Unknown"),
                linkedin_url=bio,
                angle_signals=angle_signals
            )
            
            # Debug print (SRD-01 Phase 5)
            print(f"ENRICHMENT SIGNALS for {name}: {angle_signals}")

            return lead

        except Exception as e:
            print(f"CRITICAL ENRICHMENT FAILURE for {name}: {e}")
            traceback.print_exc()
            # SRD-01: Eliminate fallback paths unless actual exception
            # If we are here, something is truly broken.
            # We return a safe default but log heavily.
            return NormalizedLead(
                first_name=first_name,
                last_name=last_name,
                role_title=title,
                company=company,
                company_size=employees,
                angle_signals=AngleSignals(
                    delivery_pressure="medium",
                    product_complexity="medium",
                    team_structure="functional",
                    engineering_maturity="medium",
                    decision_maker_level="low",
                    execution_noise_level="low",
                    multi_team_coordination="low",
                    organizational_stage_signal="growing"
                )
            )
