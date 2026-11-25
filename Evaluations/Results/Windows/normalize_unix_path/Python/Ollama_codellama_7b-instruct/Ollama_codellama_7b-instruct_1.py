def normalize_path(path: str) -> str:
    # Replace multiple slashes with one
    path = path.replace("//", "/")
    # Remove leading slash
    path = path[1:]
    # Replace . with empty string
    path = path.replace(".", "")
    # Replace .. with empty string
    path = path.replace("..", "")
    # If path is empty, return root
    if path == "":
        return "/"
    # If path is not empty, return canonical absolute path
    return "/" + path