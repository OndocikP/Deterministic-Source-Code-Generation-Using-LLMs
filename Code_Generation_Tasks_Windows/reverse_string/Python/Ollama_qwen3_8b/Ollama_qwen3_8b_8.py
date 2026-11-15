def reverse_string(value: str) -> str:
    """
    Returns the input string in reverse order. If input is not a string, returns an empty string.
    """
    if not isinstance(value, str):
        return ""
    return value[::-1]