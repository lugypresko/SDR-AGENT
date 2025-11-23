def route_angle(enrichment, primary_pain):
    """
    Input: enrichment dict, primary_pain str
    Output: angle_name (str)
    """
    # Deterministic Rule
    if "delivery" in primary_pain or "tooling" in primary_pain:
        return "Execution OS"
    else:
        return "Product Ops"
