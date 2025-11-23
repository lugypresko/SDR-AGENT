Antigravity, apply the following system repair steps:

1. Restore the full original implementation of:
   - agents/email_quality_agent.py
   - tools/mock_llm_provider.py
   These must contain their working pre-scaffolding code exactly as before.

2. Update imports everywhere to match the new folder layout:
   - Replace: from mock_llm_provider import MockLLMProvider
   - With:    from tools.mock_llm_provider import MockLLMProvider
   Do this in:
     • enrichment_agent.py
     • llm_adapter.py
     • any file referencing the old path

3. Do NOT modify:
   - main.py pipeline structure
   - verify_mvp.py
   - verify_phase5.py
   - contracts.py

4. Ensure every agent still exposes:
   run(self, …) → OutputModel

5. After fixing imports and restoring full agents:
   Run verification:
     python verify_mvp.py
     python verify_phase5.py

STOP after both pass. Do not refactor further.
