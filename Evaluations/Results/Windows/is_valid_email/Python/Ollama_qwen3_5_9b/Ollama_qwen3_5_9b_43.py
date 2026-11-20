def is_valid_email(email):
    """
    Validates an email address according to RFC 5322 simplified rules.
    
    Args:
        email (str | None | any): The email address to validate.
        
    Returns:
        bool: True if the email is valid, False otherwise.
    """
    # Check type
    if not isinstance(email, str):
        return False
    
    # Check for empty string or leading/trailing whitespace
    if email == "" or email != email.strip():
        return False
    
    # Split into local and domain parts
    if "@" not in email:
        return False
    
    at_count = email.count("@")
    if at_count != 1:
        return False
    
    local_part, domain = email.split("@")
    
    # Validate local part
    if len(local_part) == 0 or len(domain) == 0:
        return False
    
    # Check for spaces or control characters in the entire string
    for char in email:
        if char.isspace() or ord(char) < 32 or ord(char) == 127:
            return False
    
    # Local part rules: no consecutive dots, cannot start/end with dot
    if local_part.startswith(".") or local_part.endswith("."):
        return False
    
    if ".." in local_part:
        return False
    
    # Domain rules: must have at least one dot, labels cannot start/end with hyphen
    if "." not in domain:
        return False
    
    labels = domain.split(".")
    
    for label in labels:
        if len(label) == 0:
            return False
        
        if label.startswith("-") or label.endswith("-"):
            return False
        
        # Domain labels should be alphanumeric with hyphens allowed in between
        if not all(c.isalnum() or c == "-" for c in label):
            return False
    
    return True