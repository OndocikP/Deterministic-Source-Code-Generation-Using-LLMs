def min_path_sum(grid: list[list[int]]) -> int | None:
    if grid[0][0] == -1 or grid[-1][-1] == -1:
        return None
    
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]
    
    for i in range(1, rows):
        if grid[i][0] != -1:
            dp[i][0] = dp[i-1][0] + grid[i][0]
        else:
            dp[i][0] = float('inf')
    
    for j in range(1, cols):
        if grid[0][j] != -1:
            dp[0][j] = dp[0][j-1] + grid[0][j]
        else:
            dp[0][j] = float('inf')
    
    for i in range(1, rows):
        for j in range(1, cols):
            if grid[i][j] != -1:
                dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]
            else:
                dp[i][j] = float('inf')
    
    if dp[-1][-1] == float('inf'):
        return None
    return dp[-1][-1]