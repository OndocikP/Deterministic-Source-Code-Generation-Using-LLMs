def square_number(value: float | int | None = None) -> float | None:
    """
    Returns the square of the input number.
    If input is not a number, returns None.
    """
    if value is None or isinstance(value, (int, float)):
        return value ** 2
    return None