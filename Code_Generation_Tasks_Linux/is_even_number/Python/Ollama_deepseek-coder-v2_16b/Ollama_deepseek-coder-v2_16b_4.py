def is_even_number(value: int) -> bool:
    """
    Returns True if the input integer is even, otherwise False.
    Returns False if the input is not an integer.
    """
    if isinstance(value, int):
        return value % 2 == 0
    return False