def is_even_number(value: int) -> bool:
    """
    Returns True if the input integer is even, otherwise False.
    If input is not an integer, returns False.
    """
    if not isinstance(value, int):
        return False
    return value % 2 == 0