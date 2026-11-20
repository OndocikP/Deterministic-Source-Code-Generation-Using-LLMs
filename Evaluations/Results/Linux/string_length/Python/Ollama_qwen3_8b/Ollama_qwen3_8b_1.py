def string_length(value: any) -> int:
    """Return the number of characters in the input string, or 0 if input is not a string."""
    if isinstance(value, str):
        return len(value)
    return 0