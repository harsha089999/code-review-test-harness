def merge(intervals):
    """Merge overlapping or touching intervals. Returns a new sorted list."""
    merged = []
    for start, end in sorted(intervals, key=lambda pair: pair[0]):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
