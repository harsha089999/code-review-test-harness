from collections import Counter


def top_k(words, k):
    """k most frequent words, highest count first, ties broken alphabetically."""
    counts = Counter(words)
    ranked = sorted(counts, key=lambda word: (-counts[word], word))
    return ranked[:k]
