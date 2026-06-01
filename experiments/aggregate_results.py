#!/usr/bin/env python3
"""
Aggregate the per-class theoretical-axis results into a single results/theoretical_summary.json
for the article and figures. Source of truth stays the per-class JSONs under
complexity_analysis/<class>/results/{calibration.json, selectivity.json}; this just
collects them. Re-run after each class closes:  python3 aggregate_results.py
"""
import json
import glob
import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'complexity_analysis')
# consolidated results live in the root results/ folder (theoretical + real-world side by side)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results', 'theoretical_summary.json')

# O(1) and O(log n) sit below the 10:1 scale-dominance floor (S3.2): runtime is
# dominated by fixed overhead, so beta is not a calibrated algorithmic factor and
# selectivity does not apply. Reported as overhead-floor controls, not calibration.
FLOOR_CLASSES = {'O1_constant', 'O_log_n'}


def load(path):
    with open(path) as f:
        return json.load(f)


def main():
    classes = {}
    for cal_path in sorted(glob.glob(os.path.join(BASE, '*', 'results', 'calibration.json'))):
        cls = cal_path.split(os.sep)[-3]
        cal = load(cal_path)
        b = cal['benchmark']
        entry = {
            'complexity_class': cls,
            'problem_title': cal['problem']['title'],
            'beta': b['adjustment_factor'],
            'beta_ci95': b.get('adjustment_factor_ci95'),
            'is_reliable': b['is_reliable'],
            'cpp_median_s': b['cpp_median'],
            'python_median_s': b['python_median'],
            'test_case_used': b['test_case_used'],
            'calibration_timestamp': cal['timestamp'],
            'has_slow_solution': os.path.isdir(os.path.join(BASE, cls, 'slow_solutions')),
            'is_overhead_floor': cls in FLOOR_CLASSES,
        }
        sel_path = os.path.join(os.path.dirname(cal_path), 'selectivity.json')
        if os.path.exists(sel_path):
            sel = load(sel_path)
            entry['selectivity'] = {
                'preserved': sel['selectivity_preserved'],
                'python_limit_s': sel['python_limit_s'],
                'cpp_limit_s': sel['cpp_limit_s'],
                'reference_verdict': sel['reference_verdict'],
                'slow_verdict': sel['slow_verdict'],
            }
        else:
            entry['selectivity'] = None
        classes[cls] = entry

    out = {
        '_about': ('Central aggregated results (theoretical axis) for the article and figures. '
                   'Source of truth = complexity_analysis/<class>/results/*.json. '
                   'Regenerate with: python3 aggregate_results.py'),
        'methodology': {
            'engine': ('lib/benchmark_engine.py: startup+compilation excluded, microsecond timer, '
                       'adaptive reps (blocks of 5, cap 35) + IQR, bootstrap CI95 (10000 resamples, seed 42)'),
            'beta_definition': 'median(Python)/median(C++) on the largest test case',
            'adaptive_limit': 'Python limit = beta x 1.0s; C++ limit = 1.0s (traditional)',
            'fast_io': 'all reference C++ use sync_with_stdio(false)+cin.tie(NULL) (symmetric I/O, S3.1)',
            'selectivity': 'slow_solution must stay TLE under the adaptive limit; reference is the AC control',
            'floor_note': ('classes with has_slow_solution=false (O(1), O(log n)) are below the 10:1 '
                           'scale-dominance threshold (S3.2): beta reflects fixed overhead, not algorithmic '
                           'cost; reported as overhead floor / control, not as a calibrated beta'),
        },
        'classes': classes,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w') as f:
        json.dump(out, f, indent=2)
    print(f'Wrote {OUT} with {len(classes)} class(es): {", ".join(classes) or "(none)"}')


if __name__ == '__main__':
    main()
