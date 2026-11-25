from collections import deque

def knight_min_moves(board_size: int, start: tuple[int, int], end: tuple[int, int]) -> int | None:
    if not (0 <= start[0] < board_size and 0 <= start[1] < board_size and
            0 <= end[0] < board_size and 0 <= end[1] < board_size):
        return None

    if start == end:
        return 0

    queue = deque([(start, 0)])
    visited = {start}

    knight_moves = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]

    while queue:
        (current_pos, moves) = queue.popleft()

        for dr, dc in knight_moves:
            next_r = current_pos[0] + dr
            next_c = current_pos[1] + dc
            next_pos = (next_r, next_c)

            if 0 <= next_r < board_size and 0 <= next_c < board_size and next_pos not in visited:
                if next_pos == end:
                    return moves + 1
                
                visited.add(next_pos)
                queue.append((next_pos, moves + 1))

    return None