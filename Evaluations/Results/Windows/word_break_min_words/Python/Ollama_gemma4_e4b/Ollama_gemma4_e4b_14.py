def min_word_break(text: str, dictionary: list[str]) -> int:
    n = len(text)
    word_set = set(dictionary)
    # dp[i] stores the minimum number of words to segment text[:i]
    # Initialize with infinity, dp[0] = 0
    infinity = float('inf')
    dp = [infinity] * (n + 1)
    dp[0] = 0

    for i in range(1, n + 1):
        for j in range(i):
            substring = text[j:i]
            if substring in word_set and dp[j] != infinity:
                dp[i] = min(dp[i], dp[j] + 1)

    return dp[n] if dp[n] != infinity else -1