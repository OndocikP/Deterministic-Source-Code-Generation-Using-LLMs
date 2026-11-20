def to_uppercase(value: str) -> str:
    """Converts the input string to uppercase, or returns an empty string if the input is not a string."""
    if not isinstance(value, str):
        return ""
    return value.upper()