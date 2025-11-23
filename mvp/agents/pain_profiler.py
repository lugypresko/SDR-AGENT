def profile_pain(enrichment):
    """
    Input: enrichment dict
    Output: primary_pain (str)
    """
    category = enrichment.get('company_category')

    # Deterministic Mapping Table
    mapping = {
        "SaaS": "delivery bottlenecks",
        "Platform": "context switching",
        "Cyber": "alert fatigue",
        "Fintech": "compliance overhead",
        "AppDev": "fragmented tooling"
    }

    return mapping.get(category, "generic efficiency gaps")
