import re

def is_valid_email(email: object) -> bool:
    """Validates an email address based on strict structural rules."""
    if not isinstance(email, str) or not email:
        return False

    if email != email.strip():
        return False

    if "@" not in email or email.count("@") != 1:
        return False

    local_part, domain = email.split("@")

    if not local_part or not domain:
        return False

    if ".." in local_part:
        return False

    if not re.match(r"^[a-zA-Z0-9!#$%&'*+/=?^_`{|}~.-]+$", local_part):
        return False

    if local_part.startswith(".") or local_part.endswith("."):
        return False

    domain_labels = domain.split(".")
    if len(domain_labels) < 2:
        return False

    for label in domain_labels:
        if not label or not re.match(r"^[a-zA-Z0-9-]+$", label):
            return False
        if label.startswith("-") or label.endswith("-"):
            return False

    return True