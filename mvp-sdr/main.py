import csv
import os
from agents.enrichment_agent import EnrichmentAgent
from agents.pain_profiler import PainProfiler
from agents.angle_router import AngleRouter
from agents.email_writer import EmailWriter
from agents.email_quality_agent import EmailQualityAgent
from schema_governor import SchemaGovernor

def main():
    input_file = 'leads.csv'
    output_file = 'generated_emails.csv'
    
    # Instantiate Agents
    enrichment_agent = EnrichmentAgent()
    pain_profiler = PainProfiler()
    angle_router = AngleRouter()
    email_writer = EmailWriter()
    quality_agent = EmailQualityAgent()
    governor = SchemaGovernor()

    print(f"Starting MVP Pipeline (Phase 3: Multi-Angle)...")
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
    
    for i, lead in enumerate(leads):
        print(f"  [{i+1}/{len(leads)}] Processing {lead['name']} @ {lead['company']}...")
        
        # 1. Enrichment -> NormalizedLead
        normalized_lead = enrichment_agent.run(lead)
        
        # MVSG: Validate NormalizedLead
        validation = governor.validate_normalized_lead(normalized_lead, lead['name'])
        governor.log_validation_result(validation)
        
        # 2. Pain Profiler (Takes NormalizedLead)
        pain = pain_profiler.run(normalized_lead)
        
        # 3. Angle Router (Takes NormalizedLead)
        angle = angle_router.run(normalized_lead, pain)

        # 4. Email Generation
        email_output = email_writer.run(normalized_lead, pain, angle)
        
        # MVSG: Validate EmailOutput
        validation = governor.validate_email_output(email_output, lead['name'])
        governor.log_validation_result(validation)

        # 5. Quality Assurance
        clean_email = quality_agent.run(email_output)

        # 6. Append Result
        # Merge lead data, pipeline context, and email output
        result_row = lead.copy()
        result_row.update({
            "pain": pain,
            "angle": angle,
            **clean_email.dict()
        })
        results.append(result_row)
        
    if results:
        keys = results[0].keys()
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(results)

    print(f"Done! Generated {len(results)} emails.")

if __name__ == "__main__":
    main()
