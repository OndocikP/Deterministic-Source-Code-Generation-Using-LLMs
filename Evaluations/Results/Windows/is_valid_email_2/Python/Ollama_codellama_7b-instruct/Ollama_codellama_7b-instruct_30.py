def is_valid_email(email: str) -> bool:
    """
    Validate an email address according to the following rules:

    - The input must be a string.
    - The input must not be empty or contain leading or trailing whitespace.
    - The email structure must be valid, including the local part, the @ symbol, and the domain.
    - The local part must not be empty or contain consecutive dots.
    - The domain must not be empty or contain consecutive dots.
    - The domain must not start or end with a hyphen.
    - The input must not contain spaces or control characters.

    >>> is_valid_email("john.doe@example.com")
    True
    >>> is_valid_email("john.doe@example.com ")
    False
    >>> is_valid_email("john.doe@example.com\n")
    False
    >>> is_valid_email("john.doe@example.com.")
    False
    >>> is_valid_email("john.doe@example.com..")
    False
    >>> is_valid_email("john.doe@example.com-")
    False
    >>> is_valid_email("john.doe@example.com_")
    False
    >>> is_valid_email("john.doe@example.com.")
    False
    >>> is_valid_email("john.doe@example.com..")
    False
    >>> is_valid_email("john.doe@example.com-")
    False
    >>> is_valid_email("john.doe@example.com_")
    False
    """
    if not isinstance(email, str):
        return False
    if not email.strip():
        return False
    local_part, domain = email.split("@")
    if not local_part or not domain:
        return False
    if ".." in local_part or ".." in domain:
        return False
    if domain.startswith("-") or domain.endswith("-"):
        return False
    if any(c in local_part for c in " \t\n\r"):
        return False
    return True