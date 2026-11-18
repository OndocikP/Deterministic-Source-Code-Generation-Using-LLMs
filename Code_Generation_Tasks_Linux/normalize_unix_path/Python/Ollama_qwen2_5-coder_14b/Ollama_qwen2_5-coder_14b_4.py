def normalize_path(path: str) -> str:
    components = path.split('/')
    stack = []
    
    for component in components:
        if component == '' or component == '.':
            continue
        if component == '..':
            if stack:
                stack.pop()
        else:
            stack.append(component)
    
    return '/' + '/'.join(stack) if stack else '/'