def merge(intervals):
    intervals.sort(key=lambda pair: pair[0])
    merged = []
    for pair in intervals:
        if merged and pair[0] <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], pair[1])
        else:
            merged.append(pair)
    return merged
