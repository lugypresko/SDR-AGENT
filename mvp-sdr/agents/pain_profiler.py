class PainProfiler:
    def run(self, nl):
        """
        Input: NormalizedLead object
        Output: primary_pain (str)
        
        Hierarchical priority-based pain profiling.
        Meta-rule: First match wins (if-elif chain ensures determinism).
        """

        # Safety: if enrichment failed
        if not nl.angle_signals:
            return "execution friction"

        s = nl.angle_signals  # shorthand

        # Priority 1: Extreme Chaos Signals
        # Persona: CTO
        if (
            getattr(s, "execution_noise_level", "") == "extreme"
            or getattr(s, "organizational_stage_signal", "") == "chaos"
        ):
            return "firefighting spiral"

        # Priority 2: Organizational Maturity Signals
        # Persona: Director
        elif (
            getattr(s, "team_structure", "") == "matrix"
            and getattr(s, "execution_noise_level", "") == "high"
        ):
            return "silent attrition"

        # Priority 3: Coordination Complexity Signals
        # Persona: VP R&D
        elif (
            getattr(s, "multi_team_coordination", "") == "high"
            or getattr(s, "team_structure", "") == "squads"
        ):
            return "cross-team flow collapse"

        # Priority 4: Breaking Point Signals
        # Persona: Head of Eng
        elif (
            getattr(s, "organizational_stage_signal", "") == "breaking"
            and getattr(s, "execution_noise_level", "") == "high"
        ):
            return "too many initiatives"

        # Priority 5: Strategic Alignment Signals
        # Persona: Product Lead
        elif (
            getattr(s, "team_structure", "") == "cross-functional"
            or getattr(s, "organizational_stage_signal", "") == "scaleup"
        ):
            return "architecture drift"

        # Priority 6: Delegation Gap Signals
        # (Fallback for flat + low maturity, should not hit with current mock)
        elif (
            getattr(s, "team_structure", "") == "flat"
            and getattr(s, "engineering_maturity", "") == "low"
        ):
            return "no delegation layer"

        # Default Fallback (should never hit with current MockLLMProvider)
        else:
            return "execution friction"

