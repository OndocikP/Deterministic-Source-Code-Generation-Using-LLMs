def normalize_path(path: str) -> str:
    """
    Normalize an absolute Unix-style file path.
    """
    # Collapse multiple slashes into one
    path = re.sub(r'//+', '/', path)
    # Handle . as current directory (ignore it)
    path = re.sub(r'\.+', '', path)
    # Handle .. as parent directory; do not go above root
    path = re.sub(r'\.\./+', '', path)
    # Return canonical absolute path
    return os.path.abspath(path)