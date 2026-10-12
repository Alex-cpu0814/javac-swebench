#!/usr/bin/env bash

build_project() {
    command -v clang-14 >/dev/null && command -v python3 >/dev/null && command -v git >/dev/null
}

run_project_tests() {
    local raw="/results/compilation.json"
    python3 /testbed/config/tests/native_compilation.py --root /testbed >"${raw}" 2>/results/compiler-launch.raw.log
    local status=$?
    cat "${raw}"
    # Genuine missing tools, launcher errors and timeouts are infrastructure
    # failures. Changes to production inputs by a candidate are unresolved.
    python3 - "${raw}" "${status}" <<'PY'
import json, sys
try:
    report = json.load(open(sys.argv[1], encoding="utf-8"))
except (ValueError, OSError):
    sys.exit(2)
category = report.get("diagnostic_category")
if category in {"missing_project_compilation_inputs", "compilation_control_failed", "selected_native_regression_failed", "unrelated_compilation_failure"}:
    sys.exit(1)
if report.get("infrastructure_error") or int(sys.argv[2]) not in (0, 1):
    sys.exit(2)
sys.exit(int(sys.argv[2]))
PY
}
