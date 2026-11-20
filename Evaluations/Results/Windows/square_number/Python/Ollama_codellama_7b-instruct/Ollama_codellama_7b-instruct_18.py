def square_number(value: Union[int, float]) -> Optional[float]:
    """
    Returns the square of the input number.
    """
    if not isinstance(value, (int, float)):
        return None
    return value ** 2