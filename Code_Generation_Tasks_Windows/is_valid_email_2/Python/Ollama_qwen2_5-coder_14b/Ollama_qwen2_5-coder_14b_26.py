import re
from typing import Any

def is_valid_email(email: Any) -> bool:
    """
    Validates an email address according to specified rules.
    
    Args:
    email (Any): The email address to validate.
    
    Returns:
    bool: True if the email is valid, False otherwise.
    """
    if not isinstance(email, str):
        return False
    
    if not email or email.strip() != email:
        return False
    
    email_regex = re.compile(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    )
    
    if email_regex.match(email):
        local_part, domain = email.split('@')
        if ".." in local_part or local_part.startswith('.') or local_part.endswith('.'):
            return False
        domain_labels = domain.split('.')
        if any(label.startswith('-') or label.endswith('-') or not label for label in domain_labels):
            return False
        return True
    
    return False