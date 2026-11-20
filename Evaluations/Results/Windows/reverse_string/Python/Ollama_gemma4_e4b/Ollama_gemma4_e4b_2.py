def reverse_string(value: str) -> str:
    """Reverses the input string, returning an empty string if the input is not a string."""
    if not isinstance(value, str):
        return ""
    return value[::-1]