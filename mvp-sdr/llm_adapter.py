import json
import os
from llm_client import LLMClient
from mock_llm_provider import MockLLMProvider

class LLMAdapter:
    def __init__(self):
        self.client = LLMClient()
        self.mock_provider = MockLLMProvider()
        # Default to MOCK_MODE = True for Phase 5
        self.mock_mode = os.getenv("MOCK_MODE", "True").lower() == "true"
        
    def call(self, prompt, tier="tier2", schema=None, system_prompt="You are a helpful assistant."):
        """
        High-level API for Agents.
        tier: "tier1" (Pro/Expensive) or "tier2" (Flash/Cheap)
        """
        # 0. Check Mock Mode
        if self.mock_mode:
            # Bypass Cache & Client for pure deterministic simulation
            response_str = self.mock_provider.call(prompt, schema)
            
            # Parse if schema needed (Mock provider returns JSON string for enrichment)
            if schema:
                try:
                    return json.loads(response_str)
                except json.JSONDecodeError:
                    return {}
            return response_str

        # 1. Select Model based on Tier
        if tier == "tier1":
            model = "gpt-4-turbo" # or claude-3-opus
        else:
            model = "gpt-3.5-turbo" # or claude-3-haiku
            
        # 2. Construct Messages
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        # 3. Call Client (Handles Cache/Log)
        response_str = self.client.call(model, messages, schema)
        
        # 4. Parse Output (if schema expected)
        if schema:
            try:
                # In a real implementation, we'd use structured output mode.
                # Here we just try to parse the mock JSON.
                return json.loads(response_str)
            except json.JSONDecodeError:
                # Fallback or Error
                print(f"Error parsing JSON from LLM: {response_str}")
                return {}
                
        return response_str
