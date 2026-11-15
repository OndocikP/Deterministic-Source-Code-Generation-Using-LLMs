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

    # Check for consecutive dots in local part
    if '..' in local_part:
        return False

    # Local part validation: must not contain invalid characters (only letters, digits, ., _, -)
    # We are restricted from using regex for complexity, so we check characters allowed by common standards
    # and explicitly reject spaces/control chars already checked.
    for char in local_part:
        if not (char.isalnum() or char in '._-'):
            return False

    # Domain part validation
    domain_labels = domain_part.split('.')
    if not domain_labels:
        return False

    for label in domain_labels:
        if not label:
            # Handles leading/trailing dots in domain, e.g., ".example.com" or "example."
            return False
        if label.startswith('-') or label.endswith('-'):
            return False
        if not label.isalnum() and '-' not in label:
            # Must contain only alphanumeric characters or hyphens
            return False
        if '--' in label:
            return False

    # TLD check (simplistic: must have at least one label after the last dot, and that label must not be empty)
    if not domain_labels[-1]:
        return False

    # Check for consecutive dots in domain part
    if '..' in domain_part:
        return False

    return True