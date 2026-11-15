def insert_and_merge(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
    result = []
    i = 0
    n = len(intervals)
    
    # Add all intervals that end before the new interval starts
    while i < n and intervals[i][1] < new_interval[0]:
        result.append(intervals[i])
        i += 1
    
    # Merge all overlapping intervals
    while i < n and intervals[i][0] <= new_interval[1]:
        new_interval = [min(new_interval[0], intervals[i][0]), max(new_interval[1], intervals[i][1])]
        i += 1
    
    # Add the merged interval
    result.append(new_interval)
    
    # Add all remaining intervals
    while i < n:
        result.append(intervals[i])
        i += 1
    
    return result