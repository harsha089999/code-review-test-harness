# Top k frequent words

Write `top_k(words, k)` that returns the `k` most frequent words in `words`.

Rules:

- Order by frequency, highest first.
- Ties are broken alphabetically, so `"apple"` comes before `"banana"` when both appear
  the same number of times.
- If `k` is bigger than the number of distinct words, return all of them (no error).
- `k` of 0 returns an empty list.

Example:

```python
top_k(["b", "a", "c", "a", "b", "d"], 2)
# ["a", "b"]   (a and b both appear twice, a wins the tie)
```

Why this problem: `Counter.most_common` looks like a one-line answer, and it gets the
frequency part right. It doesn't handle the tie rule, and that's exactly the kind of
requirement that gets skimmed past in a quick review.
