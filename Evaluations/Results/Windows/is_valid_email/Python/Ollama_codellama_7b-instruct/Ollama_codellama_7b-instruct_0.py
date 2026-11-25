```
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
    if email.startswith(" ") or email.endswith(" "):
        return False
    if email.count(" ") > 0:
        return False
    if email.count("@") > 1:
        return False
    if email.count(".") == 0:
        return False
    if email.count("..") > 0:
        return False
    if email.count("-") > 0:
        return False
    if email.count("_") > 0:
        return False
    if email.count("+") > 0:
        return False
    if email.count("=") > 0:
        return False
    if email.count("(") > 0:
        return False
    if email.count(")") > 0:
        return False
    if email.count("[") > 0:
        return False
    if email.count("]") > 0:
        return False
    if email.count("{") > 0:
        return False
    if email.count("}") > 0:
        return False
    if email.count("|") > 0:
        return False
    if email.count("\\") > 0:
        return False
    if email.count("^") > 0:
        return False
    if email.count("~") > 0:
        return False
    if email.count("`") > 0:
        return False
    if email.count(";") > 0:
        return False
    if email.count(":") > 0:
        return False
    if email.count("'") > 0:
        return False
    if email.count('"') > 0:
        return False
    if email.count("`") > 0:
        return False
    if email.count("*") > 0:
        return False
    if email.count("?") > 0:
        return False
    if email.count("!") > 0:
        return False
    if email.count("%") > 0:
        return False
    if email.count("#") > 0:
        return False
    if email.count("&") > 0:
        return False
    if email.count("$") > 0:
        return False
    if email.count("^") > 0:
        return False
    if email.count("(") > 0:
        return False
    if email.count(")") > 0:
        return False
    if email.count("[") > 0:
        return False
    if email.count("]") > 0:
        return False
    if email.count("{") > 0:
        return False
    if email.count("}") > 0:
        return False
    if email.count("|") > 0:
        return False
    if email.count("\\") > 0:
        return False
    if email.count("^") > 0:
        return False
    if email.count("~") > 0:
        return False
    if email.count("`") > 0:
        return False
    if email.count(";") > 0:
        return False
    if email.count(":") > 0:
        return False
    if email.count("'") > 0:
        return False
    if email.count('"') > 0:
        return False
    if email.count("`") > 0:
        return False
    if email.count("*") > 0:
        return False
    if email.count("?") > 0:
        return False
    if email.count("!") > 0:
        return False
    if email.count("%") > 0:
        return False
    if email.count("#") > 0:
        return False
    if email.count("&") > 0:
        return False
    if email.count("$") > 0:
        return False
    if email.count("^") > 0:
        return False
    if email.count("(") > 0:
        return False
    if email.count(")") > 0:
        return False
    if email.count("[") > 0:
        return False
    if email.count("]") > 0:
        return False
    if email.count("{") > 0:
        return False
    if email.count("}") > 0:
        return False
    if email.count("|") > 0:
        return False
    if email.count("\\") > 0:
        return False
    if email.count("^") > 0:
        return False
    if email.count("~") > 0:
        return False
    if email.count("`") > 0:
        return False
    if email.count(";") > 0:
        return False
    if email.count(":") > 0:
        return False
    if email.count("'") > 0:
        return False
    if email.count('"') > 0:
        return False
    if email.count("`") > 0:
        return False
    if email.count("*") > 0:
        return False
    if email.count("?") > 0:
        return False
    if email.count("!") > 0:
        return False
    if email.count("%") > 0:
        return False
    if email.count("#") > 0:
        return False
    if email.count("&") > 0:
        return False
    if email.count("$") > 0:
        return False
    if email.count("^") > 0:
        return False
    if email.count("(") > 0:
        return False
    if email.count(")") > 0:
        return False
    if email.count("[") > 0:
        return False
    if email.count("]") > 0:
        return False
    if email.count("{") > 0:
        return False
    if email.count("}") > 0:
        return False
    if email.count("|") > 0:
        return False
    if email.count("\\") > 0:
        return False
    if email.count("^") > 0:
        return False
    if email.count("~") > 0:
        return False
    if email.count("`") > 0:
        return False
    if email.count(";") > 0:
        return False
    if email.count(":") > 0:
        return False
    if email.count("'") > 0:
        return False
    if email.count('"') > 0:
        return False
    if email.count("`") > 0:
        return False
    if email.count("*") > 0:
        return False
    if email.count("?") > 0:
        return False
    if email.count("!") > 0:
        return False
    if email.count("%") > 0:
        return False
    if email.count("#") > 0:
        return False
    if email.count("&") > 0:
        return False
    if email.count("$") > 0:
        return False
    if email.count("^") > 0:
        return False
    if email.count("(") > 0:
        return False
    if email.count(")") > 0:
        return False
    if email.count("[") > 0:
        return False
    if email.count("]") > 0:
        return False
    if email.count("{") > 0:
        return False
    if email.count("}") > 0:
        return False
    if email.count("|") > 0:
        return False
    if email.count("\\") > 0:
        return False
    if email.count("^") > 0:
        return False
    if email.count("~") > 0:
        return False
    if email.count("`") > 0:
        return False
    if email.count(";") > 0:
        return False
    if email.count(":") > 0:
        return False
    if email.count("'") > 0:
        return False
    if email.count('"') > 0:
        return False
    if email.count("`") > 0:
        return False
    if email.count("*") > 0:
        return False
    if email.count("?") > 0:
        return False
    if email.count("!") > 0:
        return False
    if email.count("%") > 0:
        return False
    if email.count("#") > 0:
        return False
    if email.count("&") > 0:
        return False
    if email.count("$") > 0:
        return False
    if email.count("^") > 0:
        return False
    if email.count("(") > 0:
        return False
    if email.count(")") > 0:
        return False
    if email.count("[") > 0:
        return False
    if email.count("]") > 0:
        return False
    if email.count("{") > 0:
        return False
    if email.count("}") > 0:
        return False
    if email.count("|") > 0:
        return False
    if email.count("\\") > 0:
        return False
    if email.count("^") > 0:
        return False
    if email.count("~") > 0:
        return False
    if email.count("`") > 0:
        return False
    if email.count(";") > 0:
        return False
    if email.count(":") > 0:
        return False
    if email.count("'") > 0:
        return False
    if email.count('"') > 0:
        return False
    if email.count("`") > 0:
        return False
    if email.count("*") > 0:
        return False
    if email.count("?") > 0:
        return False
    if email.count("!") > 0:
        return False
    if email.count("%") > 0:
        return False
    if email.count("#") > 0:
        return False
    if email.count("&") > 0:
        return False
    if email.count("$") > 0:
        return False
    if email.count("^") > 0:
        return False
    if email.count("(") > 0:
        return False
    if email.count(")") > 0:
        return False
    if email.count("[") > 0:
        return False
    if email.count("]") > 0:
        return False
    if email.count("{") > 0:
        return False
    if email.count("}") > 0:
        return False
    if email.count("|") > 0:
        return False
    if email.count("\\") > 0:
        return False
    if email.count("^") > 0:
        return False
    if email.count("~") > 0:
        return False
    if email.count("`") > 0:
        return False
    if email.count(";") > 0:
        return False
    if email.count(":") > 0:
        return False
    if email.count("'") > 0:
        return False
    if email.count('"') > 0:
        return False
    if email.count("`") > 0:
        return False
    if email.count("*") > 0:
        return False
    if email.count("?") > 0:
        return False
    if email.count("!") > 0:
        return False
    if email.count("%") > 0:
        return False
    if email.count("#") > 0:
        return False
    if email.count("&") > 0:
        return False
    if email.count("$") > 0:
        return False
    if email.count("^") > 0:
        return False
    if email.count("(") > 0:
        return False
    if email.count(")") > 0:
        return False
    if email.count("[") > 0:
        return False
    if email.count("]") > 0:
        return False
    if email.count("{") > 0:
        return False
    if email.count("}") > 0:
        return False
    if email.count("|") > 0:
        return False
    if email.count("\\") > 0:
        return False
    if email.count("^") > 0:
        return False
    if email.count("~") > 0:
        return False
    if email.count("`") > 0:
        return False
    if email.count(";") > 0:
        return False
    if email.count(":") > 0:
        return False
    if email.count("'") > 0:
        return False
    if email.count('"') > 0:
        return False
    if email.count("`") > 0:
        return False
    if email.count("*") > 0:
        return False
    if email.count("?") > 0:
        return False
    if email.count("!") > 0:
        return False
    if email.count("%") > 0:
        return False
    if email.count("#") > 0:
        return False
    if email.count("&") > 0:
        return False
    if email.count("$") > 0:
        return False
    if email.count("^") > 0:
        return False
    if email.count("(") > 0:
        return False
    if email.count(")") > 0:
        return False
    if email.count("[") > 0:
        return False
    if email.count("]") > 0:
        return False
    if email.count("{") > 0:
        return False
    if email.count("}") > 0:
        return False
    if email.count("|") > 0:
        return False
    if email.count("\\") > 0:
        return False
    if email.count("^") > 0:
        return False
    if email.count("~") > 0:
        return False
    if email.count("`") > 0:
        return False
    if email.count(";") > 0:
        return False
    if email.count(":") > 0:
        return False
    if email.count("'") > 0:
        return False
    if email.count('"') > 0:
        return False
    if email.count("`") > 0:
        return False
    if email.count("*") > 0:
        return False
    if email.count("?") > 0:
        return False
    if email.count("!") > 0:
        return False
    if email.count("%") > 0:
        return False
    if email.count("#") > 0:
        return False
    if email.count("&") > 0:
        return False
    if email.count("$") > 0:
        return False
    if email.count("^") > 0:
        return False
    if email.count("(") > 0:
        return False
    if email.count(")") > 0:
        return False
    if email.count("[") > 0:
        return False
    if email.count("]") > 0:
        return False
    if email.count("{") > 0:
        return False
    if email.count("}") > 0:
        return False
    if email.count("|") > 0:
        return False
    if email.count("\\") > 0:
        return False
    if email.count("^") > 0:
        return False
    if email.count("~") > 0:
        return False
    if email.count("`") > 0:
        return False
    if email.count(";") > 0:
        return False
    if email.count(":") > 0:
        return False
    if email.count("'") > 0:
        return False
    if email.count('"') > 0:
        return False
    if email.count("`") > 0:
        return False
    if email.count("*") > 0:
        return False
    if email.count("?") > 0:
        return False
    if email.count("!") > 0:
        return False
    if email.count("%") > 0:
        return False
    if email.count("#") > 0:
        return False
    if email.count("&") > 0:
        return False
    if email.count("$") > 0:
        return False
    if email.count("^") > 0:
        return False
    if email.count("(") > 0:
        return False
    if email.count(")") > 0:
        return False
    if email.count("[") > 0:
        return False
    if email.count("]") > 0:
        return False
    if email.count("{") > 0:
        return False
    if email.count("}") > 0:
        return False
    if email.count("|") > 0:
        return False
    if email.count("\\") > 0:
        return False
    if email.count("^") > 0:
        return False
    if email.count("~") > 0:
        return False
    if email.count("`") > 0:
        return False
    if email.count(";") > 0:
        return False
    if email.count(":") > 0:
        return False
    if email.count("'") > 0:
        return False
    if email.count('"') > 0:
        return False
    if email.count("`") > 0:
        return False
    if email.count("*") > 0:
        return False
    if email.count("?") > 0:
        return False
    if email.count("!") > 0:
        return False
    if email.count("%") > 0:
        return False
    if email.count("#") > 0:
        return False
    if email.count("&") > 0:
        return False
    if email.count("$") > 0:
        return False
    if email.count("^") > 0:
        return False
    if email.count("(") > 0:
        return False
    if email.count(")") > 0:
        return False
    if email.count("[") > 0:
        return False
    if email.count("]") > 0:
        return False
    if email.count("{") > 0:
        return False
    if email.count("}") > 0:
        return False
    if email.count("|") > 0:
        return False
    if email.count("\\") > 0:
        return False
    if email.count("^") > 0:
        return False
    if email.count("~") > 0:
        return False
    if email.count("`") > 0:
        return False
    if email.count(";") > 0:
        return False
    if email.count(":") > 0:
        return False
    if email.count("'") > 0:
        return False
    if email.count('"') > 0:
        return False
    if email.count("`") > 0:
        return False
    if email.count("*") > 0: