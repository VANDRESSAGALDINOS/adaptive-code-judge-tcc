#!/usr/bin/env python3
"""
Benchmark runner for graphs/problem02 (CSES 1197 - Cycle Finding, Bellman-Ford).

Thin per-problem configuration: it only points the generic RealWorldBenchmark
template at this problem's files and supplies its output validator. All the
measurement methodology (canonical -O2 / images, startup-excluded timing,
adaptive repetition, bootstrap CI, largest-case selection, verdict phase) lives
in the shared template + engine.
"""
import sys
import json
import argparse
from pathlib import Path

# Locate the real-world template (experiments_realworld/lib) and import it.
_BASE = Path(__file__).resolve().parents[1]          # .../graphs/problem02
_RW_ROOT = Path(__file__).resolve().parents[3]       # .../experiments_realworld
sys.path.insert(0, str(_RW_ROOT / 'lib'))

from realworld_benchmark import RealWorldBenchmark


def validate_cycle_finding(expected_output, actual_output):
    """
    Intelligent validation for cycle finding (CSES 1197): a negative cycle may
    be reported in several valid ways, so we match the YES/NO decision and, for
    YES, accept any returned cycle of at least two nodes.
    """
    expected_lines = expected_output.strip().split('\n')
    actual_lines = actual_output.strip().split('\n')

    if len(expected_lines) == 0 or len(actual_lines) == 0:
        return False

    expected_decision = expected_lines[0].strip()
    actual_decision = actual_lines[0].strip()
    if expected_decision != actual_decision:
        return False

    if expected_decision == "NO":
        return expected_output.strip() == actual_output.strip()

    if expected_decision == "YES":
        if len(actual_lines) < 2:
            return False
        cycle_nodes = actual_lines[1].strip().split()
        return len(cycle_nodes) >= 2

    return False


def build_benchmark():
    return RealWorldBenchmark(
        problem_name='graphs/problem02 (CSES 1197 - Cycle Finding)',
        input_dir=_BASE / 'test_data' / 'input',
        output_dir=_BASE / 'test_data' / 'output',
        optimal_dir=_BASE / 'implementations' / 'optimal',
        suboptimal_dir=_BASE / 'implementations' / 'suboptimal',
        results_dir=_BASE / 'results',
        validate_fn=validate_cycle_finding,
        # CSES submission 14361394 categorization (recorded as metadata only).
        critical_cases=[6, 7, 8, 9, 10, 27],
        control_cases=[1, 2, 3, 4, 5, 11, 12, 13, 14, 15, 16, 17, 18, 20, 22, 23, 24, 25, 26],
    )


def _beta_from_calibration(bench):
    calib = bench.results_dir / 'calibration.json'
    if not calib.exists():
        raise FileNotFoundError(
            "No calibration.json found; run --phase calibration first or pass --beta")
    with open(calib) as f:
        return json.load(f)['benchmark']['adjustment_factor']


def main():
    parser = argparse.ArgumentParser(description='graphs/problem02 benchmark (CSES 1197)')
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
