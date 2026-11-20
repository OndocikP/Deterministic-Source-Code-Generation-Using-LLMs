def factorial_small(value: int) -> int | None:
    """
    Returns the factorial of a non-negative integer input between 0 and 10 inclusive.
    Returns None if input is not an integer or outside the valid range.
    """
    if not isinstance(value, int) or value < 0 or value > 10:
        return None
    result = 1
    for i in range(1, value + 1):
        result *= i
    return result