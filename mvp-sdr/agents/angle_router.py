class AngleRouter:
    """
    Angle Router (CSE Phase 7 - "Dumb" Mode)
    
    Returns ALL candidate angles and the final selection.
    The CSE will use this to explain why alternatives were rejected.
    """
    def run(self, normalized_lead, primary_pain):
        """
        Input: NormalizedLead object, primary_pain str
        Output: dict with candidate_angles, rejected_angles, selected_angle, raw_patterns
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
        
        # Get selected angle
        selected_angle = mapping.get(primary_pain, "Execution Velocity")
        
        # All possible angles (candidates)
        all_angles = list(set(mapping.values()))
        
        # Rejected angles (all except selected)
        rejected_angles = [a for a in all_angles if a != selected_angle]
        
        # Debug print (SRD-01 Phase 5)
        print(f"ANGLE SELECTED for {normalized_lead.first_name}: {selected_angle} (from pain: {primary_pain})")
        
        # Return raw data for CSE
        return {
            "candidate_angles": all_angles,
            "rejected_angles": rejected_angles,
            "selected_angle": selected_angle,
            "raw_patterns": {
                "pain_to_angle_mapping": mapping,
                "matched_pain": primary_pain
            }
        }
