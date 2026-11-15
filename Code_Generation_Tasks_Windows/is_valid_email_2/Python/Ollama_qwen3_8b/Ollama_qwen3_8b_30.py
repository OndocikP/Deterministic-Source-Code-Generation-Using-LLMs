from typing import Optional

def is_valid_email(email: Optional[str]) -> bool:
    """
    Validates an email address according to specific rules.
    Returns True if the email is valid, False otherwise.
    """
    if not isinstance(email, str) or email.strip() != email:
        return False
    if not email:
        return False
    if email.count('@') != 1:
        return False
    local_part, domain = email.split('@')
    if '..' in local_part or local_part.startswith('.') or local_part.endswith('.'):
        return False
    if not domain or domain.count('.') < 1 or domain.startswith('-') or domain.endswith('-'):
        return False
    domain_parts = domain.split('.')
    for part in domain_parts:
        if not part or not part.isalnum() or part.startswith('-') or part.endswith('-') or '--' in part:
            return False
    return True