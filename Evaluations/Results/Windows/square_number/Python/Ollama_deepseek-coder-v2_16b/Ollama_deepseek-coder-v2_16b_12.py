def square_number(value: (int, float)) -> (int, float, None):
    """
    Returns the square of the input number.
    
    Args:
        value (int, float): The number to be squared.
    
    Returns:
        int, float or None: The square of the input number, or None if the input is not a number.
    """
    if isinstance(value, (int, float)):
        return value ** 2
    else:
        return None