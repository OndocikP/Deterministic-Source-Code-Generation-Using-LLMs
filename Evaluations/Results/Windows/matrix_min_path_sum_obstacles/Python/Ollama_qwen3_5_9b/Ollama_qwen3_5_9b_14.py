def min_path_sum(grid: list[list[int]]) -> int | None:
    if not grid or not grid[0]:
        return None
    
    rows = len(grid)
    cols = len(grid[0])
    
    if grid[0][0] == -1 or grid[rows-1][cols-1] == -1:
        return None
    
    dp = [[float('inf')] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]
    
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == -1:
                continue
            
            if i > 0:
                dp[i][j] = min(dp[i][j], dp[i-1][j] + grid[i][j])
            if j > 0:
                dp[i][j] = min(dp[i][j], dp[i][j-1] + grid[i][j])
    
    return dp[rows-1][cols-1]