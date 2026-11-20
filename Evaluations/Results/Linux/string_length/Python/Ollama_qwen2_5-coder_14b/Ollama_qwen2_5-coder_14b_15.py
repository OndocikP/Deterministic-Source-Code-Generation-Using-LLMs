def string_length(value: str) -> int:
    """Return the number of characters in the input string."""
    if not isinstance(value, str):
        return 0
    return len(value)