#!/usr/bin/env python3
"""
Benchmark runner for graphs/problem01 (CSES 1672 - Shortest Routes II,
Floyd-Warshall, all-pairs shortest paths).

Thin per-problem configuration: it only points the generic RealWorldBenchmark
template at this problem's files. The output is deterministic numeric (q
distances or -1), so the engine's default exact-match correctness check is
used (no custom validator). All measurement methodology lives in the shared
template + engine.
"""
import sys
import json
import argparse
from pathlib import Path

# Locate the real-world template (experiments_realworld/lib) and import it.
_BASE = Path(__file__).resolve().parents[1]          # .../graphs/problem01
_RW_ROOT = Path(__file__).resolve().parents[3]       # .../experiments_realworld
sys.path.insert(0, str(_RW_ROOT / 'lib'))

from realworld_benchmark import RealWorldBenchmark


def build_benchmark():
    return RealWorldBenchmark(
        problem_name='graphs/problem01 (CSES 1672 - Shortest Routes II)',
        input_dir=_BASE / 'test_data' / 'input',
        output_dir=_BASE / 'test_data' / 'output',
        optimal_dir=_BASE / 'implementations' / 'optimal',
        suboptimal_dir=_BASE / 'implementations' / 'suboptimal',
        results_dir=_BASE / 'results',
        # Deterministic numeric output -> engine default exact-match validator.
        validate_fn=None,
        traditional_time_limit=1.0,
        # CSES verdict (submission 28/05/2026): Python optimal TLE set.
        critical_cases=[6, 7, 8, 9, 10, 11, 12, 14, 15],
        control_cases=[1, 2, 3, 4, 5, 13, 16],
    )


def _beta_from_calibration(bench):
    calib = bench.results_dir / 'calibration.json'
    if not calib.exists():
        raise FileNotFoundError(
            "No calibration.json found; run --phase calibration first or pass --beta")
    with open(calib) as f:
        return json.load(f)['benchmark']['adjustment_factor']


def main():
    parser = argparse.ArgumentParser(description='graphs/problem01 benchmark (CSES 1672)')
    parser.add_argument('--phase', choices=['calibration', 'verdict'], required=True)
    parser.add_argument('--case', type=int, default=None,
                        help='Manual override of the calibration case (default: largest by bytes)')
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
