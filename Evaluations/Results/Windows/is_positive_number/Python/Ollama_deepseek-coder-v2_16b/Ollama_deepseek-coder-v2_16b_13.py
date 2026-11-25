def is_positive_number(value: float) -> bool:
    """
    Returns True if the input number is strictly greater than 0, otherwise False.
    """
    return isinstance(value, (int, float)) and value > 0