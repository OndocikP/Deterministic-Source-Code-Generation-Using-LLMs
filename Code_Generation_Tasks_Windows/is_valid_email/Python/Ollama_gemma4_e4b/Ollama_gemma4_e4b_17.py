def is_valid_email(email: any) -> bool:
    """
    Validates an email address based on structural rules.

    Args:
        email: The input to validate.

    Returns:
        True if the email is structurally valid, False otherwise.
    """
    if not isinstance(email, str):
        return False

    if not email or email.strip() != email:
        return False

    if email.count('@') != 1:
        return False

    parts = email.split('@')
    local_part = parts[0]
    domain_part = parts[1]

    if not local_part or not domain_part:
        return False

    # Check for spaces or control characters (ASCII 0-31 and 127)
    if any(c in ' \t\n\r' or (ord(c) < 32 and ord(c) != 9) or ord(c) == 127 for c in email):
        return False

    # Local part validation
    # Reject consecutive dots
    if '..' in local_part:
        return False
    # Reject leading/trailing dots in local part (though the initial check handles overall whitespace)
    if local_part.startswith('.') or local_part.endswith('.'):
        return False

    # Domain part validation
    if not domain_part:
        return False

    domain_labels = domain_part.split('.')

    if len(domain_labels) < 2:
        # Must have at least one dot for a TLD (e.g., example.com)
        return False

    for label in domain_labels:
        if not label:
            # Handles consecutive dots in domain (e.g., example..com)
            return False
        if label.startswith('-') or label.endswith('-'):
            return False
        if not label.isalnum() and not (label.count('-') == 1 and label.replace('-', '').isalnum()):
            # Basic check: labels should primarily be alphanumeric or contain one hyphen internally
            # This is a simplification of RFC rules but covers the specified constraints.
            # We must ensure no spaces or control characters are present in labels.
            if any(c in ' ' for c in label) or any(ord(c) < 32 and ord(c) != 9 for c in label) or 127 in label:
                return False
            
            # A stricter check for allowed characters in domain labels (alphanumeric and hyphen)
            if not all(c.isalnum() or c == '-' for c in label):
                return False

    return True