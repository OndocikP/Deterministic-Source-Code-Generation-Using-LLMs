def is_valid_email(email: str) -> bool:
    """
    Validate an email address according to RFC 5322.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: Whether the email address is valid.
    """
    if not isinstance(email, str):
        return False
    if not email.strip():
        return False
    if "@" not in email or email.count("@") != 1:
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
    if local_part.count(".") > 0:
        return False
    if domain.count(".") == 0:
        return False
    if domain.count(".") > 2:
        return False
    if domain[-1] == "-":
        return False
    return True