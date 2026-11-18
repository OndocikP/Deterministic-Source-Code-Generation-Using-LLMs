def count_vowels(value: str) -> int:
    """
    Returns the count of vowels a, e, i, o, u in the input string, case-insensitive.
    """
    if not isinstance(value, str):
        return 0
    vowels = ["a", "e", "i", "o", "u"]
    count = 0
    for char in value.lower():
        if char in vowels:
            count += 1
    return count