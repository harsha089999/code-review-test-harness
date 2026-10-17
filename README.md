# code-review-test-harness

A small Python project for grading code: given a problem, a known-good reference
solution and a handful of candidate solutions, it works out which candidates are wrong,
shows the smallest input that breaks each one, and pairs that with a written review
explaining the bug and the fix.

I built it to practise the part of software engineering that's mostly reading other
people's code: spotting subtle bugs, writing tests that actually separate correct
solutions from almost-correct ones, and explaining clearly what's wrong.

## How it grades

Every candidate goes through two kinds of testing.

**Targeted checks.** Hand-written tests, each aimed at one specific way to get the
problem wrong (touching interval edges, recency on update, alphabetical tie breaks and
so on). When one fails, its name tells you what the bug is.

**Differential testing.** 300 random inputs (fixed seed, so runs are repeatable) go to
both the reference and the candidate. Any difference in output counts as a mismatch, and
the harness reports the smallest input that triggered one, since that's the easiest
place to start debugging.

Neither is enough alone. Targeted checks only cover the cases I thought of, and random
testing covers lots of input shapes I didn't. But random testing completely misses
`mutates_input.py`, which returns the right answer while quietly changing the caller's
data. The harness's own test suite enforces
that every buggy candidate is caught by at least one targeted check for this reason.

## Problems

| problem | what makes it tricky | candidates |
|---|---|---|
| [merge_intervals](problems/merge_intervals) | unsorted input, touching edges, contained intervals, not mutating input | 4 buggy |
| [lru_cache](problems/lru_cache) | whether reads and updates count as use, when eviction fires, O(1) cost | 3 buggy, 1 correct but too slow |
| [top_k_frequent](problems/top_k_frequent) | alphabetical tie breaks, k larger than the number of distinct words | 3 buggy |

Each problem folder has:

- `problem.md` the spec
- `reference.py` a correct solution
- `candidates/` solutions to grade, each with a realistic bug
- `checks.py` targeted checks plus a random input generator
- `review.md` a written review of every candidate: verdict, what's wrong, how to fix it

## Running it

```bash
pip install -r requirements.txt

python -m harness.runner                      # scorecard for every problem
python -m harness.runner lru_cache            # one problem
python -m harness.runner --report REPORT.md   # also save the scorecard as markdown

pytest -q                                     # tests for the harness itself
```

A saved scorecard is in [REPORT.md](REPORT.md).

## Adding a problem

1. Make `problems/<name>/` with `reference.py` and a `candidates/` folder.
2. Write `checks.py` with a `CHECKS` list of `(name, fn)` pairs, a `random_input(rng)`
   function and a `call(module, inp)` function that runs a solution on one input.
3. Run `pytest`. It fails if the reference doesn't pass its own checks or if any
   candidate isn't caught.

## Design notes

- Solutions are loaded straight from their file paths, so candidates never need to be
  packages or share names.
- Inputs are deep-copied before every call. That keeps a mutating candidate from
  corrupting the reference's input during differential testing.
- The LRU performance check measures the reference on the same machine and allows 10x
  that time, instead of a fixed number of seconds, so it doesn't flake on slow CI.
- A crash during differential testing is recorded as a mismatch with the exception type,
  not as a harness error.

## Tech

Python 3.10+, pytest, GitHub Actions for CI. No other dependencies.
