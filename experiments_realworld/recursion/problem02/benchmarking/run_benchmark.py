#!/usr/bin/env python3
"""
Benchmark runner for recursion/problem02 (CSES 1139 - Distinct Colors).

Deep-recursion design: a SINGLE optimal style (recursive DFS + small-to-large
merging of subtree color-sets). Recursion is the natural form of the tree DFS,
so there is one optimal -> one beta. The suboptimal (same DFS but naive merging,
i.e. WITHOUT small-to-large -> O(n^2) in the worst case) is the selectivity
check, created in the suboptimal phase.

Cost driver is the recursion + set work over n nodes (n up to 2*10^5); several
large cases share near-identical byte sizes, so the "largest input by bytes"
selector may not pick the time-heaviest. Override with --case to a Python-TLE
case (e.g. one of {6,7,8}).

Output is n space-separated integers per case -> engine default exact-match
validator. All measurement methodology lives in the shared template + engine.
"""
import sys
import json
import argparse
from pathlib import Path

_BASE = Path(__file__).resolve().parents[1]          # .../recursion/problem02
_RW_ROOT = Path(__file__).resolve().parents[3]        # .../experiments_realworld
sys.path.insert(0, str(_RW_ROOT / 'lib'))

from realworld_benchmark import RealWorldBenchmark


def build_benchmark():
    return RealWorldBenchmark(
        problem_name='recursion/problem02 (CSES 1139 - Distinct Colors)',
        input_dir=_BASE / 'test_data' / 'input',
        output_dir=_BASE / 'test_data' / 'output',
        optimal_dir=_BASE / 'implementations' / 'optimal',
        suboptimal_dir=_BASE / 'implementations' / 'suboptimal',
        results_dir=_BASE / 'results',
        # n integers on one line -> engine default exact-match validator.
        validate_fn=None,
        traditional_time_limit=1.0,
        # CSES (optimal, 2026-05-31): Python TLE {6,7,8} (borderline elsewhere);
        # C++ AC 16/16.
        critical_cases=[6, 7, 8],
        control_cases=[1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16],
    )


def _beta_from_calibration(bench):
    calib = bench.results_dir / 'calibration.json'
    if not calib.exists():
        raise FileNotFoundError(
            f"No {calib.name} found; run --phase calibration first or pass --beta")
    with open(calib) as f:
        return json.load(f)['benchmark']['adjustment_factor']


def main():
    parser = argparse.ArgumentParser(description='recursion/problem02 benchmark (CSES 1139)')
    parser.add_argument('--phase', choices=['calibration', 'verdict'], required=True)
    parser.add_argument('--case', type=int, default=None,
                        help='Manual override of the calibration case (default: largest by bytes; '
                             'use a Python-TLE case e.g. 6, since bytes may not distinguish)')
    parser.add_argument('--cases', type=str, default=None,
                        help='Comma-separated case ids for the verdict phase (default: all)')
    parser.add_argument('--repetitions', type=int, default=None)
    parser.add_argument('--beta', type=float, default=None,
                        help='Adjustment factor for the verdict phase (default: from calibration.json)')
    parser.add_argument('--solutions', choices=['optimal', 'suboptimal'], default='optimal',
                        help='Which implementation to run in the verdict phase '
                             '(suboptimal = selectivity check, writes verdict_suboptimal.json)')
    args = parser.parse_args()

    bench = build_benchmark()

    if args.phase == 'calibration':
        bench.run_calibration(case_override=args.case)
    elif args.phase == 'verdict':
        beta = args.beta if args.beta is not None else _beta_from_calibration(bench)
        cases = ([int(x.strip()) for x in args.cases.split(',')] if args.cases else None)
        repetitions = args.repetitions or 10
        bench.run_validation(beta=beta, cases_override=cases, repetitions=repetitions,
                             solutions=args.solutions)


if __name__ == '__main__':
    main()
