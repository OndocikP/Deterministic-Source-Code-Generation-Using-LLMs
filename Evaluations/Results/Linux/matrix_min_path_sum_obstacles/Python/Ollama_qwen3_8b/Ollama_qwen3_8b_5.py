def min_path_sum(grid: list[list[int]]) -> int | None:
    if not grid or grid[0][0] == -1 or grid[-1][-1] == -1:
        return None

    rows, cols = len(grid), len(grid[0])
    dp = [[float('inf')] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == -1:
                continue
            if i > 0 and dp[i-1][j] != float('inf'):
                dp[i][j] = min(dp[i][j], dp[i-1][j] + grid[i][j])
            if j > 0 and dp[i][j-1] != float('inf'):
                dp[i][j] = min(dp[i][j], dp[i][j-1] + grid[i][j])

    return dp[-1][-1] if dp[-1][-1] != float('inf') else None