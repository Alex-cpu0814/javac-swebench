#!/usr/bin/env bash
build_project() {
    command -v python3 >/dev/null && command -v git >/dev/null && command -v ant >/dev/null && command -v gcc >/dev/null && command -v java >/dev/null && command -v javac >/dev/null || return 2
    python3 /benchmark/build_project.py /testbed
}
run_project_tests() {
    python3 /benchmark/test_runner.py /testbed /results > /results/runner.stdout.log 2>/results/runner.stderr.log
    local status=$?
    cat /results/runner.stdout.log
    return "$status"
}
