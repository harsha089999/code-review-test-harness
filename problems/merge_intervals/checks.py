"""Checks for merge_intervals. Each check targets one specific way to get it wrong."""

import copy


def check_example(m):
    got = m.merge([[1, 3], [2, 6], [8, 10], [15, 18]])
    assert got == [[1, 6], [8, 10], [15, 18]], f"got {got}"


def check_empty(m):
    assert m.merge([]) == [], "empty input should give []"


def check_unsorted_input(m):
    got = m.merge([[8, 10], [1, 3], [2, 6]])
    assert got == [[1, 6], [8, 10]], f"unsorted input gave {got}"


def check_touching_edges(m):
    got = m.merge([[1, 3], [3, 5]])
    assert got == [[1, 5]], f"touching intervals should merge, got {got}"


def check_contained_interval(m):
    got = m.merge([[1, 10], [2, 3]])
    assert got == [[1, 10]], f"[2,3] sits inside [1,10], got {got}"


def check_does_not_mutate_input(m):
    original = [[5, 7], [1, 2], [2, 4]]
    snapshot = copy.deepcopy(original)
    m.merge(original)
    assert original == snapshot, f"input was modified to {original}"


def check_single_point_intervals(m):
    got = m.merge([[4, 4], [4, 4], [1, 1]])
    assert got == [[1, 1], [4, 4]], f"got {got}"


CHECKS = [
    ("example", check_example),
    ("empty", check_empty),
    ("unsorted_input", check_unsorted_input),
    ("touching_edges", check_touching_edges),
    ("contained_interval", check_contained_interval),
    ("does_not_mutate_input", check_does_not_mutate_input),
    ("single_point_intervals", check_single_point_intervals),
]


def random_input(rng):
    intervals = []
    for _ in range(rng.randint(0, 8)):
        start = rng.randint(0, 20)
        intervals.append([start, start + rng.randint(0, 6)])
    return intervals


def call(module, inp):
    return module.merge(inp)
