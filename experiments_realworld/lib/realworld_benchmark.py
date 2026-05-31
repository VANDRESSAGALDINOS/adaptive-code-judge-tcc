#!/usr/bin/env python3
"""
Generic real-world benchmark template.

This is the "casca" (shell): a single, problem-agnostic driver that runs the
two pillars of the work on any real-world (CSES) problem, using the SAME
validated measurement methodology as the theoretical pipeline (project items
3-6), imported from the shared engine. A new problem is added by writing a thin
config that points this template at its files and supplies its output
validator -- no change to the engine or to this template.

Pillars:
  1. Calibration of beta on the automatically selected largest test case
     (item 7, option 1: largest input in bytes, ties broken by smaller id),
     with a 95% bootstrap CI and raw per-repetition data.
  2. Verdict phase: traditional system (same time limit for both languages)
     vs adaptive system (C++ limit, Python limit scaled by beta), per case,
     producing the injustice metrics (TLE reduction / cases rescued).
"""
import os
import sys
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

# Import the shared engine as a top-level module (add experiments/lib to path).
# Done by path rather than as a package to avoid any `lib` package-name clash
# between the engine's package and the real-world tree.
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(_REPO_ROOT, 'experiments', 'lib'))
sys.path.append(os.path.join(_REPO_ROOT, 'src'))

import benchmark_engine
from config.app import AppConfig


