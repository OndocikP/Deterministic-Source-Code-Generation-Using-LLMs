def count_vowels(value: str) -> int:
    """
    Count the number of vowels (a, e, i, o, u) in a string, case-insensitive.
    
    Args:
        value: The input string to analyze.
        
    Returns:
        The count of vowels found in the string. Returns 0 if input is not a string.
    """
    if not isinstance(value, str):
        return 0
    
    vowel_set = set("aeiou")
    return sum(1 for char in value.lower() if char in vowel_set)