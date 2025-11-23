import json

class MockLLMProvider:
    def __init__(self):
        self.personas = {
            "VP R&D": {
                "angle": "Execution Velocity",
                "pain": "Cross-team flow collapse",
                "hook": "At this stage, speed is oxygen, but process is the enemy.",
                "email_body": "Running a scaleup engineering org means you're dealing with dependency drag and shifting priorities. It's the silent killer of velocity.\n\nMost teams try to solve this with more process, but it only slows them further. You need visibility, not bureaucracy.\n\nOur Execution OS removes bottlenecks by creating flow across squads without adding weight. We connect the dots between strategy and code.\n\nWorth seeing how we do it?"
            },
            "Head of Engineering": {
                "angle": "Predictability",
                "pain": "Too many initiatives",
                "hook": "Predictability isn't about working harder; it's about seeing the blockers earlier.",
                "email_body": "When you have too many initiatives, the roadmap becomes a wish list rather than a plan. Your team is working hard, but delivery feels random.\n\nWe help you align engineering signals to business goals automatically, giving you a live view of reality.\n\nStop guessing and start delivering with confidence. It changes the conversation with the board.\n\nChat next week?"
            },
            "CTO": {
                "angle": "Firefighting Spiral",
                "pain": "No delegation layer",
                "hook": "If you're always fighting fires, you can't build the fire station.",
                "email_body": "Firefighting isn't a strategy. It's a symptom of a system that can't handle its own complexity. You're stuck in the weeds instead of building the future.\n\nWe build the fire station so you can focus on the architecture. We automate the incident response patterns.\n\nPrevent issues before they start. Get your time back.\n\nOpen to a demo?"
            },
            "Director of Engineering": {
                "angle": "Team Health",
                "pain": "Silent attrition",
                "hook": "Burnout doesn't happen overnight; it happens when friction becomes normal.",
                "email_body": "Your best engineers aren't leaving because of money. They're leaving because they're blocked. They want to ship, not fight tools.\n\nNoise causes burnout. We reduce the noise and give them their focus back. We measure the friction points they can't see.\n\nCan I show you how we save your best talent?"
            },
            "Product Lead": {
                "angle": "Strategic Clarity",
                "pain": "Architecture drift",
                "hook": "Don't let the roadmap drift. Lock it in.",
                "email_body": "Alignment is hard when the architecture drifts from the strategy. You ship features, but the platform rots.\n\nWe ensure every commit aligns with the roadmap. We link code changes to product specs automatically.\n\nKeep your product vision pure. Don't let technical debt kill your velocity.\n\nWorth 5 mins to see the link?"
            }
        }

    def call(self, prompt, schema=None):
        """
        Simulates LLM behavior based on input prompt content.
        """
        # Layer A: Synthetic Enrichment
        if "Extract company_category" in prompt:
            return self._mock_enrichment(prompt)
            
        # Layer C: Email Generation (includes Layer B logic implicitly)
        if "Write a cold email" in prompt:
            return self._mock_email_generation(prompt)
            
        return "Mock LLM Response (Fallback)"

    def _mock_enrichment(self, prompt):
        # Phase 5.5: Rich Enrichment Simulation
        bio = prompt.lower()
        
        # Default
        data = {
            "company_category": "SaaS",
            "product_type": "B2B Platform",
            "business_model": "Subscription",
            "pain_points": ["generic pain"],
            "signals": ["hiring"],
            "angle_signals": {
                "delivery_pressure": "medium",
                "product_complexity": "medium",
                "team_structure": "functional",
                "engineering_maturity": "medium",
                "decision_maker_level": "medium",
                "execution_noise_level": "low",
                "multi_team_coordination": "low",
                "organizational_stage_signal": "growing"
            }
        }

        # Persona 1: VP R&D @ 100 (Execution Velocity)
        if "vp" in bio or "100" in bio:
            data.update({
                "company_category": "DevOps",
                "product_type": "Infrastructure",
                "business_model": "Enterprise License",
                "angle_signals": {
                    "delivery_pressure": "high",
                    "product_complexity": "high",
                    "team_structure": "squads",
                    "engineering_maturity": "high",
                    "decision_maker_level": "high",
                    "execution_noise_level": "medium",
                    "multi_team_coordination": "high",
                    "organizational_stage_signal": "scaleup"
                }
            })
            
        # Persona 2: Head of Eng @ 50 (Predictability)
        elif "head of" in bio:
            data.update({
                "company_category": "Fintech",
                "product_type": "Payments API",
                "business_model": "Transaction Fee",
                "angle_signals": {
                    "delivery_pressure": "high",
                    "product_complexity": "high",
                    "team_structure": "pods",
                    "engineering_maturity": "medium",
                    "decision_maker_level": "high",
                    "execution_noise_level": "high", # Trigger
                    "multi_team_coordination": "medium",
                    "organizational_stage_signal": "breaking"
                }
            })

        # Persona 3: CTO @ Startup (Firefighting)
        elif "cto" in bio:
            data.update({
                "company_category": "AI/ML",
                "product_type": "GenAI Tool",
                "business_model": "SaaS",
                "angle_signals": {
                    "delivery_pressure": "extreme",
                    "product_complexity": "high",
                    "team_structure": "flat",
                    "engineering_maturity": "low",
                    "decision_maker_level": "high",
                    "execution_noise_level": "extreme",
                    "multi_team_coordination": "low",
                    "organizational_stage_signal": "chaos"
                }
            })

        # Persona 4: Director Eng @ 200 (Team Health)
        elif "director" in bio:
            data.update({
                "company_category": "Enterprise Software",
                "product_type": "Mobile Platform",
                "business_model": "Seat-based",
                "angle_signals": {
                    "delivery_pressure": "medium",
                    "product_complexity": "medium",
                    "team_structure": "matrix",
                    "engineering_maturity": "high",
                    "decision_maker_level": "medium",
                    "execution_noise_level": "high", # Trigger
                    "multi_team_coordination": "high",
                    "organizational_stage_signal": "mature"
                }
            })
            
        # Persona 5: Product Lead (Strategic Clarity)
        elif "product" in bio:
            data.update({
                "company_category": "AI Data",
                "product_type": "Analytics",
                "business_model": "Usage-based",
                "angle_signals": {
                    "delivery_pressure": "high",
                    "product_complexity": "high",
                    "team_structure": "cross-functional",
                    "engineering_maturity": "high",
                    "decision_maker_level": "medium",
                    "execution_noise_level": "medium",
                    "multi_team_coordination": "medium",
                    "organizational_stage_signal": "scaleup"
                }
            })
            
        return json.dumps(data)

    def _mock_email_generation(self, prompt):
        # Identify Persona based on prompt content
        persona_key = "VP R&D" # Default
        if "Head of Engineering" in prompt: persona_key = "Head of Engineering"
        elif "CTO" in prompt: persona_key = "CTO"
        elif "Director of Engineering" in prompt: persona_key = "Director of Engineering"
        elif "Product Lead" in prompt: persona_key = "Product Lead"
        
        # Extract Pain from Prompt
        # Prompt format: "Pain: {pain_string}"
        pain_point = "generic pain"
        try:
            import re
            print(f"DEBUG: Prompt received:\n{prompt}")
            match = re.search(r"Pain: (.*)", prompt)
            if match:
                pain_point = match.group(1).strip()
                print(f"DEBUG: Extracted Pain: '{pain_point}'")
            else:
                print("DEBUG: No Pain match found!")
        except Exception as e:
            print(f"DEBUG: Regex Error: {e}")
            pass
        
        # Templates with placeholders
        templates = {
            "VP R&D": "Running a scaleup engineering org means you're dealing with {pain}. It's the silent killer of velocity.\n\nMost teams try to solve this with more process, but it only slows them further. You need visibility, not bureaucracy.\n\nOur Execution OS removes bottlenecks by creating flow across squads without adding weight. We connect the dots between strategy and code.\n\nWorth seeing how we do it?",
            "Head of Engineering": "When you have {pain}, the roadmap becomes a wish list rather than a plan. Your team is working hard, but delivery feels random.\n\nWe help you align engineering signals to business goals automatically, giving you a live view of reality.\n\nStop guessing and start delivering with confidence. It changes the conversation with the board.\n\nChat next week?",
            "CTO": "Firefighting isn't a strategy. It's a symptom of a system that can't handle {pain}. You're stuck in the weeds instead of building the future.\n\nWe build the fire station so you can focus on the architecture. We automate the incident response patterns.\n\nPrevent issues before they start. Get your time back.\n\nOpen to a demo?",
            "Director of Engineering": "Your best engineers aren't leaving because of money. They're leaving because of {pain}. They want to ship, not fight tools.\n\nNoise causes burnout. We reduce the noise and give them their focus back. We measure the friction points they can't see.\n\nCan I show you how we save your best talent?",
            "Product Lead": "Alignment is hard when you have {pain}. You ship features, but the platform rots.\n\nWe ensure every commit aligns with the roadmap. We link code changes to product specs automatically.\n\nKeep your product vision pure. Don't let technical debt kill your velocity.\n\nWorth 5 mins to see the link?"
        }
        
        base_body = templates.get(persona_key, templates["VP R&D"])
        return base_body.replace("{pain}", pain_point)
