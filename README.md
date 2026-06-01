
# Adaptive Code Judge: Fair Evaluation between C++ and Python

Research artifact for an **Adaptive Code Judge** that replaces the fixed time limit of
online judges (and the fixed 2x-3x multipliers) with a per-language, per-problem
calibration factor (**beta**) measured from controlled benchmarks in Docker containers.

> Anonymized for double-blind review. Author and affiliation are omitted here and added
> in the camera-ready version.

## Problem and research questions

Online judges set a single time limit calibrated on optimized C++. Applied to teaching,
this penalizes correct solutions in interpreted languages (Python) with Time Limit
Exceeded (TLE) verdicts that reflect the execution model, not an incorrect algorithm.

- **RQ1**: Do fixed multipliers (2x-3x over C++) capture the C++/Python execution gap
  across complexity classes?
- **RQ2**: Does adaptive calibration (empirical beta) reduce unfair TLE on correct Python
  solutions **without** losing selectivity against inefficient solutions?
- **RQ3**: Is beta a per-language constant, or does it vary with the nature of the problem
  (deep recursion, dynamic programming, graphs, I/O)?

## Method (summary)

- **beta = median(Python) / median(C++)** on the largest test case (where TLE is decided).
- **Adaptive limit**: `limit_Python = beta x 1.0s`; `limit_C++ = 1.0s` (C++ is the ruler,
  `beta_cpp = 1`). The model only grants the Python solution time proportional to the
  measured disadvantage; it never tightens C++.
- **Engine** (`experiments/lib/benchmark_engine.py`): compilation and process startup are
  excluded from timing; microsecond timer; adaptive repetition (blocks of 5, cap 35) with
  IQR stability (<15% C++, <20% Python); 95% CI by bootstrap (10000 resamples, seed 42).
- **Symmetric I/O (fast-IO)**: all reference C++ use `sync_with_stdio(false)+cin.tie(NULL)`.
- **CSES-first**: the official judge (CSES) decides whether an injustice is real; the local
  pipeline measures beta and proposes the adaptive limit (it is hardware-dependent and is
  not the source of the injustice verdict).
- **Selectivity**: a deliberately inefficient solution must still TLE under the adaptive
  limit; the reference solution is the accepted control.

## Two experimental axes

- **Theoretical** (`experiments/`): 6 synthetic complexity classes — O(1), O(log n), O(n),
  O(n^2), O(n^3), O(2^n).
- **Real-world** (`experiments_realworld/`): 11 CSES problems across 4 categories —
  graphs (3), dynamic programming (3), backtracking (2), recursion (3).

## Headline results

beta is **not** a per-language constant; it spans a wide range and tracks the nature of the
problem, so no fixed 2x-3x multiplier fits.

- Real-world beta range: ~3.07 (memory-bound, Planets Queries) to ~120 (compute-bound,
  Floyd-Warshall). DP problems are calibrated by the slower correct style (the larger beta).
- Theoretical spectrum: O(n) 3.87 < O(n^2) 4.48 < O(2^n) 33.84 < O(n^3) 77.22; O(1) and
  O(log n) sit at an overhead floor (work too small to calibrate beta — reported as control).

Consolidated numbers and the per-problem evidence live in **`results/`** (see below).

## Repository structure

```
.
├── results/                     # Consolidated results (single place)
│   ├── theoretical_summary.json   # theoretical axis: 6 classes (beta + CI95 + selectivity)
│   ├── theoretical_validation.md  # theoretical validation log
│   ├── realworld_summary.json     # real-world axis: 11 problems (beta + CI95 + verdicts)
│   └── realworld_validation.md    # real-world validation log (CSES submissions, cross-checks)
├── experiments/                 # Theoretical axis (synthetic complexity classes)
│   ├── lib/benchmark_engine.py    # measurement engine (source of the paper's numbers)
│   ├── run_experiment_direct.py   # runner (calibration + selectivity)
│   ├── aggregate_results.py       # aggregates per-class JSONs -> results/theoretical_summary.json
│   └── complexity_analysis/<class>/{problem_definition.py, reference_solutions/,
│                                     slow_solutions/, FORMAL_PROOF.md, results/}
├── experiments_realworld/       # Real-world axis (CSES problems)
│   └── <category>/<problem>/{README.md, formal_proof.md, implementations/, test_data/,
│                             benchmarking/, results/}
├── docker/                      # Pinned execution environment (Dockerfiles + run scripts)
│   └── ENVIRONMENT.md             # exact toolchain/versions used in all runs
├── figuras/                     # All figures
│   ├── paper_figures/             # Figure generators + original figures
│   └── paper_figures_regeneradas/ # Regenerated figures (plotnine) + reading guide/captions
├── src/                         # Adaptive Code Judge MVP (Flask service)
│   ├── api/  models/  services/  executor/  config/  main.py
├── scripts/init_db.py           # MVP database bootstrap
├── requirements.txt             # MVP dependencies (Flask service)
├── start_server.py  run.sh      # MVP launchers
└── data/                        # MVP runtime DB location (created on demand; gitignored)
```

### Note on `src/` (the MVP) vs the validated pipeline

`src/` is the **architectural MVP** of the judge (the system described in the paper):
REST API, Docker execution engine, data model, calibration/judging services. **The paper's
measured numbers come from the experiments pipeline** (`experiments/lib` + the per-problem
benchmarking under `experiments_realworld/`), not from the MVP service. The MVP's calibration
is a simplified version of the full protocol; treat `src/` as the architecture, and
`experiments*/` + `results/` as the validated measurements.

## Environment (reproducibility)

All experiments ran in pinned Docker images (verified inside the images):

- C++: `gcc:16.1.0` → g++ (GCC) 16.1.0
- Python: `python:3.11.15-slim` → Python 3.11.15
- Debian GLIBC 2.41 (Debian 13), arm64; Docker Desktop on macOS host
- Flags: `-O2`; memory `512m`; CPUs `1.0`; bootstrap seed `42`

See `docker/ENVIRONMENT.md` for image ids and full details.

## Reproducing

```bash
# 1. Build the pinned images (from repo root)
docker build -f docker/Dockerfile.cpp    -t adaptive-judge-cpp:latest .
docker build -f docker/Dockerfile.python -t adaptive-judge-python:latest .

# 2. Theoretical axis (one class at a time), then aggregate
cd experiments
python3 run_experiment_direct.py On_linear     # O1_constant, O_log_n, On2_quadratic, On3_cubic, O2n_exponential
python3 aggregate_results.py                    # -> ../results/theoretical_summary.json

# 3. Real-world axis (per problem)
python3 experiments_realworld/<category>/<problem>/benchmarking/run_benchmark.py

# 4. Figures (need: matplotlib, plotnine, pandas, numpy, scipy)
python3 figuras/paper_figures/make_figures.py
python3 figuras/paper_figures_regeneradas/make_fig1_plotnine.py   # fig2/fig3 likewise
```

Dependency note: `requirements.txt` covers the **MVP service** (Flask/SQLAlchemy/docker). The
analysis/figure scripts additionally require `matplotlib`, `plotnine`, `pandas`, `numpy`,
`scipy`.

## Running the MVP service (optional)

```bash
pip install -r requirements.txt
python3 scripts/init_db.py        # bootstrap the database
python3 start_server.py           # or: ./run.sh server
curl http://localhost:8000/health
```

## License

Academic research use.
