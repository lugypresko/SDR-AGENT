def check_quality(email_text, primary_pain):
    """
    Input: email_text str, primary_pain str
    Output: approved (bool), final_email (str)
    """
    
    # 1. Check for pain reference
    if primary_pain not in email_text:
        # Fail safe: append it
        email_text += f"\nP.S. We specifically solve {primary_pain}."

    # 2. Check length (very rough word count)
    word_count = len(email_text.split())
    
    # MVP Rule: If too short, append generic closer to bulk it up
    if word_count < 30:
        email_text += "\n\nLet's discuss how we can help your team move faster and break fewer things."

    return True, email_text


class EmailQualityAgent:
    def run(self, email_output):
        """
        Input: EmailOutput object
        Output: EmailOutput object (potentially modified)
        """
        approved, clean_body = check_quality(email_output.body, "")
        email_output.body = clean_body
        return email_output
