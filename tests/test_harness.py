"""Tests for the harness itself.

If any of these fail, the harness is the thing that's broken: either a reference
solution no longer passes its own checks, or a known buggy candidate is slipping through.
"""

import pytest

from harness.runner import PROBLEMS_DIR, run_problem

PROBLEMS = sorted(p.name for p in PROBLEMS_DIR.iterdir() if (p / "checks.py").exists())


@pytest.fixture(scope="module", params=PROBLEMS)
def results(request):
    return request.param, run_problem(PROBLEMS_DIR / request.param)


def test_reference_passes_everything(results):
    name, rows = results
    reference = rows[0]
    assert reference.candidate == "reference"
    assert reference.verdict == "PASS", f"{name}: reference failed {reference.failed}"


def test_every_buggy_candidate_is_caught(results):
    name, rows = results
    for row in rows[1:]:
        assert row.verdict == "FAIL", f"{name}/{row.candidate} was not caught"


def test_each_candidate_fails_a_targeted_check(results):
    # Random testing alone misses some bugs (e.g. input mutation), so every buggy
    # candidate should be pinned down by at least one hand-written check.
    name, rows = results
    for row in rows[1:]:
        assert row.failed, f"{name}/{row.candidate} only caught by random tests"
