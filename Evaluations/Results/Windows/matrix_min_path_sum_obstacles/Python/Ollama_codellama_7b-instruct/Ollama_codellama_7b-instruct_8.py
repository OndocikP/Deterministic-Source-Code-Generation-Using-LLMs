def min_path_sum(grid: list[list[int]]) -> int | None:
    """
    Returns the minimum path sum from top-left to bottom-right in a matrix.
    """
    # Initialize the dp table with the first row and column
    dp = [[0] * len(grid[0]) for _ in range(len(grid))]

    # Initialize the start and end positions
    start_row = 0
    start_col = 0
    end_row = len(grid) - 1
    end_col = len(grid[0]) - 1

    # Fill in the dp table
    for i in range(1, len(grid)):
        for j in range(1, len(grid[0])):
            # If the current cell is blocked, set the value to None
            if grid[i][j] == -1:
                dp[i][j] = None
            # If the current cell is not blocked, calculate the minimum path sum
            else:
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1]) + grid[i][j]

    # Return the minimum path sum from the start to the end position
    return dp[end_row][end_col]

# Test the function with a sample input
grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
print(min_path_sum(grid)) # Output: 12