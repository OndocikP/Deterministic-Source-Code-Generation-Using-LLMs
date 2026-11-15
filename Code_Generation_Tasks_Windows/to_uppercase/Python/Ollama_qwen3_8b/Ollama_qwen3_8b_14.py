def to_uppercase(value: str | None) -> str:
    """Convert the input string to uppercase. Return empty string if input is not a string."""
    if not isinstance(value, str):
        return ""
    return value.upper()