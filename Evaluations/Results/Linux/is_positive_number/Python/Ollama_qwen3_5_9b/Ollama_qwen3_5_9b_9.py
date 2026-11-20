def is_positive_number(value: int | float) -> bool:
    """
    Check if the given value is strictly greater than zero.

    Args:
        value: The number to check. Can be an integer or a float.

    Returns:
        True if value is strictly greater than 0, False otherwise.
        Returns False for non-numeric types (though type hints restrict input).
    """
    return value > 0