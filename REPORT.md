# Scorecard

## lru_cache

| candidate | verdict | checks passed | random mismatches | time (s) |
|---|---|---|---|---|
| reference | PASS | 7/7 | 0/300 | 0.05 |
| evicts_on_update | FAIL | 6/7 | 21/300 | 0.05 |
| get_no_refresh | FAIL | 6/7 | 29/300 | 0.05 |
| list_based | FAIL | 6/7 | 0/300 | 1.11 |
| update_no_refresh | FAIL | 6/7 | 15/300 | 0.05 |

**evicts_on_update**
- failed `update_at_capacity_keeps_others`: updating an existing key evicted an unrelated key
- smallest random mismatch:
      input=(2, [('get', 1), ('get', 3), ('put', 5, 40), ('get', 5), ('put', 0, 63), ('get', 4), ('get', 0), ('put', 0, 6), ('get', 2), ('get', 1), ('get', 5)])
      expected=[-1, -1, 40, -1, 63, -1, -1, 40]
      got=[-1, -1, 40, -1, 63, -1, -1, -1]

**get_no_refresh**
- failed `get_refreshes_recency`: get(1) should have protected key 1, so key 2 is evicted
- smallest random mismatch:
      input=(4, [('put', 2, 12), ('put', 0, 91), ('put', 1, 52), ('put', 5, 66), ('put', 6, 27), ('get', 4), ('get', 0), ('put', 4, 87), ('put', 5, 92), ('get', 2), ('put', 1, 76), ('put', 1, 64), ('get', 0), ('put', 0, 48)])
      expected=[-1, 91, -1, 91]
      got=[-1, 91, -1, -1]

**list_based**
- failed `performance`: took 1.07s vs reference 0.02s; operations are not O(1)

**update_no_refresh**
- failed `update_refreshes_recency`: updating key 1 should make key 2 the eviction target
- smallest random mismatch:
      input=(3, [('put', 1, 12), ('get', 1), ('put', 4, 26), ('get', 6), ('put', 4, 37), ('put', 5, 46), ('put', 0, 46), ('put', 1, 86), ('put', 2, 26), ('put', 0, 65), ('get', 6), ('put', 2, 73), ('get', 5), ('get', 4), ('put', 5, 32), ('get', 1)])
      expected=[12, -1, -1, -1, -1, -1]
      got=[12, -1, -1, -1, -1, 86]

## merge_intervals

| candidate | verdict | checks passed | random mismatches | time (s) |
|---|---|---|---|---|
| reference | PASS | 7/7 | 0/300 | 0.01 |
| contained_shrink | FAIL | 6/7 | 115/300 | 0.01 |
| mutates_input | FAIL | 6/7 | 0/300 | 0.01 |
| no_sort | FAIL | 5/7 | 207/300 | 0.01 |
| touching_gap | FAIL | 5/7 | 77/300 | 0.01 |

**contained_shrink**
- failed `contained_interval`: [2,3] sits inside [1,10], got [[1, 3]]
- smallest random mismatch:
      input=[[9, 11], [9, 10]]
      expected=[[9, 11]]
      got=[[9, 10]]

**mutates_input**
- failed `does_not_mutate_input`: input was modified to [[1, 4], [2, 4], [5, 7]]

**no_sort**
- failed `unsorted_input`: unsorted input gave [[8, 10]]
- failed `single_point_intervals`: got [[4, 4]]
- smallest random mismatch:
      input=[[8, 9], [2, 4]]
      expected=[[2, 4], [8, 9]]
      got=[[8, 9]]

**touching_gap**
- failed `touching_edges`: touching intervals should merge, got [[1, 3], [3, 5]]
- failed `single_point_intervals`: got [[1, 1], [4, 4], [4, 4]]
- smallest random mismatch:
      input=[[2, 6], [6, 7]]
      expected=[[2, 7]]
      got=[[2, 6], [6, 7]]

## top_k_frequent

| candidate | verdict | checks passed | random mismatches | time (s) |
|---|---|---|---|---|
| reference | PASS | 6/6 | 0/300 | 0.01 |
| heap_overflow | FAIL | 4/6 | 149/300 | 0.03 |
| most_common | FAIL | 4/6 | 166/300 | 0.01 |
| reversed_ties | FAIL | 4/6 | 203/300 | 0.01 |

**heap_overflow**
- failed `k_larger_than_distinct`: crashed: IndexError('index out of range')
- failed `empty_words`: crashed: IndexError('index out of range')
- smallest random mismatch:
      input=([], 5)
      expected=[]
      got='<crash: IndexError: index out of range>'

**most_common**
- failed `example`: got ['b', 'a']
- failed `tie_broken_alphabetically`: ties should be alphabetical, got ['pear', 'apple']
- smallest random mismatch:
      input=(['fox', 'cat'], 7)
      expected=['cat', 'fox']
      got=['fox', 'cat']

**reversed_ties**
- failed `example`: got ['b', 'a']
- failed `tie_broken_alphabetically`: ties should be alphabetical, got ['pear', 'apple']
- smallest random mismatch:
      input=(['eel', 'fox'], 1)
      expected=['eel']
      got=['fox']
