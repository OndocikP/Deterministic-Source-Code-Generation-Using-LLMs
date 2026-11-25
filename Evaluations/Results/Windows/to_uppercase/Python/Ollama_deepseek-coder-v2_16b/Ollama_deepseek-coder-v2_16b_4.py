def to_uppercase(value: str) -> str:
    """
    Returns the input string converted to uppercase.
    
    Args:
        value (str): The input string to be converted to uppercase.
    
    Returns:
        str: The input string converted to uppercase if it is a string, otherwise an empty string.
    """
    if not isinstance(value, str):
        return ""
    return value.upper()