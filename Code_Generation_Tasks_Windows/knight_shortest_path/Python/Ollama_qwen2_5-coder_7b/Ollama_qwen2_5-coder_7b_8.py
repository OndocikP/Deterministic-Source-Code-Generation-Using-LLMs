from collections import deque

def knight_min_moves(board_size: int, start: tuple[int, int], end: tuple[int, int]) -> int | None:
    if start == end:
        return 0
    if not (0 <= start[0] < board_size and 0 <= start[1] < board_size and 0 <= end[0] < board_size and 0 <= end[1] < board_size):
        return None
    directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    queue = deque([(start, 0)])
    visited = set([start])
    while queue:
        (current, moves) = queue.popleft()
        for (dr, dc) in directions:
            (nr, nc) = (current[0] + dr, current[1] + dc)
            if 0 <= nr < board_size and 0 <= nc < board_size and (nr, nc) not in visited:
                if (nr, nc) == end:
                    return moves + 1
                visited.add((nr, nc))
                queue.append(((nr, nc), moves + 1))
    return None