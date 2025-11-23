import os
import csv
import hashlib
import subprocess
import sys

def run_pipeline():
    """Runs the main.py pipeline."""
    print("  Running pipeline...")
    try:
        # Force UTF-8 encoding for subprocess
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        
        result = subprocess.run(
            [sys.executable, "main.py"], 
            check=True, 
            capture_output=True, 
            text=True,
            env=env,
            encoding='utf-8'
        )
    except subprocess.CalledProcessError as e:
        print(f"Pipeline failed with exit code {e.returncode}")
        print(f"STDOUT:\n{e.stdout}")
        print(f"STDERR:\n{e.stderr}")
        raise e

def get_file_hash(filepath):
    """Returns MD5 hash of file content."""
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def verify_output_validity(filepath):
    """Rule #1 & #4: Checks for valid fields and structural correctness."""
    print("  Verifying output validity...")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"{filepath} does not exist!")

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    if not rows:
        raise ValueError("Output CSV is empty!")

    for i, row in enumerate(rows):
        # Rule #1: No missing fields / None values
        for key, value in row.items():
            if not value or value.strip() == "":
                raise ValueError(f"Row {i} has empty field: {key}")
        
        # Rule #4: Structural Correctness
        email = row.get('email', '')
        pain = row.get('pain', '')
        angle = row.get('angle', '')
        
        if len(email) < 50:
            raise ValueError(f"Row {i}: Email too short!")
        if pain not in email:
            raise ValueError(f"Row {i}: Email missing pain reference '{pain}'")
        if "Subject:" not in email:
            raise ValueError(f"Row {i}: Email missing Subject line")

    print("  Output Validity Verified.")

def verify_determinism(filepath):
    """Rule #2: Runs pipeline twice, asserts identical output."""
    print("  Verifying determinism...")
    
    # Run 1
    run_pipeline()
    hash1 = get_file_hash(filepath)
    
    # Run 2
    run_pipeline()
    hash2 = get_file_hash(filepath)
    
    if hash1 != hash2:
        raise ValueError("Determinism Failed: Outputs differ between runs!")
    
    print("  Determinism Verified (Hashes match).")

def main():
    print("Starting MVP Verification...")
    output_file = "generated_emails.csv"
    
    try:
        # Initial run to ensure file exists
        # Always run pipeline to ensure we test current code
        run_pipeline()

        verify_output_validity(output_file)
        verify_determinism(output_file)
        
        print("\nALL CHECKS PASSED. MVP IS SOLID.")
        
    except Exception as e:
        print(f"\nVERIFICATION FAILED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
