from typing import Any

def count_vowels(value: Any) -> int:
    """Return the count of vowels a, e, i, o, u in the input string, case-insensitive."""
    if not isinstance(value, str):
        return 0
    vowels = 'aeiou'
    return sum(1 for char in value.lower() if char in vowels)