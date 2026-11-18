def normalize_path(path: str) -> str:
    if not path.startswith('/'):
        return path
    
    parts = []
    for part in path.split('/'):
        if part == '..':
            if parts:
                parts.pop()
        elif part and part != '.':
            parts.append(part)
    
    normalized_path = '/' + '/'.join(parts)
    return normalized_path