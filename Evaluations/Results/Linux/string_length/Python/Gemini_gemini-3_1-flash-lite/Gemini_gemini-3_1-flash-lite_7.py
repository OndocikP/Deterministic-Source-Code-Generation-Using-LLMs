def string_length(value: object) -> int:
    """Returns the number of characters in the input string, or 0 if not a string."""
    if isinstance(value, str):
        return len(value)
    return 0