def normalize_path(path: str) -> str:
    parts = []
    current = ''
    i = 0
    while i < len(path):
        if path[i] == '/':
            if current:
                parts.append(current)
                current = ''
            i += 1
        else:
            current += path[i]
            i += 1
    if current:
        parts.append(current)
    result = '/'
    for part in parts:
        if part == '.' or part == '':
            continue
        if part == '..':
            if result != '/':
                result = result[:-len(parts[-1]) - 1]
        else:
            result += '/' + part
    return result if result != '/' else '/'