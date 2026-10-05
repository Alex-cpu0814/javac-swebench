#!/usr/bin/env bash
set -uo pipefail

readonly BASE_COMMIT="${BENCHMARK_BASE_COMMIT:?BENCHMARK_BASE_COMMIT is required}"
readonly MODEL_PATCH="/inputs/model.patch"
readonly TEST_PATCH="/inputs/test.patch"
readonly CASE_ADAPTER="/benchmark/case_adapter.sh"
readonly RESULT_DIR="/results"
readonly BUILD_LOG="${RESULT_DIR}/project-build.raw.log"
readonly TEST_LOG="${RESULT_DIR}/tests.raw.log"
readonly MODEL_LOG="${RESULT_DIR}/model-patch.raw.log"
readonly TEST_PATCH_LOG="${RESULT_DIR}/test-patch.raw.log"
readonly EVENTS_FILE="${RESULT_DIR}/events.jsonl"
readonly PHASE_FILE="${RESULT_DIR}/phase.json"
readonly RUN_ID="${BENCHMARK_RUN_ID:-unknown-run}"

mkdir -p "${RESULT_DIR}"

utc_now() { date -u +"%Y-%m-%dT%H:%M:%S.%3NZ"; }
emit_event() {
    printf '{"schema_version":"3.0","timestamp":"%s","level":"%s","operation_id":"%s","phase":"%s","event":"%s","message":"%s"}\n' \
        "$(utc_now)" "$1" "${RUN_ID}" "$2" "$3" "$4" >> "${EVENTS_FILE}"
}
write_phase() {
    printf '{\n  "phase": "%s",\n  "outcome": "%s",\n  "reason": "%s",\n  "test_exit_code": %s\n}\n' "$1" "$2" "$3" "${4:-null}" > "${PHASE_FILE}"
}
fail_infrastructure() { emit_event ERROR "$1" "$2" "Evaluation infrastructure failed"; write_phase "$1" infrastructure_error "$2"; exit 2; }
reject_candidate() { emit_event WARN "$1" "$2" "Candidate could not complete this phase"; write_phase "$1" unresolved "$2"; exit 1; }

[[ -f "${MODEL_PATCH}" ]] || fail_infrastructure preflight model_patch_missing
[[ -f "${TEST_PATCH}" ]] || fail_infrastructure preflight test_patch_missing
[[ -f "${CASE_ADAPTER}" ]] || fail_infrastructure preflight case_adapter_missing
source "${CASE_ADAPTER}" || fail_infrastructure preflight case_adapter_load_failed
declare -F build_project >/dev/null || fail_infrastructure preflight build_function_missing
declare -F run_project_tests >/dev/null || fail_infrastructure preflight test_function_missing

cd /testbed || fail_infrastructure workspace testbed_missing
git reset --hard "${BASE_COMMIT}" >/dev/null 2>&1 || fail_infrastructure workspace base_reset_failed
git clean -fdx -e bin >/dev/null 2>&1 || fail_infrastructure workspace base_clean_failed
[[ "$(git rev-parse HEAD)" == "${BASE_COMMIT}" ]] || fail_infrastructure workspace base_commit_mismatch

sed 's/\r$//' "${MODEL_PATCH}" > /tmp/model.patch
sed 's/\r$//' "${TEST_PATCH}" > /tmp/test.patch
git apply --check --whitespace=nowarn /tmp/test.patch >"${TEST_PATCH_LOG}" 2>&1 || fail_infrastructure preflight protected_test_patch_invalid

emit_event INFO model_patch model_patch_started "Applying candidate patch"
git apply --check --whitespace=nowarn /tmp/model.patch >"${MODEL_LOG}" 2>&1 || reject_candidate model_patch model_patch_apply_failed
git apply --whitespace=nowarn /tmp/model.patch >>"${MODEL_LOG}" 2>&1 || reject_candidate model_patch model_patch_apply_failed

emit_event INFO test_patch test_patch_started "Applying protected test patch"
git apply --check --whitespace=nowarn /tmp/test.patch >>"${TEST_PATCH_LOG}" 2>&1 || reject_candidate test_patch candidate_conflicts_with_test_patch
git apply --whitespace=nowarn /tmp/test.patch >>"${TEST_PATCH_LOG}" 2>&1 || reject_candidate test_patch candidate_conflicts_with_test_patch

emit_event INFO project_build project_build_started "Building LWJGL core"
if ! build_project >"${BUILD_LOG}" 2>&1; then
    reject_candidate project_build project_build_failed
fi

emit_event INFO tests tests_started "Running official MemoryUtilTest"
set +e
run_project_tests >"${TEST_LOG}" 2>&1
test_exit_code=$?
set -e
emit_event INFO tests tests_completed "Official MemoryUtilTest completed"
write_phase tests_complete completed tests_completed "${test_exit_code}"
[[ "${test_exit_code}" -eq 0 ]] && exit 0
exit 1
@@
-git clean -fdx -e bin >/dev/null 2>&1 || fail_infrastructure workspace base_clean_failed
+git clean -fdx >/dev/null 2>&1 || fail_infrastructure workspace base_clean_failed
@@
-emit_event INFO project_build project_build_started "Building LWJGL core"
+emit_event INFO project_build project_build_started "Building OpenJPEG for 32-bit x86"
@@
-emit_event INFO tests tests_started "Running official MemoryUtilTest"
+emit_event INFO tests tests_started "Running official issue571 lossless round-trip regression"
@@
-emit_event INFO tests tests_completed "Official MemoryUtilTest completed"
+emit_event INFO tests tests_completed "Official issue571 regression completed"
