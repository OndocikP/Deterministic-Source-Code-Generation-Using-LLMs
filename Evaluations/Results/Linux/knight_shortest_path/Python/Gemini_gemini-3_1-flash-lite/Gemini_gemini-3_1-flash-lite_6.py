from collections import deque

def knight_min_moves(board_size: int, start: tuple[int, int], end: tuple[int, int]) -> int | None:
    if not (0 <= start[0] < board_size and 0 <= start[1] < board_size and
            0 <= end[0] < board_size and 0 <= end[1] < board_size):
        return None
    
    if start == end:
        return 0
    
    queue = deque([(start[0], start[1], 0)])
    visited = {start}
    
    moves = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    
    while queue:
        r, c, dist = queue.popleft()
        
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            
            if (nr, nc) == end:
                return dist + 1
            
            if 0 <= nr < board_size and 0 <= nc < board_size and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))
                
    return None