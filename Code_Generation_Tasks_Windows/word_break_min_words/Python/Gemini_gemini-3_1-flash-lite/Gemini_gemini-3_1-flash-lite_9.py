def min_word_break(text: str, dictionary: list[str]) -> int:
    n = len(text)
    word_set = set(dictionary)
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] != float('inf') and text[j:i] in word_set:
                dp[i] = min(dp[i], dp[j] + 1)
                
    return int(dp[n]) if dp[n] != float('inf') else -1