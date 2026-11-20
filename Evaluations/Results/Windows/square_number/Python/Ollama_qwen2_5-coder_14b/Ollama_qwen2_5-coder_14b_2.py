def square_number(value: float) -> float | None:
    """Return the square of the input number if it's a number, otherwise return None."""
    if isinstance(value, (int, float)):
        return value ** 2
    return None