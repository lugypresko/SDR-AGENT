import csv
import os
from agents.enrichment_agent import enrich_lead
from agents.pain_profiler import profile_pain
from agents.angle_router import route_angle
from agents.email_writer import write_email
from agents.email_quality_agent import check_quality

def main():
    input_file = 'leads.csv'
    output_file = 'generated_emails.csv'
    
    print(f"🚀 Starting MVP Pipeline...")
    print(f"📂 Loading {input_file}...")

    leads = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(row)

    print(f"📊 Found {len(leads)} leads. Processing...")

    results = []
    
    for i, lead in enumerate(leads):
        print(f"  [{i+1}/{len(leads)}] Processing {lead['name']} @ {lead['company']}...")
        
        # 1. Enrichment
        ctx = enrich_lead(lead)
        
        # 2. Pain Profiler
        pain = profile_pain(ctx)
        
        # 3. Angle Router
        angle = route_angle(ctx, pain)
        
        # 4. Email Writer
        raw_email = write_email(ctx, pain, angle)
        
        # 5. Quality Check
        approved, final_email = check_quality(raw_email, pain)
        
        results.append({
            "name": lead['name'],
            "company": lead['company'],
            "pain": pain,
            "angle": angle,
            "email": final_email,
            "approved": approved
        })

    print(f"💾 Saving results to {output_file}...")
    
    keys = results[0].keys()
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)

    print(f"✅ Done! Generated {len(results)} emails.")

if __name__ == "__main__":
    main()
