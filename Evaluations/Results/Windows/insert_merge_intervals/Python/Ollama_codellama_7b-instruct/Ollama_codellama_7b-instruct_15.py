def insert_and_merge(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
    # Sort the intervals by start time
    intervals.sort(key=lambda x: x[0])

    # Merge overlapping or touching intervals
    for i in range(len(intervals) - 1):
        if intervals[i][1] >= intervals[i + 1][0]:
            intervals[i][1] = max(intervals[i][1], intervals[i + 1][1])
            intervals.pop(i + 1)

    # Insert the new interval
    intervals.append(new_interval)

    # Sort the intervals by start time again
    intervals.sort(key=lambda x: x[0])

    return intervals