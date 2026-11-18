def lcs_length(first: str, second: str) -> int:
    n = len(first)
    m = len(second)
    
    # Create a 2D DP table with dimensions (n+1) x (m+1)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    # Fill the DP table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if first[i - 1] == second[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # The bottom-right cell contains the length of LCS
    return dp[n][m]