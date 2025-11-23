import csv
import subprocess
import sys
from agents.enrichment_agent import EnrichmentAgent
from agents.angle_router import AngleRouter
from agents.hook_engine import HookEngine
from contracts import NormalizedLead, AngleSignals

def verify_phase3():
    print("Running Phase 3 Verification...")
    
    # 1. Run Pipeline
    print("Running main.py...")
    subprocess.run([sys.executable, "main.py"], check=True)
    
    # 2. Load Results
    emails = []
    with open("generated_emails.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            emails.append(row)
            
    if not emails:
        print("FAIL: No emails generated.")
        return

    # 3. Verify Completeness (Are we hitting different angles?)
    angles = set(e['angle'] for e in emails)
    print(f"Unique Angles Found: {angles}")
    if len(angles) < 2:
        print("WARNING: Low angle diversity. Check routing logic.")
        
    # 4. Verify Structure & Hooks
    print("\nVerifying Structure...")
    for e in emails:
        body = e['email']
        subject = e['subject']
        
        # Check for Hook (First line should be non-empty)
        lines = body.split('\n')
        hook = lines[0]
        if len(hook) < 10:
            print(f"FAIL: Hook too short for {e['name']}: {hook}")
            
        # Check for Tone Guardrails (Negative)
        banned = ["Hope you are well", "Just checking in"]
        for b in banned:
            if b in body:
                print(f"FAIL: Banned phrase found in {e['name']}: {b}")
                
        print(f"  OK: {e['name']} -> {e['angle']}")

    # 5. Verify Determinism
    print("\nVerifying Determinism (Run 2)...")
    subprocess.run([sys.executable, "main.py"], check=True, stdout=subprocess.DEVNULL)
    
    emails_run2 = []
    with open("generated_emails.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            emails_run2.append(row)
            
    if emails == emails_run2:
        print("PASS: Determinism verified.")
    else:
        print("FAIL: Output changed between runs.")

if __name__ == "__main__":
    verify_phase3()
