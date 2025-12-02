ANTIGRAVITY – SYSTEM REPAIR DIRECTIVE (SRD-01)

Objective: Restore full persona differentiation by enforcing a deterministic, contract-driven enrichment → pain → angle pipeline.

PHASE 1 — EnrichmentAgent Reset & Stabilization

Goal: Ensure every lead receives complete and correct angle_signals.

Instructions:

Remove all LLM-related code from EnrichmentAgent.

Disable LLMAdapter calls entirely (tier1 / tier2). They must NOT be invoked.

Use MockLLMProvider exclusively for enrichment.

Call _mock_enrichment(bio) deterministically for every lead.

Ensure _mock_enrichment() JSON fields map exactly to AngleSignals fields:

delivery_pressure

product_complexity

team_structure

engineering_maturity

decision_maker_level

execution_noise_level

multi_team_coordination

organizational_stage_signal

If any field is missing or None, apply a safe default:

"medium" for most

"functional" for team structure

"growing" for org stage

Ensure the returned NormalizedLead includes:

correct first_name / last_name

correct role_title & role_seniority

correct company_stage

correct company_category

fully populated angle_signals

Eliminate all fallback paths that overwrite signals with defaults unless an actual exception occurs.

PHASE 2 — PainProfiler Hierarchical Logic

Goal: Map signals → pain deterministically for each persona.

Instructions:

Replace PainProfiler logic with a priority-based rule system:

Priority 1: extreme noise OR chaos → “firefighting spiral”

Priority 2: matrix + high noise → “silent attrition”

Priority 3: high coordination OR squads → “cross-team flow collapse”

Priority 4: breaking stage + high noise → “too many initiatives”

Priority 5: cross-functional OR scaleup → “architecture drift”

Priority 6: flat + low maturity → “no delegation layer”

Else → “execution friction”

Rules must be mutual-exclusive and evaluated top-to-bottom.

Use only fields defined in AngleSignals.

Ensure no string operations treat AngleSignals as a list.

PHASE 3 — AngleRouter Alignment

Goal: Ensure selected angle matches selected pain.

Instructions:

Create deterministic mapping:

“firefighting spiral” → Firefighting Spiral

“silent attrition” → Team Health

“cross-team flow collapse” → Execution Velocity

“too many initiatives” → Predictability

“architecture drift” → Strategic Clarity

“no delegation layer” → Team Foundations

“execution friction” → Execution Velocity

Ensure no rule conflicts with PainProfiler output.

Guarantee all angles are valid and recognized by EmailWriter.

PHASE 4 — Determinism Enforcement

Goal: Ensure no randomness or external calls pollute results.

Instructions:

Remove:

random(), randint(), shuffle()

datetime-based seeds

non-deterministic string ordering

any LLM variability

Normalize:

whitespace

capitalization

ordering of dicts

Ensure:

same input → same CSV

verify_mvp.py determinism check passes (hash match)

PHASE 5 — Debugging Infrastructure

Goal: Provide instrumentation to verify correct behavior.

Instructions:

Implement debug print blocks in each agent:

“ENRICHMENT SIGNALS:”

“PAIN SELECTED:”

“ANGLE SELECTED:”

Ensure they are printed during main.py execution.

Provide a structured debug function for each agent, callable via:

python debug_enrichment.py
python debug_pain_profiler.py
python debug_router.py

PHASE 6 — Validation

Goal: Confirm pipeline is fully repaired.

Instructions:

Run:

python verify_mvp.py
python verify_phase5.py


Expected results:

PASS

PASS

≥5 distinct pains

≥5 distinct angles

100% deterministic

EXPECTED OUTCOME

After successful execution of all phases, the system MUST produce:

Persona-specific signals

Persona-specific pains

Persona-specific angles

Persona-specific emails

Complete determinism

Verification success across all tests

…and zero fallback “execution friction” except for true edge cases.