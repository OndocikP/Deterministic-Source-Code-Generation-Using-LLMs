def reverse_string(value: str) -> str:
    """
    Returns the input string in reverse order.
    
    Args:
    value (str): The string to be reversed.
    
    Returns:
    str: The reversed string.
    """
    if not isinstance(value, str):
        return ""
    return value[::-1]