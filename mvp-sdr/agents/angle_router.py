class AngleRouter:
    def run(self, normalized_lead, primary_pain):
        """
        SRD-01 Phase 3: Deterministic Pain -> Angle Mapping
        
        Input: NormalizedLead object, primary_pain str
        Output: angle_name (str)
        """
        
        # Deterministic mapping as per SRD-01
        mapping = {
            "firefighting spiral": "Firefighting Spiral",
            "silent attrition": "Team Health",
            "cross-team flow collapse": "Execution Velocity",
            "too many initiatives": "Predictability",
            "architecture drift": "Strategic Clarity",
            "no delegation layer": "Team Foundations",
            "execution friction": "Execution Velocity"
        }
        
        # Return mapped angle or safe fallback
        angle = mapping.get(primary_pain, "Execution Velocity")
        
        # Debug print (SRD-01 Phase 5)
        print(f"ANGLE SELECTED for {normalized_lead.first_name}: {angle} (from pain: {primary_pain})")
        
        return angle
