def insert_and_merge(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
    result = []
    i = 0
    n = len(intervals)
    new_start, new_end = new_interval[0], new_interval[1]

    # 1. Add all intervals that come before the new interval (no overlap)
    while i < n and intervals[i][1] < new_start:
        result.append(intervals[i])
        i += 1

    # 2. Merge overlapping intervals
    while i < n and intervals[i][0] <= new_end:
        new_start = min(new_start, intervals[i][0])
        new_end = max(new_end, intervals[i][1])
        i += 1

    # 3. Add the merged interval
    result.append([new_start, new_end])

    # 4. Add all remaining intervals that come after the merged interval
    while i < n:
        result.append(intervals[i])
        i += 1

    return result