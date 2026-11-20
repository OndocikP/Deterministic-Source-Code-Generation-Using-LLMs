def is_valid_email(email: str | None) -> bool:
    """
    Validates an email address according to specific rules.
    """
    if not isinstance(email, str) or email.strip() != email:
        return False
    if not email:
        return False
    if email.count('@') != 1:
        return False
    local_part, domain = email.split('@')
    if '..' in local_part:
        return False
    if not local_part or not domain:
        return False
    if domain.startswith('-') or domain.endswith('-'):
        return False
    if '-' in domain:
        if domain.split('-')[0] == '' or domain.split('-')[-1] == '':
            return False
    if not domain.replace('.', '').isalnum():
        return False
    if not local_part.replace('.', '').isalnum():
        return False
    return True