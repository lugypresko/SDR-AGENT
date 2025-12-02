import csv
import os
import json
from agents.enrichment_agent import EnrichmentAgent
from agents.brightdata_enrichment_agent import BrightDataEnrichmentAgent
from agents.pain_profiler import PainProfiler
from agents.angle_router import AngleRouter
from agents.email_writer import EmailWriter
from agents.email_quality_agent import EmailQualityAgent
from schema_governor import SchemaGovernor
from cse.engine import CSEEngine
from cse.schema import RawContext, BrightDataOutput, PainProfilerOutput, AngleRouterOutput, EmailWriterOutput

def main():
    input_file = 'leads.csv'
    output_file = 'generated_emails.csv'
    trace_file = 'pipeline_trace.json'
    
    # Instantiate Agents
    brightdata_agent = BrightDataEnrichmentAgent()
    enrichment_agent = EnrichmentAgent()
    pain_profiler = PainProfiler()
    angle_router = AngleRouter()
    email_writer = EmailWriter()
    quality_agent = EmailQualityAgent()
    governor = SchemaGovernor()
    
    # Instantiate CSE Engine
    cse_engine = CSEEngine()

    print(f"Starting MVP Pipeline (Phase 7: CSE Integration)...")
    print(f"Loading {input_file}...")

    leads = []
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(row)

    print(f"Found {len(leads)} leads. Processing...")

    results = []
    all_traces = []
    
    for i, lead in enumerate(leads):
        print(f"  [{i+1}/{len(leads)}] Processing {lead['name']} @ {lead['company']}...")
        
        # ===== PHASE 1: COLLECT RAW AGENT OUTPUTS =====
        
        # 0. BrightData Enrichment (Raw)
        try:
            bd_raw = brightdata_agent.run(lead)
            print(f"    [BrightData] Raw data collected")
            bd_output = BrightDataOutput(**bd_raw)
        except Exception as e:
            print(f"    [BrightData] Failed: {e}")
            bd_output = None
        
        # 1. Enrichment -> NormalizedLead (still needed for pain/angle agents)
        normalized_lead = enrichment_agent.run(lead)
        
        # MVSG: Validate NormalizedLead
        validation = governor.validate_normalized_lead(normalized_lead, lead['name'])
        governor.log_validation_result(validation)
        
        # 2. Pain Profiler (Raw)
        pain_raw = pain_profiler.run(normalized_lead)
        print(f"    [Pain] Candidates: {pain_raw.get('pain_candidates', [])}")
        pain_output = PainProfilerOutput(**pain_raw)
        
        # 3. Angle Router (Raw)
        angle_raw = angle_router.run(normalized_lead, pain_raw['primary_pain'])
        print(f"    [Angle] Selected: {angle_raw.get('selected_angle')}")
        angle_output = AngleRouterOutput(**angle_raw)

        # 4. Email Generation
        email_output_obj = email_writer.run(normalized_lead, pain_raw['primary_pain'], angle_raw['selected_angle'])
        
        # MVSG: Validate EmailOutput
        validation = governor.validate_email_output(email_output_obj, lead['name'])
        governor.log_validation_result(validation)

        # 5. Quality Assurance
        clean_email = quality_agent.run(email_output_obj)
        
        # Convert email to raw output for CSE
        email_output = EmailWriterOutput(
            personalization_depth=0.7,  # Placeholder
            tone="professional",
            structure="standard",
            length=len(clean_email.body) if clean_email.body else 0,
            email_body=clean_email.body
        )
        
        # ===== PHASE 2: ASSEMBLE RAW CONTEXT =====
        
        raw_context = RawContext(
            lead_name=lead['name'],
            lead_company=lead['company'],
            lead_title=lead.get('title', ''),
            brightdata=bd_output,
            pain=pain_output,
            angle=angle_output,
            email=email_output
        )
        
        # ===== PHASE 3: CSE PROCESSING =====
        
        print(f"    [CSE] Processing...")
        cse_result = cse_engine.process(raw_context)
        
        print(f"    [CSE] Score: {cse_result['lead_score']:.0f}, Tier: {cse_result['priority_tier']}, Confidence: {cse_result['avg_confidence']:.2f}")
        
        # ===== PHASE 4: ASSEMBLE OUTPUT =====
        
        # Merge lead data, CSE results, and email
        result_row = lead.copy()
        result_row.update({
            "pain": pain_raw['primary_pain'],
            "angle": angle_raw['selected_angle'],
            "lead_score": cse_result['lead_score'],
            "priority_tier": cse_result['priority_tier'],
            "avg_confidence": cse_result['avg_confidence'],
            "min_confidence": cse_result['min_confidence'],
            "explanation_summary": cse_result['explanation_summary'],
            "data_quality_flag": cse_result['data_quality_flag'],
            **clean_email.dict()
        })
        results.append(result_row)
        
        # Store trace
        all_traces.append({
            "lead_name": lead['name'],
            "lead_company": lead['company'],
            "trace": cse_result['trace']
        })
        
    # ===== WRITE OUTPUTS =====
    
    # Write CSV
    if results:
        keys = results[0].keys()
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(results)
    
    # Write Trace
    with open(trace_file, 'w', encoding='utf-8') as f:
        json.dump(all_traces, f, indent=2)

    print(f"Done! Generated {len(results)} emails.")
    print(f"Trace written to {trace_file}")

if __name__ == "__main__":
    main()
