from collections import deque

def knight_min_moves(board_size: int, start: tuple[int, int], end: tuple[int, int]) -> int | None:
    if not (0 <= start[0] < board_size and 0 <= start[1] < board_size) or not (0 <= end[0] < board_size and 0 <= end[1] < board_size):
        return None
    
    if start == end:
        return 0
    
    directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    queue = deque([(start, 0)])
    visited = set([start])
    
    while queue:
        (current, moves) = queue.popleft()
        for dr, dc in directions:
            new_r, new_c = current[0] + dr, current[1] + dc
            if (new_r, new_c) == end:
                return moves + 1
            if 0 <= new_r < board_size and 0 <= new_c < board_size and (new_r, new_c) not in visited:
                visited.add((new_r, new_c))
                queue.append(((new_r, new_c), moves + 1))
    
    return None