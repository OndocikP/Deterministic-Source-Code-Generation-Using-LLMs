def is_leap_year(value: int) -> bool:
    """
    Determine if a given year is a leap year.
    """
    if not isinstance(value, int):
        return False
    if value < 1:
        return False
    return value % 4 == 0 and (value % 100 != 0 or value % 400 == 0)