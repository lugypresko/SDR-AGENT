def write_email(enrichment, primary_pain, angle):
    """
    Input: enrichment dict, primary_pain str, angle str
    Output: email string
    """
    company_size = enrichment.get('company_size')
    
    if angle == "Execution OS":
        return f"""
Subject: Fixing {primary_pain}

I noticed you're running a {company_size} engineering team. usually that means you're battling {primary_pain}.

Most leaders try to solve this with more process, but that just slows things down.

We built an Execution OS that eliminates {primary_pain} without adding bureaucracy.

Worth a chat?
"""
    else: # Product Ops
        return f"""
Subject: Better than Product Ops

Running a {company_size} org often leads to {primary_pain}.

Instead of hiring a Product Ops team to manage the chaos, you can automate the context.

Our system solves {primary_pain} by connecting the dots automatically.

Open to seeing how?
"""
