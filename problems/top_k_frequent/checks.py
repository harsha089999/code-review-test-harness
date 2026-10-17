"""Checks for top_k_frequent."""


def check_example(m):
    got = m.top_k(["b", "a", "c", "a", "b", "d"], 2)
    assert got == ["a", "b"], f"got {got}"


def check_clear_winner(m):
    got = m.top_k(["x", "y", "x", "z", "x", "y"], 2)
    assert got == ["x", "y"], f"got {got}"


def check_tie_broken_alphabetically(m):
    # "pear" is seen first, but "apple" should win the tie
    got = m.top_k(["pear", "apple", "pear", "apple", "kiwi"], 2)
    assert got == ["apple", "pear"], f"ties should be alphabetical, got {got}"


def check_k_larger_than_distinct(m):
    got = m.top_k(["a", "b", "a"], 10)
    assert got == ["a", "b"], f"k > distinct words should return all, got {got}"


def check_k_zero(m):
    assert m.top_k(["a", "b"], 0) == []


def check_empty_words(m):
    assert m.top_k([], 3) == []


CHECKS = [
    ("example", check_example),
    ("clear_winner", check_clear_winner),
    ("tie_broken_alphabetically", check_tie_broken_alphabetically),
    ("k_larger_than_distinct", check_k_larger_than_distinct),
    ("k_zero", check_k_zero),
    ("empty_words", check_empty_words),
]

_VOCAB = ["ant", "bee", "cat", "dog", "eel", "fox", "gnu"]


def random_input(rng):
    words = [rng.choice(_VOCAB) for _ in range(rng.randint(0, 15))]
    return words, rng.randint(0, 9)


def call(module, inp):
    words, k = inp
    return module.top_k(words, k)
