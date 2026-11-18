import re

def is_valid_email(email: object) -> bool:
    """Validates an email address based on strict structural rules."""
    if not isinstance(email, str) or not email:
        return False

    if email != email.strip():
        return False

    if any(ord(c) < 33 or ord(c) > 126 for c in email):
        return False

    if email.count('@') != 1:
        return False

    local_part, domain = email.split('@')

    if not local_part or not domain:
        return False

    if local_part.startswith('.') or local_part.endswith('.') or '..' in local_part:
        return False

    if not re.match(r'^[a-zA-Z0-9!#$%&\'*+/=?^_`{|}~.-]+$', local_part):
        return False

    domain_parts = domain.split('.')
    if len(domain_parts) < 2:
        return False

    for part in domain_parts:
        if not part or part.startswith('-') or part.endswith('-') or not re.match(r'^[a-zA-Z0-9-]+$', part):
            return False

    return True