def is_leap_year(value: int) -> bool:
    """
    Determine if a given year is a leap year.

    A leap year is divisible by 4, but years divisible by 100 are not leap years
    unless they are also divisible by 400.

    Args:
        value (int): The year to check.

    Returns:
        bool: True if the year is a leap year, False otherwise.
    """
    if not isinstance(value, int):
        return False
    if value % 4 == 0:
        if value % 100 == 0:
            if value % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False