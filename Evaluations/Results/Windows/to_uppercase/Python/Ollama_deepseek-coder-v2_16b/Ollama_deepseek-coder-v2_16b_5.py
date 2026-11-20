def to_uppercase(value: str) -> str:
    """
    Returns the input string converted to uppercase.
    
    Args:
        value (str): The input string to be converted to uppercase.
    
    Returns:
        str: The uppercase version of the input string, or an empty string if the input is not a string.
    """
    if not isinstance(value, str):
        return ""
    return value.upper()