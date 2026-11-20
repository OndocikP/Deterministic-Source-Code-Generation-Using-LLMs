def square_number(value):
    """
    Returns the square of the input number.

    Args:
        value (int | float): The number to be squared.

    Returns:
        int | float | None: The square of the input if it is a number, otherwise None.
    """
    try:
        return value ** 2
    except TypeError:
        return None