def is_positive_number(value: float) -> bool:
    """Return True if the input number is strictly greater than 0, otherwise False."""
    if isinstance(value, (int, float)):
        return value > 0
    return False