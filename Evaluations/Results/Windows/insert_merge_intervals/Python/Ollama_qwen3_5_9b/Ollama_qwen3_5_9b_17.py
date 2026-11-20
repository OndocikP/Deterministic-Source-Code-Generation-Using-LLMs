def insert_and_merge(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
    result = []
    i = 0
    n = len(intervals)
    
    # Add all intervals that come before the new interval
    while i < n and intervals[i][1] < new_interval[0]:
        result.append(intervals[i])
        i += 1
    
    # Merge overlapping intervals with the new interval
    merged_start = min(new_interval[0], intervals[i][0] if i < n else float('inf'))
    merged_end = max(new_interval[1], intervals[i][1] if i < n else float('inf'))
    
    while i < n and intervals[i][0] <= merged_end:
        merged_start = min(merged_start, intervals[i][0])
        merged_end = max(merged_end, intervals[i][1])
        i += 1
    
    result.append([merged_start, merged_end])
    
    # Add remaining intervals
    while i < n:
        result.append(intervals[i])
        i += 1
    
    return result