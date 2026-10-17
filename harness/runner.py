"""Run every candidate solution for every problem and print a scorecard.

Each problem folder contains:
  reference.py      the known-good solution
  candidates/*.py   solutions to grade (some deliberately wrong)
  checks.py         defines CHECKS, random_input(rng) and call(module, inp)

A candidate is graded on two things:
  1. Hand-written checks that target specific edge cases.
  2. Differential testing: random inputs are fed to both the reference and the
     candidate, and any output mismatch is recorded with the input that caused it.

Usage:
  python -m harness.runner                 # all problems
  python -m harness.runner merge_intervals # one problem
  python -m harness.runner --report report.md
"""

from __future__ import annotations

import argparse
import copy
import importlib.util
import random
import sys
import time
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS_DIR = ROOT / "problems"
RANDOM_TRIALS = 300
SEED = 1234
SLOW_THRESHOLD_S = 2.0


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@dataclass
class Result:
    candidate: str
    passed: list[str] = field(default_factory=list)
    failed: list[tuple[str, str]] = field(default_factory=list)
    diff_mismatches: int = 0
    smallest_mismatch: str | None = None
    _smallest_size: int = 10**9
    seconds: float = 0.0

    @property
    def verdict(self) -> str:
        if self.failed or self.diff_mismatches:
            return "FAIL"
        if self.seconds > SLOW_THRESHOLD_S:
            return "SLOW"
        return "PASS"


def grade(problem_dir: Path, candidate_path: Path, reference: ModuleType,
          checks: ModuleType) -> Result:
    result = Result(candidate=candidate_path.stem)
    start = time.perf_counter()
    try:
        candidate = load_module(candidate_path, f"cand_{problem_dir.name}_{candidate_path.stem}")
    except Exception as exc:  # syntax errors, import errors
        result.failed.append(("import", repr(exc)))
        return result

    for check_name, check_fn in checks.CHECKS:
        try:
            check_fn(candidate)
            result.passed.append(check_name)
        except AssertionError as exc:
            result.failed.append((check_name, str(exc) or "assertion failed"))
        except Exception as exc:
            result.failed.append((check_name, f"crashed: {exc!r}"))

    rng = random.Random(SEED)
    for _ in range(RANDOM_TRIALS):
        inp = checks.random_input(rng)
        expected = checks.call(reference, copy.deepcopy(inp))
        try:
            actual = checks.call(candidate, copy.deepcopy(inp))
        except Exception:
            actual = f"<crash: {traceback.format_exc(limit=1).strip().splitlines()[-1]}>"
        if actual != expected:
            result.diff_mismatches += 1
            # Keep the smallest failing input: it's the easiest one to debug from.
            size = len(repr(inp))
            if size < result._smallest_size:
                result._smallest_size = size
                result.smallest_mismatch = (
                    f"input={inp!r}\n      expected={expected!r}\n      got={actual!r}"
                )

    result.seconds = time.perf_counter() - start
    return result


def run_problem(problem_dir: Path) -> list[Result]:
    reference = load_module(problem_dir / "reference.py", f"ref_{problem_dir.name}")
    checks = load_module(problem_dir / "checks.py", f"checks_{problem_dir.name}")
    candidates = [problem_dir / "reference.py"] + sorted(
        (problem_dir / "candidates").glob("*.py")
    )
    return [grade(problem_dir, c, reference, checks) for c in candidates]


def format_results(problem: str, results: list[Result]) -> str:
    lines = [f"\n## {problem}\n"]
    lines.append("| candidate | verdict | checks passed | random mismatches | time (s) |")
    lines.append("|---|---|---|---|---|")
    for r in results:
        total = len(r.passed) + len(r.failed)
        lines.append(
            f"| {r.candidate} | {r.verdict} | {len(r.passed)}/{total} | "
            f"{r.diff_mismatches}/{RANDOM_TRIALS} | {r.seconds:.2f} |"
        )
    for r in results:
        if r.failed or r.smallest_mismatch:
            lines.append(f"\n**{r.candidate}**")
            for name, msg in r.failed:
                lines.append(f"- failed `{name}`: {msg}")
            if r.smallest_mismatch:
                lines.append(f"- smallest random mismatch:\n      {r.smallest_mismatch}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("problems", nargs="*", help="problem folder names (default: all)")
    parser.add_argument("--report", help="also write the scorecard to this markdown file")
    args = parser.parse_args(argv)

    names = args.problems or sorted(
        p.name for p in PROBLEMS_DIR.iterdir() if (p / "checks.py").exists()
    )
    output = ["# Scorecard"]
    reference_ok = True
    for name in names:
        results = run_problem(PROBLEMS_DIR / name)
        if results[0].verdict != "PASS":
            reference_ok = False
        output.append(format_results(name, results))

    text = "\n".join(output)
    print(text)
    if args.report:
        Path(args.report).write_text(text + "\n", encoding="utf-8")
    # The harness itself is broken if a reference solution fails its own checks.
    return 0 if reference_ok else 1


if __name__ == "__main__":
    sys.exit(main())
