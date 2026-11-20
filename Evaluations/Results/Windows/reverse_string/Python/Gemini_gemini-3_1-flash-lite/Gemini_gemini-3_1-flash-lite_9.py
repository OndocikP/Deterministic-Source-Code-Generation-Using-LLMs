def reverse_string(value: object) -> str:
    """Return the input string in reverse order, or an empty string if input is not a string."""
    if not isinstance(value, str):
        return ""
    return value[::-1]