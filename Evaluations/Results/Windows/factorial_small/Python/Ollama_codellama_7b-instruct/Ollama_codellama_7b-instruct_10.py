def factorial_small(value: int) -> int | None:
    """
    Returns the factorial of a non-negative integer input.
    """
    if not isinstance(value, int):
        return None
    if value < 0 or value > 10:
        return None
    result = 1
    for i in range(2, value + 1):
        result *= i
    return result