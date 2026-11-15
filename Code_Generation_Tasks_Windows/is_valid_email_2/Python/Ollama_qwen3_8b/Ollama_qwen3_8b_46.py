def is_valid_email(email: str | None) -> bool:
    """
    Validates an email address according to strict rules.
    """
    if not isinstance(email, str) or email == '':
        return False
    if email.strip() != email:
        return False
    if email.count('@') != 1:
        return False
    local_part, domain_part = email.split('@')
    if '..' in local_part:
        return False
    if not local_part or not domain_part:
        return False
    if domain_part[0] == '-' or domain_part[-1] == '-':
        return False
    if '-' in domain_part and domain_part.index('-') == 0:
        return False
    if '-' in domain_part and domain_part.rfind('-') == len(domain_part) - 1:
        return False
    domain_parts = domain_part.split('.')
    for part in domain_parts:
        if not part or len(part) < 1 or len(part) > 63:
            return False
        if not part.isalnum() and '-' not in part:
            return False
    return True