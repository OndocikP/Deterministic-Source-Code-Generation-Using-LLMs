def normalize_path(path: str) -> str:
    if path == "/":
        return "/"
    
    parts = path.split("/")
    stack = []
    
    for part in parts:
        if part == "" or part == ".":
            continue
        elif part == "..":
            if stack:
                stack.pop()
        else:
            stack.append(part)
    
    return "/" + "/".join(stack)