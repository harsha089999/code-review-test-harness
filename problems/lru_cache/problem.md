# LRU cache

Write a class `LRUCache(capacity)` with two methods:

- `get(key)` returns the value, or `-1` if the key isn't there. A successful get makes
  that key the most recently used.
- `put(key, value)` inserts or updates. Updating an existing key also makes it the most
  recently used. If inserting a new key pushes the cache over capacity, evict the least
  recently used key.

Both operations should be O(1) on average. Capacity is at least 1.

Why this problem: most broken LRU caches still pass a basic put/get demo. The bugs hide
in recency tracking (does `get` count? does updating count?) and in when eviction fires.
The performance requirement also matters, because a list-based version is correct but
falls over on real workloads.
