from llm_adapter import LLMAdapter
import os
import time
import json

def verify_infrastructure():
    print("Verifying LLM Infrastructure...")
    adapter = LLMAdapter()
    
    # 1. Test Call (Miss)
    print("1. Testing API Call (Cache Miss)...")
    start = time.time()
    response1 = adapter.call("Extract info", tier="tier2", schema=True)
    lat1 = time.time() - start
    print(f"   Response: {response1}")
    print(f"   Latency: {lat1:.4f}s")
    
    # 2. Test Call (Hit)
    print("2. Testing API Call (Cache Hit)...")
    start = time.time()
    response2 = adapter.call("Extract info", tier="tier2", schema=True)
    lat2 = time.time() - start
    print(f"   Response: {response2}")
    print(f"   Latency: {lat2:.4f}s")
    
    if lat2 > 0.1:
        print("FAIL: Cache hit should be near-instant.")
    else:
        print("PASS: Cache is working.")
        
    # 3. Check DB
    if os.path.exists("cache.db"):
        print("PASS: cache.db exists.")
    else:
        print("FAIL: cache.db missing.")
        
    # 4. Check Logs
    if os.path.exists("logs/llm_logs.jsonl"):
        print("PASS: Logs exist.")
        with open("logs/llm_logs.jsonl", "r") as f:
            logs = [json.loads(line) for line in f]
            print(f"   Log entries: {len(logs)}")
    else:
        print("FAIL: Logs missing.")

if __name__ == "__main__":
    verify_infrastructure()
