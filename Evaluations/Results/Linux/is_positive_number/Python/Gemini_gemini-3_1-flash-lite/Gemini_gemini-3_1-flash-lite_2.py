def is_positive_number(value: object) -> bool:
    """Returns True if value is a number strictly greater than 0, else False."""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return value > 0
    return False