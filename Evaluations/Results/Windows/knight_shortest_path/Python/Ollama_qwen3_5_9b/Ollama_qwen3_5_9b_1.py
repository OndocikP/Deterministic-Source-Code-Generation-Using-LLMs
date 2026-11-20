def knight_min_moves(board_size: int, start: tuple[int, int], end: tuple[int, int]) -> int | None:
    if not (0 <= start[0] < board_size and 0 <= start[1] < board_size):
        return None
    if not (0 <= end[0] < board_size and 0 <= end[1] < board_size):
        return None
    if start == end:
        return 0
    
    moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    queue = [(start[0], start[1], 0)]
    visited = set()
    visited.add(start)
    
    while queue:
        r, c, dist = queue.pop(0)
        
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < board_size and 0 <= nc < board_size and (nr, nc) not in visited:
                if (nr, nc) == end:
                    return dist + 1
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))
    
    return None