def is_even_number(value: int) -> bool:
    if not isinstance(value, int):
        return False
    return value % 2 == 0