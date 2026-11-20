def factorial_small(value: int) -> int | None:
    """
    Calculate the factorial of a non-negative integer.

    Args:
        value: A non-negative integer between 0 and 10 inclusive.

    Returns:
        The factorial of the input value, or None if the input is invalid.
    """
    if not isinstance(value, int):
        return None
    if value < 0 or value > 10:
        return None
    result = 1
    for i in range(2, value + 1):
        result *= i
    return result