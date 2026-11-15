from typing import Union

def is_valid_email(email: Union[str, None]) -> bool:
    """
    Validate an email address according to specified rules.
    
    Returns True if the email is valid, otherwise False.
    """
    if not isinstance(email, str) or not email:
        return False
    
    # Split the email into local and domain parts
    parts = email.split('@')
    
    # Check for exactly one '@' symbol
    if len(parts) != 2:
        return False
    
    local, domain = parts
    
    # Check for leading or trailing whitespace
    if local.startswith(' ') or local.endswith(' ') or domain.startswith(' ') or domain.endswith(' '):
        return False
    
    # Check for spaces or control characters
    if any(c.isspace() or ord(c) < 32 or ord(c) > 126 for c in email):
        return False
    
    # Validate local part
    if not local or consecutive_dots(local) or local.startswith('.') or local.endswith('.'):
        return False
    
    # Validate domain
    if not domain or domain.startswith('-') or domain.endswith('-') or '.' not in domain:
        return False
    
    domain_parts = domain.split('.')
    if any(not part or part.startswith('-') or part.endswith('-') or not all(c.isalnum() or c == '-' for c in part) for part in domain_parts):
        return False
    
    return True

def consecutive_dots(s: str) -> bool:
    return '..' in s