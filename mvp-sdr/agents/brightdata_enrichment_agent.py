from tools.brightdata_client import BrightDataClient

class BrightDataEnrichmentAgent:
    """
    BrightData Enrichment Agent (CSE Phase 7 - "Dumb" Mode)
    
    This agent ONLY fetches and returns raw data from BrightData.
    ALL intelligence (stress signals, complexity, org health) is now handled by the CSE.
    """
    def __init__(self):
        self.client = BrightDataClient()

    def run(self, lead_row):
        """
        Fetch raw BrightData signals.
        
        Input: lead_row (dict) - Raw CSV row
        Output: raw_data (dict) - Raw fields ONLY, no interpretation
        """
        company_name = lead_row.get("company", "")
        
        # 1. Fetch Data
        company_data = self.client.search_company(company_name)
        
        # Get domain for job postings
        domain = company_data.get("domain", "")
        if domain:
            jobs_data = self.client.get_job_postings(domain)
        else:
            jobs_data = {"total_open_roles": 0, "roles": [], "hiring_trend": "unknown"}

        # 2. Return RAW fields ONLY (no interpretation, no logic)
        return {
            "raw_description": company_data.get("description", ""),
            "raw_headcount": company_data.get("employees", None),
            "raw_headcount_history": company_data.get("headcount_history", []),
            "raw_open_roles": jobs_data.get("total_open_roles", 0),
            "raw_industry": company_data.get("industry", ""),
            "raw_tech_stack": company_data.get("tech_stack", []),
            "raw_org_structure": company_data.get("org_structure", {}),
            "raw_domain": domain,
            "raw_hiring_trend": jobs_data.get("hiring_trend", "unknown"),
            "raw_churn_rate": company_data.get("churn_rate", None),
            "raw_new_cto_recent": company_data.get("new_cto_recent", False),
        }
