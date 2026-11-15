def min_path_sum(grid: list[list[int]]) -> int | None:
    if not grid or not grid[0]:
        return None
    
    rows = len(grid)
    cols = len(grid[0])
    
    if grid[0][0] == -1 or grid[rows - 1][cols - 1] == -1:
        return None
    
    dp = [[float('inf')] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == -1:
                dp[r][c] = float('inf')
                continue
            
            if r > 0:
                dp[r][c] = min(dp[r][c], dp[r - 1][c] + grid[r][c])
            if c > 0:
                dp[r][c] = min(dp[r][c], dp[r][c - 1] + grid[r][c])
                
    result = dp[rows - 1][cols - 1]
    return int(result) if result != float('inf') else None