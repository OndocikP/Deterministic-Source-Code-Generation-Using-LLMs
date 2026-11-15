def knight_min_moves(board_size: int, start: tuple[int, int], end: tuple[int, int]) -> int | None:
    if start == end:
        return 0
    if (start[0] < 0 or start[0] >= board_size or start[1] < 0 or start[1] >= board_size or
        end[0] < 0 or end[0] >= board_size or end[1] < 0 or end[1] >= board_size):
        return None
    from collections import deque
    directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    visited = set()
    queue = deque([(start[0], start[1], 0)])
    visited.add((start[0], start[1]))
    while queue:
        row, col, moves = queue.popleft()
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (new_row, new_col) == end:
                return moves + 1
            if 0 <= new_row < board_size and 0 <= new_col < board_size and (new_row, new_col) not in visited:
                visited.add((new_row, new_col))
                queue.append((new_row, new_col, moves + 1))
    return None