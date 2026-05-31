#!/usr/bin/env python3
"""
Benchmark runner for recursion/problem03 (CSES 1132 - Tree Distances I).

Deep-recursion design: a SINGLE optimal style (recursive DFS rerooting, two
passes: down1/down2 downward + up via parent). Recursion is the natural form of
the tree DFS, so there is one optimal -> one beta. The suboptimal (one separate
DFS per node, no rerooting -> O(n^2)) is the selectivity check.

Same rerooting TECHNIQUE as problem01 (Tree Distances II) but a different task
(max distance vs sum of distances). Cost driver scales with n (up to 2*10^5);
several large cases share near-identical byte sizes, so override --case to a
Python-TLE case (e.g. 6) if needed.

Output is n space-separated integers per case -> engine default exact-match
validator. All measurement methodology lives in the shared template + engine.
"""
import sys
import json
import argparse
from pathlib import Path

_BASE = Path(__file__).resolve().parents[1]          # .../recursion/problem03
_RW_ROOT = Path(__file__).resolve().parents[3]        # .../experiments_realworld
sys.path.insert(0, str(_RW_ROOT / 'lib'))

from realworld_benchmark import RealWorldBenchmark


def build_benchmark():
    return RealWorldBenchmark(
        problem_name='recursion/problem03 (CSES 1132 - Tree Distances I)',
        input_dir=_BASE / 'test_data' / 'input',
        output_dir=_BASE / 'test_data' / 'output',
        optimal_dir=_BASE / 'implementations' / 'optimal',
        suboptimal_dir=_BASE / 'implementations' / 'suboptimal',
        results_dir=_BASE / 'results',
        validate_fn=None,
        traditional_time_limit=1.0,
        # CSES (optimal, 2026-05-31): Python TLE {6,7,8,14}; C++ AC 16/16.
        critical_cases=[6, 7, 8, 14],
        control_cases=[1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 15, 16],
    )


def _beta_from_calibration(bench):
    calib = bench.results_dir / 'calibration.json'
    if not calib.exists():
        raise FileNotFoundError(
            f"No {calib.name} found; run --phase calibration first or pass --beta")
    with open(calib) as f:
        return json.load(f)['benchmark']['adjustment_factor']


def main():
    parser = argparse.ArgumentParser(description='recursion/problem03 benchmark (CSES 1132)')
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
