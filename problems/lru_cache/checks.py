"""Checks for lru_cache."""

import importlib.util
import time
from pathlib import Path


def _load_reference():
    path = Path(__file__).with_name("reference.py")
    spec = importlib.util.spec_from_file_location("lru_reference_for_perf", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_basic(m):
    c = m.LRUCache(2)
    c.put(1, "a")
    c.put(2, "b")
    assert c.get(1) == "a"
    assert c.get(3) == -1, "missing key should return -1"


def check_evicts_least_recent(m):
    c = m.LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(3, 3)  # 1 is oldest, should go
    assert c.get(1) == -1, "key 1 should have been evicted"
    assert c.get(2) == 2 and c.get(3) == 3


def check_get_refreshes_recency(m):
    c = m.LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.get(1)      # 1 is now most recent, so 2 is the eviction target
    c.put(3, 3)
    assert c.get(2) == -1, "get(1) should have protected key 1, so key 2 is evicted"
    assert c.get(1) == 1, "key 1 was evicted even though it was just read"


def check_update_refreshes_recency(m):
    c = m.LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(1, 10)  # update counts as a use
    c.put(3, 3)
    assert c.get(2) == -1, "updating key 1 should make key 2 the eviction target"
    assert c.get(1) == 10, "key 1 lost after update"


def check_update_at_capacity_keeps_others(m):
    c = m.LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(2, 20)  # no new key, nothing should be evicted
    assert c.get(1) == 1, "updating an existing key evicted an unrelated key"
    assert c.get(2) == 20


def check_capacity_one(m):
    c = m.LRUCache(1)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == -1 and c.get(2) == 2


def _workload(module, n_ops=30_000, capacity=10_000):
    c = module.LRUCache(capacity)
    for i in range(n_ops):
        c.put(i % (capacity * 2), i)
        c.get((i * 7) % (capacity * 2))


def check_performance(m):
    reference = _load_reference()
    start = time.perf_counter()
    _workload(reference)
    baseline = time.perf_counter() - start

    start = time.perf_counter()
    _workload(m)
    took = time.perf_counter() - start
    limit = max(baseline * 10, 0.25)
    assert took <= limit, (
        f"took {took:.2f}s vs reference {baseline:.2f}s; operations are not O(1)"
    )


CHECKS = [
    ("basic", check_basic),
    ("evicts_least_recent", check_evicts_least_recent),
    ("get_refreshes_recency", check_get_refreshes_recency),
    ("update_refreshes_recency", check_update_refreshes_recency),
    ("update_at_capacity_keeps_others", check_update_at_capacity_keeps_others),
    ("capacity_one", check_capacity_one),
    ("performance", check_performance),
]


def random_input(rng):
    capacity = rng.randint(1, 4)
    ops = []
    for _ in range(rng.randint(1, 25)):
        key = rng.randint(0, 6)
        if rng.random() < 0.5:
            ops.append(("put", key, rng.randint(0, 99)))
        else:
            ops.append(("get", key))
    return capacity, ops


def call(module, inp):
    """Replay the operations and return what every get() returned."""
    capacity, ops = inp
    cache = module.LRUCache(capacity)
    seen = []
    for op in ops:
        if op[0] == "put":
            cache.put(op[1], op[2])
        else:
            seen.append(cache.get(op[1]))
    return seen
