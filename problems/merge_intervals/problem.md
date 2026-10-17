# Merge overlapping intervals

Write `merge(intervals)` that takes a list of `[start, end]` pairs (with `start <= end`)
and returns a new list where every overlapping or touching pair has been merged.

Rules:

- The input is not sorted.
- Intervals that touch count as overlapping: `[1, 3]` and `[3, 5]` become `[1, 5]`.
- The output is sorted by start.
- Don't modify the input list or the pairs inside it. The caller may still be using them.
- An empty input returns an empty list.

Example:

```python
merge([[8, 10], [1, 3], [2, 6], [15, 18]])
# [[1, 6], [8, 10], [15, 18]]
```

Why this problem: it's short, but there are four separate ways to get it subtly wrong
(ordering, touching edges, contained intervals, mutation), and a couple of them pass
the obvious example.
