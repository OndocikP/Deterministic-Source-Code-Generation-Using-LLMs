def count_vowels(value: object) -> int:
    """Returns the count of vowels (a, e, i, o, u) in the input string, case-insensitive."""
    if not isinstance(value, str):
        return 0
    vowels = "aeiouAEIOU"
    return sum(1 for char in value if char in vowels)