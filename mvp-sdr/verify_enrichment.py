import csv
import sys
import os
from agents.enrichment_agent import EnrichmentAgent
from llm_adapter import LLMAdapter

def verify_enrichment():
    print("Running Enrichment Verification...")
    
    # Load Leads
    leads = []
    with open('leads.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(row)
            
    # Init Agent
    # EnrichmentAgent instantiates its own LLMAdapter internally
    enrichment_agent = EnrichmentAgent()
    
    normalized_leads = []
    print(f"Enriching {len(leads)} leads...")
    
    for lead in leads:
        norm = enrichment_agent.run(lead)
        normalized_leads.append(norm)
        
    # User's Requested Verification Loop
    print("\n--- User Verification Output ---")
    for lead in normalized_leads:
        # Constructing a clean dict for display
        d = lead.dict()
        # Simplify angle_signals for display
        d['angle_signals'] = "..." 
        print(f"Name: {lead.first_name} {lead.last_name} | Signals: {lead.signal_count}")
        print(f"  Role: {lead.role_title} | Stage: {lead.company_stage}")
        print(f"  Product: {lead.product_type} | Model: {lead.business_model}")
        print(f"  Stress: {lead.angle_signals.delivery_pressure} | Health: {lead.angle_signals.execution_noise_level}")
        print("-" * 40)

if __name__ == "__main__":
    # Ensure Mock Mode
    os.environ["MOCK_MODE"] = "True"
    verify_enrichment()
