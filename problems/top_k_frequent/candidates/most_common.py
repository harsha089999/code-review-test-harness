from collections import Counter


def top_k(words, k):
    return [word for word, _ in Counter(words).most_common(k)]
