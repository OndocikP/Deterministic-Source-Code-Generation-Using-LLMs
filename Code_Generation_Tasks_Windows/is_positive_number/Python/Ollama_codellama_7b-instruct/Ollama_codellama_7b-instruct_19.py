def is_positive_number(value: Union[int, float]) -> bool:
    """
    Returns True if the input number is strictly greater than 0, otherwise False.
    """
    if not isinstance(value, (int, float)):
        return False
    return value > 0