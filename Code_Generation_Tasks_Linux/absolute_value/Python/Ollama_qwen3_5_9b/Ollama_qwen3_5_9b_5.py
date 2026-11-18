def absolute_value(value: int | float) -> int | float | None:
    """
    Returns the absolute value of the input number.

    Args:
        value: The number to compute the absolute value for.

    Returns:
        The absolute value if input is a number, otherwise None.
    """
    try:
        return abs(value)
    except TypeError:
        return None