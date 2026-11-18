def is_even_number(value: int) -> bool:
    """Return True if the input integer is even, otherwise False."""
    if not isinstance(value, int):
        return False
    return value % 2 == 0