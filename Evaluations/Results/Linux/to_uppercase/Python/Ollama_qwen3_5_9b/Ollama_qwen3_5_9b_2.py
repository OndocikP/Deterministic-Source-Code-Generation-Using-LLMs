def to_uppercase(value: str) -> str:
    """Convert the input string to uppercase.

    Args:
        value: The string to convert.

    Returns:
        The uppercase version of the input string, or an empty string if the input is not a string.
    """
    return value.upper() if isinstance(value, str) else ""