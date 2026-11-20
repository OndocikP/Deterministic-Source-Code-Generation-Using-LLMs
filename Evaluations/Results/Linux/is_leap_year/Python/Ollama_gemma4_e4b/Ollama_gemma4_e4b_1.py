def is_leap_year(value: int) -> bool:
    """Checks if the given year is a leap year."""
    if not isinstance(value, int):
        return False
    return (value % 4 == 0 and value % 100 != 0) or (value % 400 == 0)