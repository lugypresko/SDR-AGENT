import sqlite3
import json
import time
import os
import hashlib
from datetime import datetime

class LLMClient:
    def __init__(self, cache_db="cache.db", log_file="logs/llm_logs.jsonl"):
        self.cache_db = cache_db
        self.log_file = log_file
        self._init_db()
        self._init_logs()

    def _init_db(self):
        conn = sqlite3.connect(self.cache_db)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS cache
                     (hash TEXT PRIMARY KEY, response TEXT, model TEXT, timestamp REAL)''')
        conn.commit()
        conn.close()

    def _init_logs(self):
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

    def _get_cache_key(self, model, messages, schema=None):
        # Create a deterministic hash of the input
        data = json.dumps({"model": model, "messages": messages, "schema": schema}, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()

    def _log(self, model, messages, response, cache_hit, latency):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "cache_hit": cache_hit,
            "latency_ms": round(latency * 1000, 2),
            "messages": messages,
            "response": response
        }
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")

    def call(self, model, messages, schema=None):
        """
        Low-level LLM call with Caching and Logging.
        """
        cache_key = self._get_cache_key(model, messages, schema)
        
        # 1. Check Cache
        conn = sqlite3.connect(self.cache_db)
        c = conn.cursor()
        c.execute("SELECT response FROM cache WHERE hash=?", (cache_key,))
        row = c.fetchone()
        conn.close()

        if row:
            self._log(model, messages, row[0], True, 0)
            return row[0]

        # 2. Call Provider (MOCK for now)
        start_time = time.time()
        response = self._mock_provider(model, messages, schema)
        latency = time.time() - start_time

        # 3. Save to Cache
        conn = sqlite3.connect(self.cache_db)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO cache VALUES (?, ?, ?, ?)", 
                  (cache_key, response, model, time.time()))
        conn.commit()
        conn.close()

        self._log(model, messages, response, False, latency)
        return response

    def _mock_provider(self, model, messages, schema):
        """
        Mock responses for development.
        """
        last_msg = messages[-1]['content']
        
        # Mock Enrichment
        if "Extract" in last_msg or "Enrich" in last_msg:
            return json.dumps({
                "company_category": "AI/Data",
                "pain_points": ["data silos", "slow reporting"],
                "signals": ["hiring data engineers", "series B"]
            })
            
        # Mock Writing
        if "Write an email" in last_msg:
            return "Subject: Speed\n\nHi,\n\nI noticed you are scaling. Speed is key.\n\nWe help.\n\nChat?"

        return "Mock LLM Response"
