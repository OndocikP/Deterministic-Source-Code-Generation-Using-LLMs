def factorial_small(value: int) -> int | None:
    """
    Returns the factorial of a non-negative integer input.
    Input range is 0 to 10 inclusive. If input is outside range or not an integer, return None.
    The implementation must be deterministic.
    """
    if not isinstance(value, int) or value < 0 or value > 10:
        return None
    result = 1
    for i in range(1, value + 1):
        result *= i
    return result