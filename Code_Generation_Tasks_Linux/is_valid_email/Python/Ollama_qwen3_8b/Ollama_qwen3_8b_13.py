def is_valid_email(email: str | None) -> bool:
    """
    Validates an email address according to specific rules.
    """
    if not isinstance(email, str) or email is None or email.strip() != email:
        return False

    if "@" not in email:
        return False

    local_part, domain_part = email.split("@", 1)
    if email.count("@") != 1:
        return False

    if not local_part or not domain_part:
        return False

    if ".." in local_part:
        return False

    if local_part[0] == "." or local_part[-1] == ".":
        return False

    if not domain_part:
        return False

    if domain_part[0] == "-" or domain_part[-1] == "-":
        return False

    if "." in domain_part:
        domain_labels = domain_part.split(".")
        for label in domain_labels:
            if not label or len(label) > 63 or not label.isalnum() or label.count("-") > 0:
                return False
    else:
        if not domain_part.isalnum():
            return False

    return True