from typing import Union, Optional

def absolute_value(value: Union[int, float]) -> Optional[float]:
    """
    Returns the absolute value of the input number.
    Returns None if the input is not a number.
    """
    if isinstance(value, (int, float)):
        return abs(value)
    return None