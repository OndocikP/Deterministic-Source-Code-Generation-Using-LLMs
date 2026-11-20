def min_word_break(text: str, dictionary: list[str]) -> int:
    dp = [0] * (len(text) + 1)
    for i in range(1, len(text) + 1):
        for j in range(i, len(text) + 1):
            if text[i - 1] in dictionary:
                dp[j] = min(dp[j], dp[i - 1] + 1)
    return dp[len(text)]