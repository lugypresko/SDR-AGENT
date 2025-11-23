def enrich_lead(row):
    """
    Input: CSV row dict
    Output: dict with company_size, company_category, challenges, signals
    """
    bio = row.get('linkedin_bio', '').lower()
    company = row.get('company', '').lower()
    employees = int(row.get('employees', 0))

    # Deterministic Category Logic
    if 'platform' in bio or 'platform' in company:
        category = "Platform"
    elif 'security' in bio or 'cyber' in bio:
        category = "Cyber"
    elif 'fintech' in bio or 'payments' in bio:
        category = "Fintech"
    elif 'app' in bio or 'mobile' in bio:
        category = "AppDev"
    else:
        category = "SaaS"

    # Deterministic Size Logic
    if employees < 50:
        size_str = "Startup"
    elif employees < 200:
        size_str = "Scaleup"
    else:
        size_str = "Enterprise"

    return {
        "company_size": size_str,
        "company_category": category,
        "challenges": "scaling pains", # Placeholder for MVP
        "signals": "hiring aggressively" # Placeholder for MVP
    }
