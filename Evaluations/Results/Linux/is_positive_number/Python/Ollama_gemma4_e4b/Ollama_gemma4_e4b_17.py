def is_positive_number(value: object) -> bool:
    """Checks if the input value is a number strictly greater than 0."""
    if isinstance(value, (int, float)):
        return value > 0
    return False