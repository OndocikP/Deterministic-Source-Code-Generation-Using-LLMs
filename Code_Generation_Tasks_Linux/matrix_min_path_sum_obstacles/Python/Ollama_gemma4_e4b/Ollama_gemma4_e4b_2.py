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
                continue

            if r == 0 and c == 0:
                continue

            from_top = float('inf')
            if r > 0 and grid[r - 1][c] != -1:
                from_top = dp[r - 1][c]

            from_left = float('inf')
            if c > 0 and grid[r][c - 1] != -1:
                from_left = dp[r][c - 1]

            min_prev = min(from_top, from_left)

            if min_prev != float('inf'):
                dp[r][c] = min_prev + grid[r][c]

    result = dp[rows - 1][cols - 1]

    return result if result != float('inf') else None