# Reviews: top_k_frequent

## most_common.py: reject

Short and readable, and the frequency ordering is right. The tie rule isn't.
`Counter.most_common` breaks ties by the order words were first seen, not alphabetically,
so `["pear", "apple", "pear", "apple"]` returns `["pear", "apple"]`. It even fails the
example in the problem statement.

Fix: sort the counter keys with `key=lambda w: (-counts[w], w)`. If this pattern is
written often, it's worth a comment, because `most_common` really does look like the
answer.

## reversed_ties.py: reject

Sorts by `(count, word)` with `reverse=True`. That gets the count highest first, but
`reverse` flips the word comparison too, so ties come out reverse alphabetical.

Fix: negate the count instead of reversing: `key=lambda w: (-counts[w], w)` with no
`reverse`. Mixing ascending and descending fields is a common trap with `reverse=True`.

## heap_overflow.py: reject

The heap of `(-count, word)` tuples is a good idea and gives the right tie order for
free. But it pops exactly `k` times, so it crashes with `IndexError` whenever `k` is
bigger than the number of distinct words, including the empty input case.

Fix: `heapq.nsmallest(k, heap)` handles short heaps for you, or loop
`range(min(k, len(heap)))`. For small inputs the plain sort in the reference is simpler.
The heap only pays off when k is much smaller than the number of distinct words.
