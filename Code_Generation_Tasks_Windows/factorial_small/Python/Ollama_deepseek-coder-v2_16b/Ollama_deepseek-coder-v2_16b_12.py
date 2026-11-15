def factorial_small(value: int) -> int | None:
    """
    Returns the factorial of a non-negative integer input.
    
    Args:
    value (int): A non-negative integer.
    
    Returns:
    int | None: The factorial of the input if it is within the range 0 to 10, inclusive.
                Returns None if the input is outside this range or not an integer.
    """
    if not isinstance(value, int) or value < 0 or value > 10:
        return None
    
    def factorial(n: int) -> int:
        if n == 0:
            return 1
        else:
            return n * factorial(n - 1)
    
    return factorial(value)