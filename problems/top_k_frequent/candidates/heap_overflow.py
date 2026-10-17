import heapq
from collections import Counter


def top_k(words, k):
    counts = Counter(words)
    heap = [(-count, word) for word, count in counts.items()]
    heapq.heapify(heap)
    return [heapq.heappop(heap)[1] for _ in range(k)]
