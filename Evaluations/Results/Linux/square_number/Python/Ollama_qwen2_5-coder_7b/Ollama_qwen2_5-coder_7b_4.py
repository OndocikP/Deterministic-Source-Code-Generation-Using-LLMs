from typing import Union, Optional

def square_number(value: Union[int, float]) -> Optional[float]:
    if isinstance(value, (int, float)):
        return value ** 2
    return None