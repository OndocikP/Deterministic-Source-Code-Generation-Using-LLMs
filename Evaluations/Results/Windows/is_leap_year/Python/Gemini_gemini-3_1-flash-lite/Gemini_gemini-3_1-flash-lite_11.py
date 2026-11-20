def is_leap_year(value: int) -> bool:
    """Returns True if the input year is a leap year, otherwise False."""
    if not isinstance(value, int):
        return False
    return (value % 4 == 0 and value % 100 != 0) or (value % 400 == 0)