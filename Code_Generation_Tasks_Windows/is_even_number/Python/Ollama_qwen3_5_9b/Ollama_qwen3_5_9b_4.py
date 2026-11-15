def is_even_number(value: int) -> bool:
    """
    Check if the given integer value is even.

    Args:
        value (int): The integer to check.

    Returns:
        bool: True if the value is even, False otherwise.
              Returns False if the input is not an integer.
    """
    return isinstance(value, int) and not isinstance(value, bool) and (value % 2 == 0)