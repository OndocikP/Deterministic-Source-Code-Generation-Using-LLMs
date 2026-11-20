def string_length(value: str) -> int:
    """
    Returns the number of characters in the input string.
    Returns 0 if the input is not a string.
    """
    if not isinstance(value, str):
        return 0
    return len(value)