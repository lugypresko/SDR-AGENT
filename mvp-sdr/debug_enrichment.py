"""
Debug script for EnrichmentAgent (SRD-01 Phase 5)
"""
import csv
from agents.enrichment_agent import EnrichmentAgent

def debug_enrichment():
    print("="*80)
    print("DEBUG: EnrichmentAgent")
    print("="*80)
    
    agent = EnrichmentAgent()
    
    # Test with leads.csv
    with open('leads.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        leads = list(reader)
        
    for i, lead in enumerate(leads[:5], 1):
        print(f"\nLead {i}: {lead['name']} ({lead['title']})")
        
        try:
            nl = agent.run(lead)
            s = nl.angle_signals
            print(f"  -> Signals Extracted:")
            print(f"     - noise: {s.execution_noise_level}")
            print(f"     - structure: {s.team_structure}")
            print(f"     - coordination: {s.multi_team_coordination}")
            print(f"     - stage: {s.organizational_stage_signal}")
            print(f"     - pressure: {s.delivery_pressure}")
            print(f"     - maturity: {s.engineering_maturity}")
            print(f"     - complexity: {s.product_complexity}")
            print(f"     - decision: {s.decision_maker_level}")
        except Exception as e:
            print(f"  -> ERROR: {e}")

if __name__ == "__main__":
    debug_enrichment()
