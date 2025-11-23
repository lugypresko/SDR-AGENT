OPERATIONAL BLUEPRINT 3.0 — Agentic Pipeline Development
For ultra-fast, low-cost, low-friction agent development
1. SYSTEM CONTRACT (NON-NEGOTIABLE)

Every project begins with this written contract before a single line of code:

1.1 Agent Roles

Each agent has ONE responsibility only:

Agent	Responsibility
Enrichment	Extract context and summaries
PainProfiler	Map profile → structured pains
AngleRouter	Pick angle deterministically
Writer	Generate email based on angle
QA	Validate email meets minimal quality

No agent may perform another agent’s job.

1.2 Allowed Operations

Agents may:

Read from context contract

Update their own output fields

Modify ONLY internal logic when instructed

Return clean structured data

Agents may NOT:

Add new fields

Change data flow

Add new logic paths unless instructed

“Improve” anything unless told explicitly

Use reasoning outside provided fields

1.3 Orchestrator Is Sacred

You must include this sentence:

The orchestrator is immutable. It cannot be edited, proposed for edits, or refactored.

2. DEVELOPMENT EXECUTION MODEL
2.1 PLAN / ACT Strict Mode

Every cycle must follow this structure:

Developer (you) requests a refinement

Model replies with PLAN only

You review

You respond ACT APPROVED

Model performs only the approved diff

Anything else = violation.

2.2 Freeze Protocol

Once an agent works:

You freeze it. No more changes.

This prevents endless tweaks.

Mark it as:

# FROZEN — do not modify

2.3 MVP Stop Condition

Define BEFORE coding:

“The system is DONE when 3 sample leads run without errors and all emails are approved.”

No quality polishing unless explicitly requested.

3. TESTING STRATEGY
3.1 Micro-Runs Only

Never run full CSV during development.

Use:

python main.py --single-lead sample1.json
python main.py --single-lead sample2.json


Why?

Faster iterations

Clearer debugging

No overwhelm

Lower costs

Full CSV is only for final verification.

3.2 Test Harness (Mandatory)

Add /test/ folder with:

sample1.json

sample2.json

sample3.json

Every agent must be tested against these.

4. RISK-REDUCTION ENGINEERING
4.1 LLM Caching Layer (Required)

Before running a pipeline 10 times, ensure:

Each LLM call is cached

Identical input → identical output → 0 cost

This reduces development time by 30–50%.

4.2 Model Stability Policy

Never switch models mid-project.

If a switch is required:

freeze project → snapshot → re-init pipeline → revalidate agents

4.3 Response Hygiene Contract

Every agent must enforce:

No null fields

No missing fields

No drift

No extra output

If something breaks → HARD STOP.

5. OBSERVABILITY & DEBUGGING
5.1 Structured Logs

Every agent logs:

input fields

output fields

reasoning summary (if allowed)

This allows instant problem detection.

5.2 Hard Alerts During Development

If contract is violated:

stop execution

print offending agent

print offending field

Return:
“Invalid contract — agent X violated field Y.”

5.3 Automatic Failure Recorder

If an agent fails:

save file to:

/debug/failure_<timestamp>.json


containing:

prompt

model response

agent name

contract violation

This prevents blind debugging.

6. LLM TIERING (COST & SPEED STRATEGY)
6.1 Two-Tier Model Strategy

Tier 1 (expensive):

Writer

PainProfiler

Tier 2 (cheap):

QA

Router

Enrichment

This cuts cost massively and doesn’t harm accuracy.

7. BLUEPRINT 3.0 SUMMARY

This entire system reduces:

rework

model drift

debugging time

LLM cost

pipeline breakage

And increases:

predictability

development speed

reproducibility

agent isolation

confidence in each iteration