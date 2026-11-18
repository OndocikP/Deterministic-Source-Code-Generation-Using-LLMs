def reverse_string(value: str) -> str:
    if not isinstance(value, str):
        return ""
    return value[::-1]