def absolute_value(value: float | int | None) -> float | None:
    """
    Returns the absolute value of the input number.
    If input is not a number, returns None.
    """
    if value is None:
        return None
    if not isinstance(value, (int, float)):
        return None
    return abs(value) if value >= 0 else -value