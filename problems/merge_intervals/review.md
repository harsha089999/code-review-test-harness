# Reviews: merge_intervals

## no_sort.py: reject

The merge loop itself is right, but it assumes the input is already sorted, and the spec
says it isn't. With `[[8, 10], [1, 3]]` the second interval starts before the first one
ends, so it gets folded into `[8, 10]` and `[1, 3]` disappears completely. That's data
loss, not just bad ordering.

Fix: iterate over `sorted(intervals, key=lambda p: p[0])`. Sorting by start is what makes
"only compare with the last merged interval" valid in the first place.

## touching_gap.py: reject

Uses `start < merged[-1][1]` where the spec needs `<=`. So `[1, 3]` and `[3, 5]` stay
separate, and duplicate single-point intervals like `[4, 4], [4, 4]` aren't merged either.
Easy to miss because the standard example has no touching edges.

Fix: change `<` to `<=`. Worth adding a test for touching edges explicitly, since it's the
kind of boundary condition that drifts during refactors.

## contained_shrink.py: reject

On overlap it sets the end to the new interval's end instead of the max of the two. That's
fine when intervals are staggered, but when one interval sits inside another it shrinks the
merged range: `[[1, 10], [2, 3]]` becomes `[[1, 3]]`, and anything that should have merged
into `[4, 10]` later now looks like a separate interval.

Fix: `merged[-1][1] = max(merged[-1][1], end)`.

## mutates_input.py: request changes

The output is correct, which is why the random differential tests don't catch it (the
harness hands each solution a fresh copy). Two side effects though:

1. `intervals.sort(...)` reorders the caller's list.
2. It appends the caller's own `pair` objects to `merged` and then edits `merged[-1][1]`,
   so the caller's inner lists get changed too.

Both break the "don't modify the input" rule, and the second one is nasty because the
caller's data changes later, somewhere far from this function. Fix by sorting a copy with
`sorted()` and appending `[start, end]` as a new list.

This is the case for keeping targeted checks alongside random testing: some bugs don't
show up in the return value at all.
