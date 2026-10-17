from collections import Counter


def top_k(words, k):
    counts = Counter(words)
    ranked = sorted(counts, key=lambda word: (counts[word], word), reverse=True)
    return ranked[:k]
