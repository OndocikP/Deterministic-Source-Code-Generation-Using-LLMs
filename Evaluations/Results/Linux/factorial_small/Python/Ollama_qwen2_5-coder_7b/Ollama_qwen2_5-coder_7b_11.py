from typing import Optional

def factorial_small(value: int) -> Optional[int]:
    if not isinstance(value, int) or value < 0 or value > 10:
        return None
    if value == 0:
        return 0
    result = 1
    for i in range(1, value + 1):
        result *= i
    return result