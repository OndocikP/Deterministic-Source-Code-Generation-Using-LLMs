def is_leap_year(value: int) -> bool:
    """
    Determine if a given year is a leap year.

    A year is a leap year if it is divisible by 4, except for end-of-century years,
    which must be divisible by 400. This means that the year 2000 was a leap year,
    although 1900, 1800, and 1700 were not.

    Args:
        value (int): The year to check.

    Returns:
        bool: True if the year is a leap year, False otherwise.
    """
    try:
        year = int(value)
    except (TypeError, ValueError):
        return False

    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)