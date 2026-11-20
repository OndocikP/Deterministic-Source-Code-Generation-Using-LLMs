def knight_min_moves(board_size: int, start: tuple[int, int], end: tuple[int, int]) -> int | None:
    if start == end:
        return 0
    if not (0 <= start[0] < board_size and 0 <= start[1] < board_size and 0 <= end[0] < board_size and 0 <= end[1] < board_size):
        return None
    queue = [(start, 0)]
    visited = set()
    while queue:
        node, moves = queue.pop(0)
        if node == end:
            return moves
        for neighbor in get_neighbors(node, board_size):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, moves + 1))
    return None

def get_neighbors(node: tuple[int, int], board_size: int) -> list[tuple[int, int]]:
    row, col = node
    neighbors = []
    for r, c in [(row - 2, col - 1), (row - 2, col + 1), (row - 1, col - 2), (row - 1, col + 2), (row + 1, col - 2), (row + 1, col + 2), (row + 2, col - 1), (row + 2, col + 1)]:
        if 0 <= r < board_size and 0 <= c < board_size:
            neighbors.append((r, c))
    return neighbors