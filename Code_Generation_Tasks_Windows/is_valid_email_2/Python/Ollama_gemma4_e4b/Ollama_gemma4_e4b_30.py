def is_valid_email(email: any) -> bool:
    """
    Validates an email address based on structural rules.
    """
    if not isinstance(email, str) or not email:
        return False
    if email != email.strip():
        return False
    if ' ' in email or any(c in email for c in ['\t', '\n', '\r']):
        return False

    parts = email.split('@')
    if len(parts) != 2:
        return False

    local_part, domain_part = parts

    if not local_part or not domain_part:
        return False

    # Local part validation
    if '..' in local_part:
        return False
    if any(c in local_part for c in ['@', ' ']): # Redundant check for ' ', but ensures no other invalid chars
        return False

    # Domain part validation
    if '.' not in domain_part:
        return False

    domain_labels = domain_part.split('.')
    if not domain_labels:
        return False

    for label in domain_labels:
        if not label:
            return False
        if label.startswith('-') or label.endswith('-'):
            return False
        if label.count('-') > 1:
            return False
        if not all('a' <= char <= 'z' or '0' <= char <= '9' or char == '-' for char in label):
            return False

    # Check for overall character validity (excluding structure handled above)
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-@")
    if not all(c in allowed_chars for c in email):
        return False

    return True