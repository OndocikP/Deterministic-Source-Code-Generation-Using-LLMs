def min_word_break(text: str, dictionary: list[str]) -> int:
    n = len(text)
    word_set = set(dictionary)
    
    # dp[i] will store the minimum number of words to break text[0:i]
    # Initialize with infinity, except for dp[0] which is 0 (empty string needs 0 words)
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    
    for i in range(1, n + 1):
        for j in range(i):
            if text[j:i] in word_set:
                dp[i] = min(dp[i], dp[j] + 1)
    
    return -1 if dp[n] == float('inf') else dp[n]