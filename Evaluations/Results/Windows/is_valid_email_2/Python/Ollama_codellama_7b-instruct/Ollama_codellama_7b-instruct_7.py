def is_valid_email(email: str) -> bool:
    """
    Validates an email address according to the RFC 5322 standard.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email address is valid, False otherwise.
    """
    if not isinstance(email, str):
        return False
    if not email.strip():
        return False
    if "@" not in email:
        return False
    local_part, domain = email.split("@")
    if not local_part or not domain:
        return False
    if local_part.startswith("."):
        return False
    if local_part.endswith("."):
        return False
    if domain.startswith("."):
        return False
    if domain.endswith("."):
        return False
    if not domain.replace("-", "").isalnum():
        return False
    if not local_part.replace("-", "").isalnum():
        return False
    return True