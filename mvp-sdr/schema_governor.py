"""
MVSG: Minimum Viable Schema Governor

Enforces ONLY:
1. Type correctness
2. Critical field presence
3. Fail-safe replacements
4. Logging (warn, don't block)
"""

from contracts import NormalizedLead, AngleSignals, EmailOutput
from typing import Any, Dict, List


class ValidationResult:
    def __init__(self):
        self.warnings: List[str] = []
        self.corrections_applied: Dict[str, Any] = {}
        self.failed_safe: bool = False


class SchemaGovernor:
    def __init__(self):
        pass
    
    def validate_normalized_lead(self, lead: Any, lead_name: str = "Unknown") -> ValidationResult:
        """
        Validates NormalizedLead contract.
        
        Checks:
        - Type is NormalizedLead
        - first_name exists
        - company exists
        - angle_signals exists (all 8 fields)
        
        Returns ValidationResult with warnings and corrections.
        """
        result = ValidationResult()
        
        # 1. Type check
        if not isinstance(lead, NormalizedLead):
            result.warnings.append(f"[GOVERNOR] [WARN] EnrichmentAgent | Lead: {lead_name} | Type mismatch: expected NormalizedLead")
            result.failed_safe = True
            return result
        
        # 2. Critical field presence
        if not lead.first_name or lead.first_name.strip() == "":
            result.warnings.append(f"[GOVERNOR] [WARN] EnrichmentAgent | Lead: {lead_name} | Missing: first_name")
            lead.first_name = "Unknown"
            result.corrections_applied["first_name"] = "Unknown"
        
        if not lead.company or lead.company.strip() == "":
            result.warnings.append(f"[GOVERNOR] [WARN] EnrichmentAgent | Lead: {lead_name} | Missing: company")
            lead.company = "Unknown Company"
            result.corrections_applied["company"] = "Unknown Company"
        
        # 3. AngleSignals presence (all 8 fields)
        if not lead.angle_signals:
            result.warnings.append(f"[GOVERNOR] [WARN] EnrichmentAgent | Lead: {lead_name} | Missing: angle_signals | Applying defaults")
            lead.angle_signals = self._create_default_signals()
            result.corrections_applied["angle_signals"] = "default"
        else:
            # Check all 8 fields exist
            required_signals = [
                "delivery_pressure",
                "product_complexity",
                "team_structure",
                "engineering_maturity",
                "decision_maker_level",
                "execution_noise_level",
                "multi_team_coordination",
                "organizational_stage_signal"
            ]
            
            for signal in required_signals:
                if not hasattr(lead.angle_signals, signal) or getattr(lead.angle_signals, signal) is None:
                    result.warnings.append(f"[GOVERNOR] [WARN] EnrichmentAgent | Lead: {lead_name} | Missing signal: {signal}")
                    # Apply default
                    default_value = self._get_default_signal_value(signal)
                    setattr(lead.angle_signals, signal, default_value)
                    result.corrections_applied[f"angle_signals.{signal}"] = default_value
        
        return result
    
    def validate_email_output(self, email: Any, lead_name: str = "Unknown") -> ValidationResult:
        """
        Validates EmailOutput contract.
        
        Checks:
        - Type is EmailOutput
        - subject exists
        - body exists
        
        Returns ValidationResult with warnings and corrections.
        """
        result = ValidationResult()
        
        # 1. Type check
        if not isinstance(email, EmailOutput):
            result.warnings.append(f"[GOVERNOR] [WARN] EmailWriter | Lead: {lead_name} | Type mismatch: expected EmailOutput")
            result.failed_safe = True
            return result
        
        # 2. Critical field presence
        if not email.subject or email.subject.strip() == "":
            result.warnings.append(f"[GOVERNOR] [WARN] EmailWriter | Lead: {lead_name} | Missing: subject | Applying fallback")
            email.subject = "Regarding Your Engineering Execution"
            result.corrections_applied["subject"] = "fallback"
        
        if not email.body or email.body.strip() == "":
            result.warnings.append(f"[GOVERNOR] [WARN] EmailWriter | Lead: {lead_name} | Missing: body | Applying fallback")
            email.body = self._create_fallback_email_body()
            result.corrections_applied["body"] = "fallback"
        
        return result
    
    def _create_default_signals(self) -> AngleSignals:
        """SRD-01 compliant defaults"""
        return AngleSignals(
            delivery_pressure="medium",
            product_complexity="medium",
            team_structure="functional",
            engineering_maturity="medium",
            decision_maker_level="low",
            execution_noise_level="low",
            multi_team_coordination="low",
            organizational_stage_signal="growing"
        )
    
    def _get_default_signal_value(self, signal_name: str) -> str:
        """Get default value for a specific signal"""
        defaults = {
            "delivery_pressure": "medium",
            "product_complexity": "medium",
            "team_structure": "functional",
            "engineering_maturity": "medium",
            "decision_maker_level": "low",
            "execution_noise_level": "low",
            "multi_team_coordination": "low",
            "organizational_stage_signal": "growing"
        }
        return defaults.get(signal_name, "medium")
    
    def _create_fallback_email_body(self) -> str:
        """Safe fallback email template"""
        return """Your team is working hard, but execution feels unpredictable.

We help engineering leaders create visibility and flow across their teams without adding process weight.

Worth a quick conversation?"""
    
    def log_validation_result(self, result: ValidationResult):
        """Print warnings to console"""
        for warning in result.warnings:
            print(warning)
