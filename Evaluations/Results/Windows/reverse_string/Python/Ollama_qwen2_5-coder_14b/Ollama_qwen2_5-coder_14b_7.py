def reverse_string(value: str) -> str:
    """Return the input string in reverse order."""
    if not isinstance(value, str):
        return ""
    return value[::-1]