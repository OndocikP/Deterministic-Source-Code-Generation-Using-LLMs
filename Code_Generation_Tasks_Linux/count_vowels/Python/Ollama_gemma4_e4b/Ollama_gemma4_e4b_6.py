def count_vowels(value: str) -> int:
    """Counts the number of vowels (a, e, i, o, u) in a string, case-insensitive."""
    if not isinstance(value, str):
        return 0
    vowels = "aeiouAEIOU"
    count = 0
    for char in value:
        if char in vowels:
            count += 1
    return count