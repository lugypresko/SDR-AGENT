class HookEngine:
    def run(self, normalized_lead, angle):
        """
        Input: NormalizedLead, Angle (str)
        Output: hook_text (str)
        
        Logic: Hierarchical Fallback
        1. Exact Match: (Role, Stage, Angle)
        2. Partial Match: (Stage, Angle)
        3. Default: (Angle)
        """
        role = normalized_lead.role_seniority # executive, senior-lead, manager, ic
        stage = normalized_lead.company_stage # startup, scaleup, growth, enterprise
        
        # 1. Exact Match Database (Role + Stage + Angle)
        exact_hooks = {
            ("executive", "breaking", "Predictability"): "Teams move fast but the system doesn't keep up. That's when predictability breaks.",
            ("executive", "scaleup", "Delivery Stability"): "Your org hits the point where alignment becomes more expensive than the code.",
            ("senior-lead", "complex", "Strategy-to-Execution Gap"): "When surface area expands, decision-making slows down unless you constrain the work.",
        }
        
        # 2. Partial Match Database (Stage + Angle)
        partial_hooks = {
            ("startup", "Execution Velocity"): "At this stage, speed is oxygen, but process is the enemy.",
            ("scaleup", "Predictability"): "Scaling breaks things, usually starting with the roadmap.",
            ("growth", "Cross-Team Flow"): "Silos start to form naturally when you cross the 100-person mark.",
            ("enterprise", "Multi-Initiative Management"): "Managing dependencies across this many teams is a full-time job.",
        }
        
        # 3. Default Angle Hooks (Fallback)
        default_hooks = {
            "Predictability": "Engineering leaders often trade speed for predictability, but you shouldn't have to.",
            "Execution Velocity": "Most teams slow down as they grow, but it's not inevitable.",
            "Cross-Team Flow": "Dependencies kill momentum more than bad code ever could.",
            "Team Health": "Burnout doesn't happen overnight; it happens when friction becomes normal.",
            "Strategic Clarity": "The gap between strategy and execution is where value gets lost.",
            "Firefighting Spiral": "If you're always fighting fires, you can't build the fire station.",
            "Silent Attrition": "The best engineers leave when they feel blocked, not when they're overworked.",
            "Rebuild Trust": "Trust erodes when delivery slips, and it's hard to earn back.",
        }
        
        # Lookup Logic
        key_exact = (role, stage, angle)
        key_partial = (stage, angle)
        
        if key_exact in exact_hooks:
            return exact_hooks[key_exact]
        elif key_partial in partial_hooks:
            return partial_hooks[key_partial]
        else:
            return default_hooks.get(angle, "We help engineering teams move faster.")
