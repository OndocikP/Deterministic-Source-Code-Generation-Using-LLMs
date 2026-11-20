def is_even_number(value: object) -> bool:
    """Returns True if the input is an even integer, otherwise False."""
    if not isinstance(value, int) or isinstance(value, bool):
        return False
    return value % 2 == 0