def factorial_small(value: int) -> int | None:
    """Returns the factorial of a non-negative integer input (0-10)."""
    if not isinstance(value, int) or not (0 <= value <= 10):
        return None
    if value == 0:
        return 1
    result = 1
    for i in range(1, value + 1):
        result *= i
    return result