class RealWorldBenchmark:
    """
    Generic real-world benchmark driver.

    Parameters (per problem):
      problem_name           : label used in output/JSON.
      input_dir / output_dir : dirs holding `<id>.in` / `<id>.out` files.
      optimal_dir            : dir with the optimal `solution.cpp` / `solution.py`
                               used for calibration (and the verdict phase here).
      results_dir            : where JSON outputs are written.
      validate_fn            : callable(expected, actual) -> bool for correctness;
                               None means exact string match (engine default).
      traditional_time_limit : judge limit (s) used by both languages in the
                               traditional system; defaults to AppConfig value.
      critical_cases /
      control_cases          : optional CSES categorization, recorded as metadata.
    """

    def __init__(self, *, problem_name, input_dir, output_dir, optimal_dir,
                 results_dir, suboptimal_dir=None, validate_fn=None,
                 traditional_time_limit=None,
                 critical_cases=None, control_cases=None, output_suffix=''):
        self.problem_name = problem_name
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.optimal_dir = Path(optimal_dir)
        self.suboptimal_dir = Path(suboptimal_dir) if suboptimal_dir else None
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.validate_fn = validate_fn
        self.traditional_time_limit = (
            traditional_time_limit
            if traditional_time_limit is not None
            else AppConfig.DEFAULT_TIME_LIMIT
        )
        self.critical_cases = critical_cases or []
        self.control_cases = control_cases or []
        # Output filename suffix (e.g. '_iterative') so variants of the same
        # problem do not overwrite each other's calibration/verdict files.
        self.output_suffix = output_suffix

    # ---- test-case discovery / selection -------------------------------------

    def discover_cases(self):
        """All `<id>.in` files present in input_dir (no pre-filtering)."""
        cases = []
        for in_path in sorted(self.input_dir.glob('*.in')):
            stem = in_path.stem
            cases.append({
                'id': int(stem) if stem.isdigit() else stem,
                'name': in_path.name,
                'input_path': in_path,
                'output_path': self.output_dir / f'{stem}.out',
                'size': in_path.stat().st_size,
            })
        if not cases:
            raise FileNotFoundError(f"No .in files found in {self.input_dir}")
        return cases

    def select_largest_case(self, cases):
        """Largest input in bytes; ties broken by smaller numeric id (item 7)."""
        return benchmark_engine.select_largest_test_case(
            cases,
            size_fn=lambda c: c['size'],
            id_fn=lambda c: c['id'] if isinstance(c['id'], int) else 0,
        )

    def _load_sources(self, solutions='optimal'):
        """Load (cpp, py) sources for 'optimal' or 'suboptimal' implementations."""
        if solutions == 'suboptimal':
            if self.suboptimal_dir is None:
                raise ValueError("suboptimal_dir not configured for this problem")
            src_dir = self.suboptimal_dir
        else:
            src_dir = self.optimal_dir
        cpp = (src_dir / 'solution.cpp').read_text()
        py = (src_dir / 'solution.py').read_text()
        return cpp, py

    def _load_optimal_sources(self):
        return self._load_sources('optimal')

    # ---- phase 1: calibration of beta ----------------------------------------

    def run_calibration(self, case_override=None):
        cases = self.discover_cases()
        if case_override is not None:
            case = next((c for c in cases if c['id'] == case_override), None)
            if case is None:
                raise ValueError(f"Requested case {case_override} not found")
        else:
            case = self.select_largest_case(cases)

        input_data = case['input_path'].read_text()
        if not case['output_path'].exists():
            raise FileNotFoundError(f"Expected output {case['output_path']} not found")
        expected = case['output_path'].read_text()
        cpp_src, py_src = self._load_optimal_sources()

        print(f"=== CALIBRATION: {self.problem_name} ===")
        print(f"Selected test case: {case['name']} "
              f"({case['size']} bytes) -- largest input in bytes (item 7)")
        print(f"Solutions: optimal C++ vs optimal Python")
        print(f"Adaptive: blocks of {AppConfig.BENCHMARK_BLOCK_SIZE}, "
              f"cap {AppConfig.BENCHMARK_MAX_REPETITIONS}, "
              f"IQR/median < {AppConfig.BENCHMARK_IQR_THRESHOLD_CPP*100:.0f}% (C++) "
              f"/ {AppConfig.BENCHMARK_IQR_THRESHOLD_PYTHON*100:.0f}% (Python)")

        print("Measuring C++ (compiled once, startup excluded, adaptive)...")
        cpp = benchmark_engine.measure_language(
            cpp_src, input_data, expected, 'cpp',
            AppConfig.BENCHMARK_IQR_THRESHOLD_CPP, validate_fn=self.validate_fn
        )
        print("Measuring Python (startup excluded, adaptive)...")
        py = benchmark_engine.measure_language(
            py_src, input_data, expected, 'python',
            AppConfig.BENCHMARK_IQR_THRESHOLD_PYTHON, validate_fn=self.validate_fn
        )

        beta_result = benchmark_engine.compute_beta(cpp, py, case['name'])

        out = {
            'problem': self.problem_name,
            'phase': 'calibration',
            'timestamp': datetime.now().isoformat(),
            'selected_case': {
                'id': case['id'],
                'name': case['name'],
                'input_bytes': case['size'],
                'selection_criterion': 'largest input in bytes, ties by smaller id (item 7, option 1)',
            },
            'solutions': 'optimal',
            'benchmark': beta_result,
        }
        out_file = self.results_dir / f'calibration{self.output_suffix}.json'
        with open(out_file, 'w') as f:
            json.dump(out, f, indent=2)
        print(f"Calibration results saved to: {out_file}")
        return out

    # ---- phase 2: verdict (traditional vs adaptive) --------------------------

    def run_validation(self, beta, cases_override=None, repetitions=10,
                       traditional_limit=None, solutions='optimal'):
        traditional_limit = (
            traditional_limit if traditional_limit is not None
            else self.traditional_time_limit
        )
        adaptive_python_limit = traditional_limit * beta

        cases = self.discover_cases()
        if cases_override:
            wanted = set(cases_override)
            cases = [c for c in cases if c['id'] in wanted]
        cpp_src, py_src = self._load_sources(solutions)

        print(f"=== VERDICT PHASE: {self.problem_name} ===")
        print(f"Solutions: {solutions}")
        print(f"Cases: {[c['id'] for c in cases]}")
        print(f"Repetitions/case: {repetitions}")
        print(f"Traditional limit: {traditional_limit:.2f}s (both languages)")
        print(f"Adaptive limit: C++ {traditional_limit:.2f}s, "
              f"Python {adaptive_python_limit:.2f}s (= {traditional_limit:.2f}s x beta {beta:.3f})")

        results = {
            'problem': self.problem_name,
            'phase': 'verdict',
            'timestamp': datetime.now().isoformat(),
            'metadata': {
                'beta': beta,
                'traditional_limit': traditional_limit,
                'adaptive_python_limit': adaptive_python_limit,
                'repetitions': repetitions,
                'critical_cases': self.critical_cases,
                'control_cases': self.control_cases,
                'solutions': solutions,
            },
            'cases': {},
        }

        for case in cases:
            cid = case['id']
            input_data = case['input_path'].read_text()
            expected = case['output_path'].read_text() if case['output_path'].exists() else ''

            trad_cpp = benchmark_engine.run_timed_trials(
                cpp_src, input_data, expected, 'cpp',
                repetitions, traditional_limit, validate_fn=self.validate_fn)
            trad_py = benchmark_engine.run_timed_trials(
                py_src, input_data, expected, 'python',
                repetitions, traditional_limit, validate_fn=self.validate_fn)
            adapt_cpp = benchmark_engine.run_timed_trials(
                cpp_src, input_data, expected, 'cpp',
                repetitions, traditional_limit, validate_fn=self.validate_fn)
            adapt_py = benchmark_engine.run_timed_trials(
                py_src, input_data, expected, 'python',
                repetitions, adaptive_python_limit, validate_fn=self.validate_fn)

            def summarize(trials):
                # Per-(system,language) case verdict = dominant trial status;
                # success_rate kept for transparency.
                acc = sum(1 for t in trials if t['status'] == 'ACCEPTED')
                verdict = (Counter(t['status'] for t in trials).most_common(1)[0][0]
                           if trials else 'NO_DATA')
                return {
                    'verdict': verdict,
                    'success_rate': acc / len(trials) if trials else 0.0,
                    'trials': trials,
                }

            rec = {
                'input_bytes': case['size'],
                'traditional': {'cpp': summarize(trad_cpp), 'python': summarize(trad_py)},
                'adaptive': {'cpp': summarize(adapt_cpp), 'python': summarize(adapt_py)},
            }
            results['cases'][cid] = rec
            print(f"  case {cid} ({case['size']} B): "
                  f"trad[cpp={rec['traditional']['cpp']['verdict']}, "
                  f"py={rec['traditional']['python']['verdict']}] "
                  f"adapt[py={rec['adaptive']['python']['verdict']}]")

        if solutions == 'suboptimal':
            self._summarize_selectivity(results)
            out_file = self.results_dir / f'verdict_suboptimal{self.output_suffix}.json'
        else:
            self._summarize_verdict(results)
            out_file = self.results_dir / f'verdict{self.output_suffix}.json'
        with open(out_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Verdict results saved to: {out_file}")
        return results

    @staticmethod
    def _summarize_verdict(results):
        """
        Aggregate the unjust-TLE metrics (the work's core claim):
          - unjust TLE under the traditional system = a case where C++ optimal
            is ACCEPTED but Python optimal is TLE (same algorithm, only the
            language is punished);
          - resolved under the adaptive system = such a case where Python
            optimal becomes ACCEPTED under its beta-scaled limit;
          - reduction rate = resolved / unjust(traditional).
        Cases with WRONG_ANSWER on any branch are surfaced for inspection.
        """
        cases = results['cases']
        unjust_trad = []
        unjust_resolved = []
        wa_cases = []
        for cid, rec in cases.items():
            verdicts = (
                rec['traditional']['cpp']['verdict'],
                rec['traditional']['python']['verdict'],
                rec['adaptive']['cpp']['verdict'],
                rec['adaptive']['python']['verdict'],
            )
            if 'WRONG_ANSWER' in verdicts:
                wa_cases.append(cid)
            if (rec['traditional']['cpp']['verdict'] == 'ACCEPTED'
                    and rec['traditional']['python']['verdict'] == 'TLE'):
                unjust_trad.append(cid)
                if rec['adaptive']['python']['verdict'] == 'ACCEPTED':
                    unjust_resolved.append(cid)

        reduction = (len(unjust_resolved) / len(unjust_trad)) if unjust_trad else None
        results['aggregate'] = {
            'total_cases': len(cases),
            'unjust_tle_traditional': len(unjust_trad),
            'unjust_tle_traditional_cases': unjust_trad,
            'unjust_tle_resolved_adaptive': len(unjust_resolved),
            'unjust_tle_resolved_cases': unjust_resolved,
            'unjust_tle_reduction_rate': reduction,
            'cases_with_wrong_answer': wa_cases,
        }

        print(f"\nAGGREGATE:")
        print(f"  Total cases: {len(cases)}")
        print(f"  Unjust TLE (traditional, C++ AC + Python TLE): {len(unjust_trad)} {unjust_trad}")
        print(f"  Resolved by adaptive (Python AC): {len(unjust_resolved)} {unjust_resolved}")
        print(f"  Unjust-TLE reduction rate: "
              f"{'n/a' if reduction is None else f'{reduction:.0%}'}")
        if wa_cases:
            print(f"  WARNING - WRONG_ANSWER on cases: {wa_cases}")

    @staticmethod
    def _summarize_selectivity(results):
        """
        Selectivity check for the suboptimal (deliberately inefficient) solution:
        the adaptive limit must NOT rescue genuinely slow code. Per case, using
        the suboptimal Python verdict:
          - candidates       = cases where suboptimal Python is TLE under the
            traditional limit (the only cases the adaptive limit could rescue);
          - rescued_adaptive = candidates that become ACCEPTED under the adaptive
            (beta-scaled) limit. These would be FALSE rescues; the goal is zero;
          - selectivity_preserved = no candidate was rescued.
        WRONG_ANSWER on any branch is surfaced for inspection.
        """
        cases = results['cases']
        candidates = []
        rescued = []
        wa_cases = []
        for cid, rec in cases.items():
            trad_py = rec['traditional']['python']['verdict']
            adapt_py = rec['adaptive']['python']['verdict']
            verdicts = (
                rec['traditional']['cpp']['verdict'], trad_py,
                rec['adaptive']['cpp']['verdict'], adapt_py,
            )
            if 'WRONG_ANSWER' in verdicts:
                wa_cases.append(cid)
            if trad_py == 'TLE':
                candidates.append(cid)
                if adapt_py == 'ACCEPTED':
                    rescued.append(cid)

        results['aggregate'] = {
            'total_cases': len(cases),
            'tle_traditional_python': len(candidates),
            'tle_traditional_python_cases': candidates,
            'rescued_by_adaptive': len(rescued),
            'rescued_by_adaptive_cases': rescued,
            'selectivity_preserved': len(rescued) == 0,
            'cases_with_wrong_answer': wa_cases,
        }

        print(f"\nAGGREGATE (selectivity):")
        print(f"  Total cases: {len(cases)}")
        print(f"  Suboptimal Python TLE (traditional): {len(candidates)} {candidates}")
        print(f"  Rescued by adaptive (goal 0): {len(rescued)} {rescued}")
        print(f"  Selectivity preserved: {len(rescued) == 0}")
        if wa_cases:
            print(f"  WARNING - WRONG_ANSWER on cases: {wa_cases}")
