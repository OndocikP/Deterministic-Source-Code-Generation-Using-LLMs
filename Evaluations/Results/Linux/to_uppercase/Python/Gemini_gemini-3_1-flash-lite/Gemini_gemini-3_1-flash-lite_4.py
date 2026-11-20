def to_uppercase(value: object) -> str:
    """Returns the input string converted to uppercase, or an empty string if input is not a string."""
    if isinstance(value, str):
        return value.upper()
    return ""