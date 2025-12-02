"""
Determinism Test Suite
Ensures the CSE pipeline produces bit-for-bit identical outputs across runs.
"""

import subprocess
import json
import csv
import os
import hashlib

def compute_file_hash(filepath):
    """Compute SHA256 hash of a file"""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def run_pipeline():
    """Run the main pipeline"""
    result = subprocess.run(
        ["python", "main.py"],
        cwd=os.path.dirname(os.path.abspath(__file__)) + "/..",
        capture_output=True,
        text=True
    )
    return result.returncode == 0

def test_determinism():
    """
    Test that running the pipeline twice produces identical outputs.
    This is CRITICAL for confidence and debugging.
    """
    print("=" * 60)
    print("DETERMINISM TEST")
    print("=" * 60)
    
    # Run 1
    print("\n[Run 1] Executing pipeline...")
    success1 = run_pipeline()
    assert success1, "Pipeline run 1 failed"
    
    # Capture outputs from run 1
    csv_hash_1 = compute_file_hash("../generated_emails.csv")
    trace_hash_1 = compute_file_hash("../pipeline_trace.json")
    
    print(f"  CSV Hash:   {csv_hash_1}")
    print(f"  Trace Hash: {trace_hash_1}")
    
    # Run 2
    print("\n[Run 2] Executing pipeline...")
    success2 = run_pipeline()
    assert success2, "Pipeline run 2 failed"
    
    # Capture outputs from run 2
    csv_hash_2 = compute_file_hash("../generated_emails.csv")
    trace_hash_2 = compute_file_hash("../pipeline_trace.json")
    
    print(f"  CSV Hash:   {csv_hash_2}")
    print(f"  Trace Hash: {trace_hash_2}")
    
    # Compare
    print("\n[Comparison]")
    csv_match = csv_hash_1 == csv_hash_2
    trace_match = trace_hash_1 == trace_hash_2
    
    print(f"  CSV Match:   {'✓ PASS' if csv_match else '✗ FAIL'}")
    print(f"  Trace Match: {'✓ PASS' if trace_match else '✗ FAIL'}")
    
    if csv_match and trace_match:
        print("\n✅ DETERMINISM TEST PASSED")
        print("Pipeline produces bit-for-bit identical outputs.")
        return True
    else:
        print("\n❌ DETERMINISM TEST FAILED")
        print("Pipeline outputs are NOT deterministic.")
        if not csv_match:
            print("  - CSV differs between runs")
        if not trace_match:
            print("  - Trace differs between runs")
        return False

def test_regression():
    """
    Test that current pipeline output matches frozen baseline.
    This catches unintended changes to scoring/logic.
    """
    print("\n" + "=" * 60)
    print("REGRESSION TEST")
    print("=" * 60)
    
    baseline_csv = "tests/baseline_generated_emails.csv"
    baseline_trace = "tests/baseline_pipeline_trace.json"
    
    if not os.path.exists(baseline_csv) or not os.path.exists(baseline_trace):
        print("\n⚠️  Baseline files not found. Creating baseline...")
        # Copy current outputs as baseline
        import shutil
        shutil.copy("../generated_emails.csv", baseline_csv)
        shutil.copy("../pipeline_trace.json", baseline_trace)
        print(f"  Created: {baseline_csv}")
        print(f"  Created: {baseline_trace}")
        print("\n✅ BASELINE CREATED")
        return True
    
    # Run pipeline
    print("\n[Current Run] Executing pipeline...")
    success = run_pipeline()
    assert success, "Pipeline run failed"
    
    # Compare with baseline
    current_csv_hash = compute_file_hash("../generated_emails.csv")
    current_trace_hash = compute_file_hash("../pipeline_trace.json")
    baseline_csv_hash = compute_file_hash(baseline_csv)
    baseline_trace_hash = compute_file_hash(baseline_trace)
    
    print(f"\n[Baseline]")
    print(f"  CSV Hash:   {baseline_csv_hash}")
    print(f"  Trace Hash: {baseline_trace_hash}")
    
    print(f"\n[Current]")
    print(f"  CSV Hash:   {current_csv_hash}")
    print(f"  Trace Hash: {current_trace_hash}")
    
    csv_match = current_csv_hash == baseline_csv_hash
    trace_match = current_trace_hash == baseline_trace_hash
    
    print(f"\n[Comparison]")
    print(f"  CSV Match:   {'✓ PASS' if csv_match else '✗ FAIL'}")
    print(f"  Trace Match: {'✓ PASS' if trace_match else '✗ FAIL'}")
    
    if csv_match and trace_match:
        print("\n✅ REGRESSION TEST PASSED")
        print("Current output matches baseline.")
        return True
    else:
        print("\n❌ REGRESSION TEST FAILED")
        print("Current output differs from baseline.")
        print("This may indicate unintended changes to scoring/logic.")
        return False

if __name__ == "__main__":
    # Run determinism test
    determinism_pass = test_determinism()
    
    # Run regression test
    regression_pass = test_regression()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Determinism: {'✅ PASS' if determinism_pass else '❌ FAIL'}")
    print(f"Regression:  {'✅ PASS' if regression_pass else '❌ FAIL'}")
    
    if determinism_pass and regression_pass:
        print("\n✅ ALL TESTS PASSED")
        exit(0)
    else:
        print("\n❌ SOME TESTS FAILED")
        exit(1)
