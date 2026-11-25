def normalize_path(path: str) -> str:
    parts = []
    current = '/'
    for part in path.split('/'):
        if part == '.' or part == '':
            continue
        if part == '..':
            if current != '/':
                current = current.rsplit('/', 1)[0] + '/'
        else:
            current += part + '/'
    return current if current.endswith('/') else current + '/'