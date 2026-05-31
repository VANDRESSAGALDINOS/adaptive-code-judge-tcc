#!/usr/bin/env python3
"""
Benchmark runner for backtracking/problem01 (CSES 1624 - Chessboard and Queens).

Backtracking design: a SINGLE optimal style (recursive DFS with constraint
pruning). Backtracking has no idiomatic iterative counterpart (an "iterative
backtracking" would just be a hand-rolled call stack over the same decision
tree), so there is one optimal -> one beta. The suboptimal (same recursive
search WITHOUT the column/diagonal pruning) is the selectivity check.

Cost driver is the size of the search tree (number of free squares / blocked
pattern), NOT input bytes (every input is a fixed 8x8 board = 72 bytes), so the
calibration case must be overridden to the heaviest tree (the empty board,
case 1 = 92 solutions) via --case 1.

Output is a single integer per case -> engine default exact-match validator.
All measurement methodology lives in the shared template + engine.
"""
import sys
import json
import argparse
from pathlib import Path

_BASE = Path(__file__).resolve().parents[1]          # .../backtracking/problem01_chessboard_queens
_RW_ROOT = Path(__file__).resolve().parents[3]        # .../experiments_realworld
sys.path.insert(0, str(_RW_ROOT / 'lib'))

from realworld_benchmark import RealWorldBenchmark


def build_benchmark():
    return RealWorldBenchmark(
        problem_name='backtracking/problem01 (CSES 1624 - Chessboard and Queens)',
        input_dir=_BASE / 'test_data' / 'input',
        output_dir=_BASE / 'test_data' / 'output',
        optimal_dir=_BASE / 'implementations' / 'optimal',
        suboptimal_dir=_BASE / 'implementations' / 'suboptimal',
        results_dir=_BASE / 'results',
        # Single deterministic integer output -> engine default exact-match.
        validate_fn=None,
        traditional_time_limit=1.0,
        # CSES (optimal): both C++ and Python AC 10/10 (trivial for the pruned
        # search); injustice does not show on the optimal here -- queens' value
        # is the selectivity dimension (suboptimal). Filled per PASSO B.
        critical_cases=[],
        control_cases=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    )


def _beta_from_calibration(bench):
    calib = bench.results_dir / 'calibration.json'
    if not calib.exists():
        raise FileNotFoundError(
            f"No {calib.name} found; run --phase calibration first or pass --beta")
    with open(calib) as f:
        return json.load(f)['benchmark']['adjustment_factor']


def main():
    parser = argparse.ArgumentParser(description='backtracking/problem01 benchmark (CSES 1624)')
    parser.add_argument('--phase', choices=['calibration', 'verdict'], required=True)
    parser.add_argument('--case', type=int, default=None,
                        help='Manual override of the calibration case (default: largest by bytes; '
                             'use 1 = empty board, the cost-heaviest, since all inputs are 72 B)')
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
