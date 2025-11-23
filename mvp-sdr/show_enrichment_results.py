"""
Simplified enrichment results display.
"""
import csv
import json
from llm_adapter import LLMAdapter
from agents.enrichment_agent import EnrichmentAgent
from agents.pain_profiler import PainProfiler

# Read leads
with open('leads.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    leads = list(reader)

print("=" * 100)
print("ENRICHMENT RESULTS: Persona-to-Pain-to-Angle Mapping")
print("=" * 100)

enrichment_agent = EnrichmentAgent()
pain_profiler = PainProfiler()

for i, lead in enumerate(leads[:5], 1):  # First 5 personas
    print(f"\n{i}. {lead['name']} - {lead['title']} @ {lead['company']} ({lead['employees']} employees)")
    
    # Run enrichment
    normalized_lead = enrichment_agent.run(lead)
    
    # Show key angle signals
    s = normalized_lead.angle_signals
    print(f"   Signals: noise={s.execution_noise_level}, structure={s.team_structure}, coord={s.multi_team_coordination}, stage={s.organizational_stage_signal}")
    
    # Run pain profiler
    pain = pain_profiler.run(normalized_lead)
    print(f"   → PAIN: {pain}")

print("\n" + "=" * 100)
print("FINAL CSV OUTPUT:")
print("=" * 100)

with open('generated_emails.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

for r in rows:
    print(f"{r['name']:20} | {r['pain']:35} | {r['angle']}")

print("=" * 100)

# Summary
pains = [r['pain'] for r in rows]
angles = [r['angle'] for r in rows]

print(f"\nSUMMARY:")
print(f"  Total Leads: {len(rows)}")
print(f"  Unique Pains: {len(set(pains))}")
print(f"  Unique Angles: {len(set(angles))}")

print(f"\nPain Distribution:")
for pain in sorted(set(pains)):
    count = pains.count(pain)
    print(f"  - {pain}: {count} leads")

print(f"\nAngle Distribution:")
for angle in sorted(set(angles)):
    count = angles.count(angle)
    print(f"  - {angle}: {count} leads")
