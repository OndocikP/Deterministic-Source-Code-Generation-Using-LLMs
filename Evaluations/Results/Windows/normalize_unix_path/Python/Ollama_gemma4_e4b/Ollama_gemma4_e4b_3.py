def normalize_path(path: str) -> str:
    if not path.startswith('/'):
        raise ValueError("Input path must be absolute.")

    components = []
    current_path = ""
    
    # Split by '/', filtering out empty strings resulting from multiple slashes
    parts = [part for part in path.split('/') if part]

    for part in parts:
        if part == '.':
            continue
        elif part == '..':
            if components:
                components.pop()
        else:
            components.append(part)

    return "/" + "/".join(components)