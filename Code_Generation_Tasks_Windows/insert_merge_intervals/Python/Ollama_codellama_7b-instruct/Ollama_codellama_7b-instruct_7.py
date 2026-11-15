def insert_and_merge(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
    # Sort the intervals by start time
    intervals.sort(key=lambda x: x[0])

    # Merge overlapping or touching intervals
    for i in range(len(intervals) - 1):
        if intervals[i][1] >= intervals[i + 1][0]:
            intervals[i][1] = max(intervals[i][1], intervals[i + 1][1])
            intervals.pop(i + 1)

    # Insert the new interval
    for i in range(len(intervals)):
        if intervals[i][1] < new_interval[0]:
            intervals.insert(i, new_interval)
            break
    else:
        intervals.append(new_interval)

    return intervals