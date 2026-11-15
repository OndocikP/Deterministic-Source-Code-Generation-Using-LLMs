import re

def is_valid_email(email: str) -> bool:
    """
    Validate an email address according to the given rules.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    if not isinstance(email, str) or email is None:
        return False

    email = email.strip()
    if not email:
        return False

    pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    if not pattern.match(email):
        return False

    local_part, domain = email.split('@', 1)
    if not local_part or not domain:
        return False

    if re.search(r'\.\.|[@ ]', local_part):
        return False

    domain_labels = domain.split('.')
    for label in domain_labels:
        if not label.isalnum() or re.match(r'^-|-$', label):
            return False

    return True