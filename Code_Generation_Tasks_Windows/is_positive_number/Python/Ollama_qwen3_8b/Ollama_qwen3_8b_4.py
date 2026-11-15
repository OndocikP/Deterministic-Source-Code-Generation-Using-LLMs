def is_positive_number(value: float | int) -> bool:
    """
    Check if the input value is a strictly positive number.
    """
    return isinstance(value, (int, float)) and value > 0