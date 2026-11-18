def absolute_value(value: Union[int, float]) -> Union[int, float]:
    """
    Returns the absolute value of the input number.
    """
    if not isinstance(value, (int, float)):
        return None
    return abs(value)