#!/usr/bin/env python3
"""
Shared benchmark engine.

This module is the SINGLE SOURCE of the measurement methodology validated on
the theoretical pipeline (complexity_analysis / On2_quadratic, project items
3-6) and reused, unchanged, by the real-world pipeline. It is problem-agnostic
and database-agnostic: every function works on plain strings (source code,
input, expected output), so the same engine drives both the DB-backed
complexity runner and the file-backed real-world runners.

Methodology (artigo Sec. 3.2/3.8), identical across pipelines via AppConfig:
  - canonical Docker images, memory, cpus and C++ flags (-O2);
  - C++ compiled ONCE, outside the timing; container started ONCE;
  - each repetition times only the ready binary/script with `/usr/bin/time -f
    %e` inside the container (startup/compilation excluded, no subtraction);
  - adaptive repetition in blocks with a per-language IQR/median stop;
  - beta (median ratio) 95% CI by bootstrap with a fixed seed.
"""
import os
import sys
import random
import subprocess
import tempfile
import statistics

# Make the application package importable so the canonical AppConfig (the one
# shared by every pipeline) is the single source of execution parameters.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from config.app import AppConfig


def _docker_start(image: str, temp_dir: str) -> str:
    """Start ONE long-lived container (untimed). Returns the container id."""
    result = subprocess.run(
        [
            'docker', 'run', '-d', '--rm',
            '-v', f'{temp_dir}:/workspace',
            '--workdir', '/workspace',
            '--memory', AppConfig.DOCKER_MEMORY_LIMIT,
            '--cpus', AppConfig.DOCKER_CPUS,
            image, 'sleep', '3600'
        ],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to start container: {result.stderr.strip()}")
    return result.stdout.strip()


def _docker_exec(container_id: str, shell_cmd: str, timeout: float):
    """Run a command in the already-running container via `docker exec`."""
    return subprocess.run(
        ['docker', 'exec', container_id, 'bash', '-c', shell_cmd],
        capture_output=True, text=True, timeout=timeout
    )


def _docker_stop(container_id: str):
    subprocess.run(['docker', 'kill', container_id], capture_output=True, text=True)


# Stack limit (KB) for the in-container runs. The default container stack (~8MB)
# overflows on deep recursion (e.g. recursion depth ~10^6 in DP/recursive
# solutions). CSES runs with a large stack, so we match it to faithfully
# reproduce its verdicts and to stay CONSISTENT with the Python solutions'
# sys.setrecursionlimit. 256 MB, well within the 512m memory limit.
_STACK_LIMIT_KB = 262144


def _wrap_timed(inner_cmd: str) -> str:
    """
    Wrap a command with a high-resolution wall-clock timer (GNU `date +%s.%N`,
    nanosecond field, ~microsecond real resolution) executed INSIDE the warm
    container. Replaces `/usr/bin/time -f %e`, whose 0.01s (centisecond)
    resolution quantizes sub-0.1s runs (e.g. C++ at ~0.02s) into a useless 2-3
    tick measurement.

    Same measurement semantics as item 4: the timer brackets the ready
    binary/script run only (container already up, C++ already compiled); the
    process's own stdout is preserved on stdout (used for verdict correctness),
    its stderr is discarded, and the T_START/T_END markers go to stderr. The
    wrapper exits with the wrapped command's status (so a judge `timeout` still
    surfaces as exit 124).
    """
    return (f"ulimit -s {_STACK_LIMIT_KB} 2>/dev/null; "
            f"START=$(date +%s.%N); {inner_cmd} 2>/dev/null; EC=$?; "
            f"END=$(date +%s.%N); echo \"T_START=$START\" >&2; "
            f"echo \"T_END=$END\" >&2; exit $EC")


def _parse_elapsed(stderr: str):
    """Recover the elapsed seconds (float) from the T_START/T_END markers."""
    start = end = None
    for line in stderr.splitlines():
        line = line.strip()
        if line.startswith('T_START='):
            try:
                start = float(line[len('T_START='):])
            except ValueError:
                return None
        elif line.startswith('T_END='):
            try:
                end = float(line[len('T_END='):])
            except ValueError:
                return None
    if start is None or end is None:
        return None
    return end - start


def _iqr(times):
    """Interquartile range (Q3 - Q1)."""
    if len(times) < 2:
        return 0.0
    q = statistics.quantiles(times, n=4)
    return q[2] - q[0]


def bootstrap_beta_ci(cpp_times, python_times, n_resamples, seed, ci=0.95):
    """
    95% confidence interval for beta = median(python)/median(cpp) by bootstrap.

    beta is a ratio of medians, which has no closed-form CI (Efron 1979), so we
    resample each language's measured times WITH REPLACEMENT (same n as the
    original sample), recompute the median ratio for each resample, and take the
    empirical percentiles. The RNG seed is fixed for reproducibility.

    Returns (ci_low, ci_high, n_used).
    """
    rng = random.Random(seed)
    n_c, n_p = len(cpp_times), len(python_times)
    betas = []
    for _ in range(n_resamples):
        rc = [rng.choice(cpp_times) for _ in range(n_c)]
        rp = [rng.choice(python_times) for _ in range(n_p)]
        mc = statistics.median(rc)
        if mc > 0:
            betas.append(statistics.median(rp) / mc)
    betas.sort()
    alpha = (1.0 - ci) / 2.0
    lo_idx = int(alpha * len(betas))
    hi_idx = min(int((1.0 - alpha) * len(betas)), len(betas) - 1)
    return betas[lo_idx], betas[hi_idx], len(betas)


def select_largest_test_case(cases, size_fn, id_fn=lambda c: 0):
    """
    Select the largest test case by input size in BYTES (project item 7,
    option 1). Ties are broken deterministically by the smaller case id/name,
    so the choice is reproducible and identical across pipelines.

    `cases`   : iterable of test cases (DB rows, file tuples, ...).
    `size_fn` : case -> input size in bytes.
    `id_fn`   : case -> numeric/comparable id used only for tie-breaking.
    """
    return max(cases, key=lambda c: (size_fn(c), -id_fn(c)))


def measure_language(source_code: str, input_data: str, expected_output: str,
                     language: str, iqr_threshold: float, time_limit: float = 60.0,
                     validate_fn=None):
    """
    Measure pure execution time with ADAPTIVE repetition (artigo Sec. 3.2).

    Measurement method (validated, item 4 - mirrors a real judge):
      - the container is started ONCE (startup excluded from timing);
      - C++ is compiled ONCE, outside any measurement;
      - one warm-up run validates correctness (untimed);
      - each timed repetition runs the ready binary/script and the wall time
        is taken by a high-resolution `date +%%s.%%N` bracket INSIDE the
        container (see _wrap_timed), so neither docker setup, compilation nor
        container startup enter the measured time. No overhead subtraction is
        used.

    Adaptive stopping:
      - timed runs are added in blocks of BENCHMARK_BLOCK_SIZE;
      - from BENCHMARK_MIN_REPETITIONS on, after each block the dispersion
        (IQR/median) is recomputed and the loop stops when it drops below
        `iqr_threshold` (per-language) or at BENCHMARK_MAX_REPETITIONS (cap).

    `validate_fn` (optional): callable(expected, actual) -> bool used for the
    warm-up correctness check. Defaults to exact string equality, which keeps
    the theoretical pipeline unchanged; problems with multiple valid outputs
    (e.g. cycle finding) pass their own validator.

    Returns a dict: times, median, iqr, iqr_ratio, n_reps, converged,
    hit_cap, threshold.
    """
    if language == 'cpp':
        image = AppConfig.DOCKER_CPP_IMAGE
        source_name = 'solution.cpp'
        run_cmd = './solution'
    else:
        image = AppConfig.DOCKER_PYTHON_IMAGE
        source_name = 'solution.py'
        run_cmd = 'python3 solution.py'

    min_reps = AppConfig.BENCHMARK_MIN_REPETITIONS
    block = AppConfig.BENCHMARK_BLOCK_SIZE
    cap = AppConfig.BENCHMARK_MAX_REPETITIONS

    with tempfile.TemporaryDirectory() as temp_dir:
        with open(os.path.join(temp_dir, source_name), 'w') as f:
            f.write(source_code)
        with open(os.path.join(temp_dir, 'input.txt'), 'w') as f:
            f.write(input_data)

        container_id = _docker_start(image, temp_dir)
        try:
            # Compilation: ONCE, outside the timing.
            if language == 'cpp':
                comp = _docker_exec(
                    container_id,
                    f'g++ {AppConfig.CPP_COMPILE_FLAGS} -o solution solution.cpp',
                    timeout=120
                )
                if comp.returncode != 0:
                    raise RuntimeError(f"C++ compilation failed: {comp.stderr.strip()}")

            # Warm-up + correctness (untimed).
            warm = _docker_exec(container_id, f'{run_cmd} < input.txt', timeout=time_limit)
            if warm.returncode != 0:
                raise RuntimeError(f"{language} warm-up run failed: {warm.stderr.strip()}")
            actual = warm.stdout.strip()
            expected = expected_output.strip()
            correct = validate_fn(expected, actual) if validate_fn else (actual == expected)
            if not correct:
                raise ValueError(
                    f"{language} output mismatch: got '{actual[:80]}', "
                    f"expected '{expected[:80]}'"
                )

            # Timed runs in adaptive blocks. Only the ready binary/script is timed.
            times = []
            failures = 0
            converged = False
            while len(times) < cap:
                target = min(len(times) + block, cap)
                while len(times) < target:
                    r = _docker_exec(
                        container_id,
                        _wrap_timed(f"{run_cmd} < input.txt"),
                        timeout=time_limit
                    )
                    if r.returncode != 0:
                        failures += 1
                        print(f"   Run {len(times)+1}: FAILED - {r.stderr.strip()[:120]}")
                    else:
                        t = _parse_elapsed(r.stderr)
                        if t is not None:
                            times.append(t)
                            print(f"   Run {len(times)}: {t:.4f}s")
                        else:
                            failures += 1
                            print(f"   Run {len(times)+1}: could not parse time from '{r.stderr.strip()[:120]}'")
                    if failures > cap:
                        raise RuntimeError(f"Too many failed runs for {language} ({failures})")

                # Evaluate dispersion after the block (once we have the minimum).
                if len(times) >= min_reps:
                    m = statistics.median(times)
                    ratio = (_iqr(times) / m) if m else float('inf')
                    print(f"   [block @ {len(times)} reps] median={m:.4f}s "
                          f"IQR/median={ratio*100:.1f}% (threshold {iqr_threshold*100:.0f}%)")
                    if ratio < iqr_threshold:
                        converged = True
                        break

            median = statistics.median(times)
            iqr = _iqr(times)
            ratio = (iqr / median) if median else float('inf')
            return {
                'times': times,
                'median': median,
                'iqr': iqr,
                'iqr_ratio': ratio,
                'n_reps': len(times),
                'converged': converged,
                'hit_cap': not converged,
                'threshold': iqr_threshold,
            }
        finally:
            _docker_stop(container_id)


def run_timed_trials(source_code: str, input_data: str, expected_output: str,
                     language: str, n_trials: int, time_limit: float,
                     validate_fn=None):
    """
    Run `n_trials` verdict trials in the canonical environment (same as
    `measure_language`: container started ONCE, C++ compiled ONCE, execution
    timed by `/usr/bin/time -f %%e` inside). Each trial is wrapped in the
    judge's `timeout <time_limit>s`, mirroring a real online judge.

    Per-trial verdict:
      - TLE            if the judge timeout killed the run (exit 124);
      - RUNTIME_ERROR  on any other non-zero exit;
      - WRONG_ANSWER   if the output fails `validate_fn` (default exact match);
      - ACCEPTED       otherwise.
    A compilation failure yields a COMPILATION_ERROR trial for every trial.

    Returns a list of dicts: {'status', 'execution_time'}.
    """
    if language == 'cpp':
        image = AppConfig.DOCKER_CPP_IMAGE
        source_name = 'solution.cpp'
        run_cmd = './solution'
    else:
        image = AppConfig.DOCKER_PYTHON_IMAGE
        source_name = 'solution.py'
        run_cmd = 'python3 solution.py'

    trials = []
    with tempfile.TemporaryDirectory() as temp_dir:
        with open(os.path.join(temp_dir, source_name), 'w') as f:
            f.write(source_code)
        with open(os.path.join(temp_dir, 'input.txt'), 'w') as f:
            f.write(input_data)

        container_id = _docker_start(image, temp_dir)
        try:
            if language == 'cpp':
                comp = _docker_exec(
                    container_id,
                    f'g++ {AppConfig.CPP_COMPILE_FLAGS} -o solution solution.cpp',
                    timeout=120
                )
                if comp.returncode != 0:
                    return [{'status': 'COMPILATION_ERROR', 'execution_time': 0.0}
                            for _ in range(n_trials)]

            expected = expected_output.strip()
            for _ in range(n_trials):
                r = _docker_exec(
                    container_id,
                    _wrap_timed(f"timeout {time_limit}s {run_cmd} < input.txt"),
                    timeout=time_limit + 15
                )
                if r.returncode == 124:
                    trials.append({'status': 'TLE', 'execution_time': time_limit})
                    continue
                if r.returncode != 0:
                    trials.append({'status': 'RUNTIME_ERROR', 'execution_time': 0.0})
                    continue
                t = _parse_elapsed(r.stderr)
                actual = r.stdout.strip()
                correct = validate_fn(expected, actual) if validate_fn else (actual == expected)
                trials.append({
                    'status': 'ACCEPTED' if correct else 'WRONG_ANSWER',
                    'execution_time': t if t is not None else 0.0,
                })
        finally:
            _docker_stop(container_id)
    return trials


def compute_beta(cpp, py, test_case_used):
    """
    Assemble the beta result dict from the two per-language measurement dicts
    returned by `measure_language`. beta = median(python)/median(cpp); its 95%
    CI comes from `bootstrap_beta_ci`. The returned schema is the canonical one
    consumed by both pipelines' JSON output.
    """
    adjustment_factor = py['median'] / cpp['median'] if cpp['median'] > 0 else float('nan')
    # Reliable only if BOTH languages reached the stability criterion (not the cap).
    is_reliable = cpp['converged'] and py['converged']

    # 95% CI for beta via bootstrap (ratio of medians has no closed-form CI).
    ci_low, ci_high, n_boot = bootstrap_beta_ci(
        cpp['times'], py['times'],
        AppConfig.BENCHMARK_BOOTSTRAP_RESAMPLES,
        AppConfig.BENCHMARK_BOOTSTRAP_SEED
    )
    print(f"   beta = {adjustment_factor:.3f}  95% CI [{ci_low:.3f}, {ci_high:.3f}]  "
          f"(bootstrap, {n_boot} resamples, seed {AppConfig.BENCHMARK_BOOTSTRAP_SEED})")

    return {
        'cpp_median': cpp['median'],
        'python_median': py['median'],
        'cpp_iqr': cpp['iqr'],
        'python_iqr': py['iqr'],
        'adjustment_factor': adjustment_factor,
        'adjustment_factor_ci95': [ci_low, ci_high],
        'bootstrap': {
            'method': 'percentile bootstrap on ratio of medians (resample times with replacement)',
            'n_resamples': n_boot,
            'seed': AppConfig.BENCHMARK_BOOTSTRAP_SEED,
        },
        'is_reliable': is_reliable,
        'cpp_times': cpp['times'],
        'python_times': py['times'],
        'repetitions': cpp['n_reps'],
        'test_case_used': test_case_used,
        'adaptive': {
            'cpp': {
                'n_reps': cpp['n_reps'], 'iqr_ratio': cpp['iqr_ratio'],
                'converged': cpp['converged'], 'hit_cap': cpp['hit_cap'],
                'threshold': cpp['threshold'],
            },
            'python': {
                'n_reps': py['n_reps'], 'iqr_ratio': py['iqr_ratio'],
                'converged': py['converged'], 'hit_cap': py['hit_cap'],
                'threshold': py['threshold'],
            },
        },
        'method': {
            'block_size': AppConfig.BENCHMARK_BLOCK_SIZE,
            'min_repetitions': AppConfig.BENCHMARK_MIN_REPETITIONS,
            'max_repetitions': AppConfig.BENCHMARK_MAX_REPETITIONS,
            'timer': 'date +%s.%N wall delta (in-container, execution only, microsecond resolution)',
            'cpp_compile_flags': AppConfig.CPP_COMPILE_FLAGS,
            'memory_limit': AppConfig.DOCKER_MEMORY_LIMIT,
            'cpus': AppConfig.DOCKER_CPUS,
            'cpp_image': AppConfig.DOCKER_CPP_IMAGE,
            'python_image': AppConfig.DOCKER_PYTHON_IMAGE,
        },
    }
