#!/usr/bin/env python3
"""
Benchmark runner for dp/problem02 (CSES 1638 - Grid Paths).

DP design: two optimal styles, ITERATIVE (bottom-up, forward) and RECURSIVE
(top-down + memoization, backward), both O(n^2). The runner calibrates beta and
runs the verdict per STYLE (--variant), with output_suffix '_iterative' /
'_recursive' so the styles do not overwrite each other's results. The suboptimal
(per style) is the selectivity check (--solutions suboptimal).

Output is a single integer per case -> engine default exact-match validator.
All measurement methodology lives in the shared template + engine.
"""
import sys
import json
import argparse
from pathlib import Path

_BASE = Path(__file__).resolve().parents[1]          # .../dp/problem02
_RW_ROOT = Path(__file__).resolve().parents[3]        # .../experiments_realworld
sys.path.insert(0, str(_RW_ROOT / 'lib'))

from realworld_benchmark import RealWorldBenchmark


def build_benchmark(variant):
    # variant in {'iterative', 'recursive'} selects which optimal style is the
    # reference; output files are suffixed accordingly.
    return RealWorldBenchmark(
        problem_name=f'dp/problem02 (CSES 1638 - Grid Paths, {variant})',
        input_dir=_BASE / 'test_data' / 'input',
        output_dir=_BASE / 'test_data' / 'output',
        optimal_dir=_BASE / 'implementations' / f'optimal_{variant}',
        suboptimal_dir=_BASE / 'implementations' / f'suboptimal_{variant}',
        results_dir=_BASE / 'results',
        # Single deterministic integer output -> engine default exact-match.
        validate_fn=None,
        traditional_time_limit=1.0,
        output_suffix=f'_{variant}',
        # CSES (optimal, 2026-05-31): heavy cases; Python recursive TLE on {6,7}.
        critical_cases=[6, 7, 8, 9, 10],
        control_cases=[1, 2, 3, 4, 5, 11, 12, 13, 14, 15],
    )


def _beta_from_calibration(bench):
    calib = bench.results_dir / f'calibration{bench.output_suffix}.json'
    if not calib.exists():
        raise FileNotFoundError(
            f"No {calib.name} found; run --phase calibration --variant ... first or pass --beta")
    with open(calib) as f:
        return json.load(f)['benchmark']['adjustment_factor']


def main():
    parser = argparse.ArgumentParser(description='dp/problem02 benchmark (CSES 1638)')
    parser.add_argument('--phase', choices=['calibration', 'verdict'], required=True)
    parser.add_argument('--variant', choices=['iterative', 'recursive'], required=True,
                        help='Which optimal style is the reference (calibration/verdict)')
    parser.add_argument('--case', type=int, default=None,
                        help='Manual override of the calibration case (default: largest by bytes)')
    parser.add_argument('--cases', type=str, default=None,
                        help='Comma-separated case ids for the verdict phase (default: all)')
    parser.add_argument('--repetitions', type=int, default=None)
    parser.add_argument('--beta', type=float, default=None,
                        help='Adjustment factor for the verdict phase (default: from calibration_<variant>.json)')
    parser.add_argument('--solutions', choices=['optimal', 'suboptimal'], default='optimal',
                        help='Which implementation to run in the verdict phase '
                             '(suboptimal = selectivity check, writes verdict_suboptimal_<variant>.json)')
    args = parser.parse_args()

    bench = build_benchmark(args.variant)

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
