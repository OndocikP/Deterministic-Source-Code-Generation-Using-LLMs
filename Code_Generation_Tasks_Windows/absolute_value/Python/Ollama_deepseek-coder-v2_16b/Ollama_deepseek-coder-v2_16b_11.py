def absolute_value(value: float) -> float | None:
    """
    Returns the absolute value of the input number.
    
    Args:
        value (float): The number to get the absolute value of.
    
    Returns:
        float | None: The absolute value of the input number, or None if the input is not a number.
    """
    if isinstance(value, (int, float)):
        return abs(value)
    else:
        return None