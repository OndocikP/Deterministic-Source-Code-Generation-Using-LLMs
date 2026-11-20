def count_vowels(value: str) -> int:
    if not isinstance(value, str):
        return 0
    return sum(1 for char in value.lower() if char in 'aeiou')