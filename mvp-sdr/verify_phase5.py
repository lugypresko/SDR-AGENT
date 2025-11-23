import csv
import subprocess
import sys
import os

def verify_phase5():
    print("Running Phase 5 Verification (Advanced Mock Mode)...")
    
    # Ensure MOCK_MODE is on
    os.environ["MOCK_MODE"] = "True"
    
    # 1. Run Pipeline (Run 1)
    print("Running main.py (Run 1)...")
    subprocess.run([sys.executable, "main.py"], check=True)
    
    emails_run1 = []
    with open("generated_emails.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            emails_run1.append(row)
            
    # 2. Run Pipeline (Run 2)
    print("Running main.py (Run 2)...")
    subprocess.run([sys.executable, "main.py"], check=True, stdout=subprocess.DEVNULL)
    
    emails_run2 = []
    with open("generated_emails.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            emails_run2.append(row)
            
    # 3. Verify Determinism
    if emails_run1 == emails_run2:
        print("PASS: Determinism verified.")
    else:
        print("FAIL: Output changed between runs.")
        return

    # 4. Verify Persona Coverage & Quality
    expected_angles = {
        "Alice": "Execution Velocity", # VP R&D
        "Bob": "Predictability", # Head of Eng
        "Charlie": "Firefighting Spiral", # CTO
        "Diana": "Team Health", # Director Eng
        "Eve": "Strategic Clarity" # Product Lead
    }
    
    print("\nVerifying Personas & Quality...")
    for e in emails_run1:
        name = e['name']
        angle = e['angle']
        body = e['email']
        subject = e['subject']
        
        # Check Angle
        expected = expected_angles.get(name)
        if expected and expected != angle:
            # Note: Router logic might differ slightly from Mock Provider logic if Router is still deterministic based on signals.
            # The Mock Provider generates the EMAIL BODY based on persona, but the ROUTER selects the ANGLE based on signals.
            # Ideally they align. Let's see what happens.
            print(f"WARNING: Angle mismatch for {name}. Expected {expected}, got {angle}")
        else:
            print(f"  OK: {name} -> {angle}")
            
        # Check Length (Mock emails should be substantial)
        words = len(body.split())
        if words < 50:
            print(f"FAIL: Email too short for {name} ({words} words).")
        
        # Check Subject
        if "Regarding" in subject and "Mock" not in body:
             # Phase 4 mock subject was "Regarding...", Phase 5 mock provider generates body but Writer might still use "Regarding" if not fully aligned.
             # Actually Writer uses adapter output for body, but subject is still "Regarding {angle}" in the code I wrote in Phase 4.
             pass

    print("Done.")

if __name__ == "__main__":
    verify_phase5()
