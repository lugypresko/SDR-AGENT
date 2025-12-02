class PainProfiler:
    """
    Pain Profiler (CSE Phase 7 - "Dumb" Mode)
    
    Returns ALL pain candidates and pattern matches.
    The CSE will use this to compute pain strength and explain reasoning.
    """
    def run(self, nl):
        """
        Input: NormalizedLead object
        Output: dict with pain_candidates, raw_fragments, pattern_matches, primary_pain
        """

        # Safety: if enrichment failed
        if not nl.angle_signals:
            return {
                "pain_candidates": ["execution friction"],
                "raw_fragments": [],
                "pattern_matches": {},
                "primary_pain": "execution friction"
            }

        s = nl.angle_signals  # shorthand
        
        # Collect all matched pains (not just first match)
        pain_candidates = []
        pattern_matches = {}

        # Priority 1: Extreme Chaos Signals
        if (
            getattr(s, "execution_noise_level", "") == "extreme"
            or getattr(s, "organizational_stage_signal", "") == "chaos"
        ):
            pain_candidates.append("firefighting spiral")
            pattern_matches["firefighting spiral"] = {
                "execution_noise_level": getattr(s, "execution_noise_level", ""),
                "organizational_stage_signal": getattr(s, "organizational_stage_signal", "")
            }

        # Priority 2: Organizational Maturity Signals
        if (
            getattr(s, "team_structure", "") == "matrix"
            and getattr(s, "execution_noise_level", "") == "high"
        ):
            pain_candidates.append("silent attrition")
            pattern_matches["silent attrition"] = {
                "team_structure": getattr(s, "team_structure", ""),
                "execution_noise_level": getattr(s, "execution_noise_level", "")
            }

        # Priority 3: Coordination Complexity Signals
        if (
            getattr(s, "multi_team_coordination", "") == "high"
            or getattr(s, "team_structure", "") == "squads"
        ):
            pain_candidates.append("cross-team flow collapse")
            pattern_matches["cross-team flow collapse"] = {
                "multi_team_coordination": getattr(s, "multi_team_coordination", ""),
                "team_structure": getattr(s, "team_structure", "")
            }

        # Priority 4: Breaking Point Signals
        if (
            getattr(s, "organizational_stage_signal", "") == "breaking"
            and getattr(s, "execution_noise_level", "") == "high"
        ):
            pain_candidates.append("too many initiatives")
            pattern_matches["too many initiatives"] = {
                "organizational_stage_signal": getattr(s, "organizational_stage_signal", ""),
                "execution_noise_level": getattr(s, "execution_noise_level", "")
            }

        # Priority 5: Strategic Alignment Signals
        if (
            getattr(s, "team_structure", "") == "cross-functional"
            or getattr(s, "organizational_stage_signal", "") == "scaleup"
        ):
            pain_candidates.append("architecture drift")
            pattern_matches["architecture drift"] = {
                "team_structure": getattr(s, "team_structure", ""),
                "organizational_stage_signal": getattr(s, "organizational_stage_signal", "")
            }

        # Priority 6: Delegation Gap Signals
        if (
            getattr(s, "team_structure", "") == "flat"
            and getattr(s, "engineering_maturity", "") == "low"
        ):
            pain_candidates.append("no delegation layer")
            pattern_matches["no delegation layer"] = {
                "team_structure": getattr(s, "team_structure", ""),
                "engineering_maturity": getattr(s, "engineering_maturity", "")
            }

        # Default Fallback
        if not pain_candidates:
            pain_candidates.append("execution friction")

        # Primary pain is the first match (highest priority)
        primary_pain = pain_candidates[0]

        return {
            "pain_candidates": pain_candidates,
            "raw_fragments": [],  # Placeholder for future text extraction
            "pattern_matches": pattern_matches,
            "primary_pain": primary_pain
        }
