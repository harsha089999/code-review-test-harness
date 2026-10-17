# Reviews: lru_cache

## get_no_refresh.py: reject

`get` reads the value without moving the key to the end, so reads don't count as use.
The cache ends up evicting by insertion order (FIFO) instead of recency. A key that's
read constantly will still be thrown out once enough new keys arrive, which defeats the
point of an LRU cache.

Fix: `self._data.move_to_end(key)` before returning, the same way the reference does it.

## update_no_refresh.py: reject

`put` on an existing key assigns `self._data[key] = value`. In a Python dict (and an
OrderedDict) assigning to an existing key keeps its old position, so an update doesn't
make the key recent. The spec says updating counts as use.

Fix: call `move_to_end(key)` when the key already exists. This one is subtle because it
relies on knowing how dict ordering behaves on reassignment.

## evicts_on_update.py: reject

Eviction runs before the code checks whether the key is new. At full capacity, updating
an existing key evicts the least recent entry even though the size wouldn't have grown,
so the cache silently drops a valid entry and runs one below capacity.

Fix: insert or update first, then evict only when `len(self._data) > self.capacity`.

## list_based.py: request changes

Behaviour is correct: every hand-written check except performance passes, and 300 random
operation sequences match the reference exactly. The problem is cost. `list.remove(key)`
and `list.pop(0)` are both O(n), so every get and put walks the order list. On a cache of
10,000 entries that came out roughly 50 times slower than the reference in the harness run,
and it gets worse as capacity grows.

Fix: use `collections.OrderedDict` (`move_to_end`, `popitem(last=False)`), or a dict plus a
doubly linked list if the point of the exercise is to build it by hand.

Note on the performance check: it compares against the reference on the same machine
rather than using a fixed time limit, so it doesn't flake on slower CI runners.
