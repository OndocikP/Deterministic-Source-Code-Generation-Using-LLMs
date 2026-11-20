def absolute_value(value: int | float) -> int | float | None:
    """Returns the absolute value of the input number, or None if not a number."""
    if isinstance(value, (int, float)):
        return abs(value)
    return None