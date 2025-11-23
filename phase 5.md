Phase 5: Advanced Mock Mode (Full Intelligence Simulation)

Goal: The system must behave exactly like a real SDR agentic pipeline, but powered by deterministic mock logic.

No randomness.
No hallucinations.
No real API calls.
Just a smart illusion.

1. Upgrade the Mock Provider

File: mock_llm_provider.py

Create a class with 3 layers of deterministic behavior:

Layer A — Synthetic Enrichment

Instead of returning “Mock LLM Response,” return structured enrichments based on the lead:

If company size > 60 → "scaleup-pressure"

If title contains “VP” → “executive-senior”

If company name includes “Sky”, “Cloud” → “AI or High-throughput”

If industry is empty → “default: SaaS scaleup”

Output example:

{
  "role_archetype": "executive",
  "org_stage": "scaleup",
  "complexity": "medium-high",
  "risk_profile": "delivery-bottlenecks"
}

Layer B — Synthetic Insight Generation

Return a believable but deterministic observation:

Executive + Scaleup → “Your team is likely drowning in cross-team dependencies.”

Head of Eng + 100+ employees → “Delivery predictability becomes the main KPI.”

Startup CTO → “Everything is on fire, including your roadmap.”

Layer C — Email Generation Mock

Simulate real writing using templates and angle:

Example:

Subject: Cutting Through Cross-Team Drag

Running a scaleup engineering org means you're dealing with dependency drag and shifting priorities.

Most teams try to solve this with more process, but it only slows them further.

Our Execution OS removes bottlenecks by creating flow across squads without adding bureaucracy.

Worth seeing?

2. Add Conditional Behavior in LLMAdapter

When MOCK_MODE=True (env flag):

Skip tiering

Skip caching

Skip external calls

Route everything into mock_llm_provider

This provides 100% determinism.

3. Simulate Tier 1 vs Tier 2 Behavior

Tier 2 (Enrichment):
Must return JSON-structured insight.

Tier 1 (Writer):
Must return a 3-paragraph email, 90–140 words, with:

Subject

Angle reference

Pain reference

CTA

Use two different mock output patterns so the system "looks" like it's using multiple LLM levels.

4. Hardcode 5 Representative Personas for Realistic Variation

Inside the mock provider, implement persona-based branches:

1. VP R&D @ 100-person company

→ “Execution Velocity” angle
→ “Cross-team flow collapse”

2. Head of Engineering @ 50-person scaleup

→ “Predictability” angle
→ “Too many initiatives”

3. CTO @ startup < 30

→ “Firefighting Spiral” angle
→ “No delegation layer”

4. Director Eng @ 200-person corporate

→ “Team Health” angle
→ “Silent attrition”

5. Product Lead @ AI company

→ “Alignment” angle
→ “Architecture drift”

The mock doesn’t know real companies — but it behaves as if it does.

5. Full Integration with the Pipeline

All agents keep working normally:

Brain (Normalization)

Soul (Router)

Mouth (Writer)

Immune System (QA)

Nervous System (Adapter+Client)

Fake Intelligence (Mock Provider)

Everything flows exactly like real inference.

6. Acceptance Criteria for Phase 5 (Mock Mode)

A mock-based pipeline is considered validated when:

generated_emails.csv contains:

At least 4 different Angles

Different hooks per persona

Messages exceeding 70 words

Correct subject lines

Determinism confirmed
Running twice → identical output.

Router decisions match Normalization
VP R&D scaleup → Execution Velocity
Startup CTO → Firefighting Spiral

Emails feel like a real SDR wrote them
Tone senior
Pain relevant
CTA crisp
No junior fluff

7. After Phase 5: You Will Have

A complete, demo-ready agentic SDR engine:

Looks real

Behaves real

Runs fast

Costs zero

Allows end-to-end testing

When you plug in real LLMs later, the pipeline will immediately upgrade itself — no refactoring.