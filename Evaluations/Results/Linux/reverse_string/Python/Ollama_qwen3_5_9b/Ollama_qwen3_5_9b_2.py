def reverse_string(value: str) -> str:
    """Return the input string in reverse order.

    If the input is not a string, returns an empty string.
    """
    if not isinstance(value, str):
        return ""
    return value[::-1]