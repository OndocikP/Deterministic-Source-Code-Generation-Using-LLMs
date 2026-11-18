def count_vowels(value: str) -> int:
    """
    Returns the count of vowels a, e, i, o, u in the input string, case-insensitive.
    """
    if not isinstance(value, str):
        return 0
    return sum(1 for char in value.lower() if char in {'a', 'e', 'i', 'o', 'u'})