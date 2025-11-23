"""
Debug script for PainProfiler (SRD-01 Phase 5)
"""
import csv
from agents.enrichment_agent import EnrichmentAgent
from agents.pain_profiler import PainProfiler

def debug_pain_profiler():
    print("="*80)
    print("DEBUG: PainProfiler")
    print("="*80)
    
    enricher = EnrichmentAgent()
    profiler = PainProfiler()
    
    with open('leads.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        leads = list(reader)
        
    for i, lead in enumerate(leads[:5], 1):
        print(f"\nLead {i}: {lead['name']}")
        nl = enricher.run(lead)
        pain = profiler.run(nl)
        print(f"  -> Pain: {pain}")

if __name__ == "__main__":
    debug_pain_profiler()
