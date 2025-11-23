"""
Debug script for AngleRouter (SRD-01 Phase 5)
"""
import csv
from agents.enrichment_agent import EnrichmentAgent
from agents.pain_profiler import PainProfiler
from agents.angle_router import AngleRouter

def debug_router():
    print("="*80)
    print("DEBUG: AngleRouter")
    print("="*80)
    
    enricher = EnrichmentAgent()
    profiler = PainProfiler()
    router = AngleRouter()
    
    with open('leads.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        leads = list(reader)
        
    for i, lead in enumerate(leads[:5], 1):
        print(f"\nLead {i}: {lead['name']}")
        nl = enricher.run(lead)
        pain = profiler.run(nl)
        angle = router.run(nl, pain)
        print(f"  -> Pain: {pain}")
        print(f"  -> Angle: {angle}")

if __name__ == "__main__":
    debug_router()
