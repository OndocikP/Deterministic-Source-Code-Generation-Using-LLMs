def knight_min_moves(board_size: int, start: tuple[int, int], end: tuple[int, int]) -> int | None:
    if not (0 <= start[0] < board_size and 0 <= start[1] < board_size and
            0 <= end[0] < board_size and 0 <= end[1] < board_size):
        return None

    if start == end:
        return 0

    directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    queue = [start]
    visited = set([start])
    moves = 0

    while queue:
        for _ in range(len(queue)):
            x, y = queue.pop(0)
            if (x, y) == end:
                return moves
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < board_size and 0 <= ny < board_size and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        moves += 1

    return None