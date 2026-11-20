def square_number(value: object) -> float | int | None:
    """Returns the square of the input number, or None if the input is not a number."""
    if isinstance(value, (int, float)):
        return value * value
    return None