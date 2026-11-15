def square_number(value: int | float) -> int | float | None:
    """Returns the square of the input number, or None if input is not a number."""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return value ** 2
    return None