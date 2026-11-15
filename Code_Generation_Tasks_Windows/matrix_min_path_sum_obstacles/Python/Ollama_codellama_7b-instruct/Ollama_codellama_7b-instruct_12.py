def min_path_sum(grid: list[list[int]]) -> int | None:
    """
    Returns the minimum path sum from top-left to bottom-right in a matrix.
    """
    # Initialize the dp table with the first row and column
    dp = [[0] * len(grid[0]) for _ in range(len(grid))]

    # Initialize the start and end points
    start_row = 0
    start_col = 0
    end_row = len(grid) - 1
    end_col = len(grid[0]) - 1

    # Check if the start and end points are blocked
    if grid[start_row][start_col] == -1 or grid[end_row][end_col] == -1:
        return None

    # Initialize the minimum path sum
    min_sum = float("inf")

    # Loop through each row and column
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            # If the current cell is blocked, set the minimum path sum to None
            if grid[i][j] == -1:
                min_sum = None
                break
            # If the current cell is the start or end point, set the minimum path sum to the current cell value
            elif i == start_row and j == start_col:
                min_sum = grid[i][j]
            elif i == end_row and j == end_col:
                min_sum = grid[i][j]
            # If the current cell is not the start or end point, set the minimum path sum to the minimum of the current cell value and the minimum path sum of the previous row and column
            else:
                min_sum = min(min_sum, grid[i][j] + min(dp[i - 1][j], dp[i][j - 1]))

            # Update the dp table
            dp[i][j] = min_sum

    # Return the minimum path sum
    return min_sum