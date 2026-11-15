from typing import Union

def absolute_value(value: Union[int, float]) -> Union[int, float, None]:
    """Returns the absolute value of the input number."""
    if isinstance(value, (int, float)):
        return abs(value)
    return None