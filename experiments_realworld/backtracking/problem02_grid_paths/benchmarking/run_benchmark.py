#!/usr/bin/env python3
"""
Benchmark runner for backtracking/problem02 (CSES 1625 - Grid Paths).

Backtracking design: a SINGLE optimal style (recursive DFS over the 48-move
path with dead-end / trap / early-termination prunings). Backtracking has no
idiomatic iterative counterpart (an iterative version would just be a
hand-rolled call stack over the same decision tree), so there is one optimal ->
one beta. The suboptimal (same search WITHOUT the prunings) is the selectivity
check.

Cost driver is the search-tree size, governed by the number of '?' (free moves)
in the 48-char input, NOT input bytes (every input is 48 chars), so the
calibration case must be overridden to the heaviest tree (case 11, all 48 '?',
output 88418) via --case 11.

Output is a single integer per case -> engine default exact-match validator.
All measurement methodology lives in the shared template + engine.
"""
import sys
import json
import argparse
from pathlib import Path

_BASE = Path(__file__).resolve().parents[1]          # .../backtracking/problem02_grid_paths
_RW_ROOT = Path(__file__).resolve().parents[3]        # .../experiments_realworld
sys.path.insert(0, str(_RW_ROOT / 'lib'))

from realworld_benchmark import RealWorldBenchmark


def build_benchmark():
    return RealWorldBenchmark(
        problem_name='backtracking/problem02 (CSES 1625 - Grid Paths)',
        input_dir=_BASE / 'test_data' / 'input',
        output_dir=_BASE / 'test_data' / 'output',
        optimal_dir=_BASE / 'implementations' / 'optimal',
        suboptimal_dir=_BASE / 'implementations' / 'suboptimal',
        results_dir=_BASE / 'results',
        # Single deterministic integer output -> engine default exact-match.
        validate_fn=None,
        traditional_time_limit=1.0,
        # Filled per PASSO B after the CSES optimal submission.
        critical_cases=[],
        control_cases=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                       11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    )


def _beta_from_calibration(bench):
    calib = bench.results_dir / 'calibration.json'
    if not calib.exists():
        raise FileNotFoundError(
            f"No {calib.name} found; run --phase calibration first or pass --beta")
    with open(calib) as f:
        return json.load(f)['benchmark']['adjustment_factor']


def main():
    parser = argparse.ArgumentParser(description='backtracking/problem02 benchmark (CSES 1625)')
    parser.add_argument('--phase', choices=['calibration', 'verdict'], required=True)
    parser.add_argument('--case', type=int, default=None,
                        help='Manual override of the calibration case (default: largest by bytes; '
                             'use 11 = all 48 "?", the cost-heaviest tree)')
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
