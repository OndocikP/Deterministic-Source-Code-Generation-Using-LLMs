def factorial_small(value: int) -> int | None:
    """Returns the factorial of an integer between 0 and 10 inclusive."""
    if not isinstance(value, int) or not (0 <= value <= 10):
        return None
    
    result = 1
    for i in range(2, value + 1):
        result *= i
    return result