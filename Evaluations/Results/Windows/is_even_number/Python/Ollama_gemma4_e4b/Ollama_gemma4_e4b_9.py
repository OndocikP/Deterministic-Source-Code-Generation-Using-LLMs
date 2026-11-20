def is_even_number(value: any) -> bool:
    """Checks if the input value is an even integer."""
    if not isinstance(value, int):
        return False
    return value % 2 == 0