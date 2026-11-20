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
    
    # Check for empty local or domain parts
    if not local or not domain:
        return False
    
    # Validate local part
    if '..' in local or local.startswith('.') or local.endswith('.'):
        return False
    
    # Validate domain part
    if '..' in domain or domain.startswith('-') or domain.endswith('-'):
        return False
    
    # Check for valid domain labels
    if not all(label and all(c.isalnum() or c in '-.' for c in label) for label in domain.split('.')):
        return False
    
    return True