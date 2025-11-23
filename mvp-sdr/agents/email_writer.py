from agents.hook_engine import HookEngine
from contracts import EmailOutput


class EmailWriter:
    def run(self, normalized_lead, primary_pain, angle):
        """
        Input: NormalizedLead, primary_pain (str), angle (str)
        Output: EmailOutput object
        """
        hook_engine = HookEngine()
        hook = hook_engine.run(normalized_lead, angle)
        
        # Phase 4: LLM Generation (Tier 1)
        from llm_adapter import LLMAdapter
        adapter = LLMAdapter()
        
        prompt = f"""
        Write a cold email to {normalized_lead.first_name} ({normalized_lead.role_title} at {normalized_lead.company}).
        Angle: {angle}
        Hook: {hook}
        Pain: {primary_pain}
        
        Constraint: Under 120 words. Direct, senior tone. No fluff.
        """
        
        try:
            # Tier 1 = Pro Model
            email_body = adapter.call(prompt, tier="tier1", schema=False)
            
            # Mock Subject for now (since LLM returns string)
            subject = f"Regarding {angle}" 
            
        except Exception as e:
            print(f"LLM Writing Failed: {e}. Falling back to templates.")
            # Fallback to Templates (Phase 3 Logic)
            templates = {
                "Predictability": {
                    "subject": "Predictability > Speed",
                    "body": f"{hook}\n\nMost leaders trade speed for predictability. You don't have to.\n\nOur system aligns engineering signals automatically.\n\nWorth a chat?"
                },
                # ... (Keep other templates or simplify fallback)
                "Execution Velocity": {
                    "subject": "Speed without breaking things",
                    "body": f"{hook}\n\nFriction kills velocity. We remove the friction.\n\nOur Execution OS connects the dots.\n\nOpen to seeing how?"
                }
            }
            default_template = {
                "subject": "Engineering Efficiency",
                "body": f"{hook}\n\nWe help teams move faster.\n\nWorth a look?"
            }
            content = templates.get(angle, default_template)
            subject = content["subject"]
            email_body = content["body"]
        
        return EmailOutput(
            subject=subject,
            body=email_body,
            angle_used=angle,
            tokens=len(email_body.split())
        )
