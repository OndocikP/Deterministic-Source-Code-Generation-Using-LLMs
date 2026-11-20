def min_word_break(text: str, dictionary: list[str]) -> int:
    n = len(text)
    dp = [-1] * (n + 1)
    dp[0] = 0

    for i in range(1, n + 1):
        for word in dictionary:
            if i >= len(word) and text[i - len(word):i] == word:
                if dp[i - len(word)] != -1:
                    if dp[i] == -1 or dp[i] > dp[i - len(word)] + 1:
                        dp[i] = dp[i - len(word)] + 1

    return dp[n]