def to_uppercase(value: str) -> str:
    """
    Convert the input string to uppercase.
    If input is not a string, return an empty string.
    """
    if not isinstance(value, str):
        return ""
    return value.upper()