def min_word_break(text: str, dictionary: list[str]) -> int:
    n = len(text)
    dp = [float('inf')] * (n + 1)
    dp[0] = 0

    dict_set = set(dictionary)

    for i in range(1, n + 1):
        for j in range(i):
            substring = text[j:i]
            if substring in dict_set and dp[j] != float('inf'):
                dp[i] = min(dp[i], dp[j] + 1)

    return dp[n] if dp[n] != float('inf') else -1