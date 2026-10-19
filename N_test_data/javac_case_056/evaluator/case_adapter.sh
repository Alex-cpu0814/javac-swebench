#!/usr/bin/env bash

build_project() {
    command -v python3 >/dev/null && command -v git >/dev/null && command -v ant >/dev/null && command -v gcc >/dev/null && command -v java >/dev/null && command -v javac >/dev/null || return 2
    python3 /benchmark/build_project.py /testbed --offline
}

run_project_tests() {
    python3 /benchmark/test_runner.py /testbed /results > /results/runner.stdout.log 2>/results/runner.stderr.log
    local status=$?
    python3 - "${status}" <<'PY'
import json
import pathlib
import sys

root = pathlib.Path('/results')
path = root / 'sanitized_results.json'
if path.is_file():
    report = json.loads(path.read_text(encoding='utf-8'))
    mapping = {'PASS': 'passed', 'FAIL': 'failed', 'SKIP': 'skipped'}
    tests = {name: {'status': mapping.get(item['status'], 'error')} for name, item in report['nodes'].items()}
    print(json.dumps({'oracle_type': 'runtime_behavior', 'phase': report['phase'], 'collected': report['collected'], 'infrastructure_error': report['infrastructure_error'], 'tests': tests}))
else:
    lines = (root / 'runner.stdout.log').read_text(encoding='utf-8', errors='replace').splitlines()
    report = {}
    for line in lines:
        try:
            report = json.loads(line)
        except ValueError:
            continue
    print(json.dumps({'oracle_type': 'runtime_behavior', 'tests': {}, 'diagnostic': report}))

code = int(sys.argv[1])
if code == 2:
    # Tools were checked before the current build. A candidate that breaks
    # compilation, library inputs, loading or test collection is unresolved.
    # Timeouts and failures outside the known execution phases remain infra.
    phase = report.get('phase')
    if phase in {'fixture_compilation', 'test_compilation', 'dynamic_loading', 'collection', 'call'} and report.get('category') != 'timeout':
        sys.exit(1)
    sys.exit(2)
sys.exit(code if code in (0, 1) else 2)
PY
}
