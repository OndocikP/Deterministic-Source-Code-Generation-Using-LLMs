import re

def is_valid_email(email: str) -> bool:
    if not isinstance(email, str) or not email.strip():
        return False
    
    email_regex = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    
    if not email_regex.match(email):
        return False
    
    local_part, domain = email.split('@')
    
    if '..' in local_part or local_part.startswith('.') or local_part.endswith('.'):
        return False
    
    domain_labels = domain.split('.')
    
    if any(label.startswith('-') or label.endswith('-') for label in domain_labels):
        return False
    
    return True