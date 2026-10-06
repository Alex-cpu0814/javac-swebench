#!/usr/bin/env bash
set -uo pipefail

readonly BASE_COMMIT="${BENCHMARK_BASE_COMMIT:?BENCHMARK_BASE_COMMIT is required}"
readonly MODEL_PATCH=/inputs/model.patch
readonly TEST_PATCH=/inputs/test.patch
readonly RESULT_DIR=/results
readonly BUILD_LOG="${RESULT_DIR}/project-build.raw.log"
readonly TEST_LOG="${RESULT_DIR}/tests.raw.log"
readonly MODEL_LOG="${RESULT_DIR}/model-patch.raw.log"
readonly TEST_PATCH_LOG="${RESULT_DIR}/test-patch.raw.log"

mkdir -p "${RESULT_DIR}"

write_phase() {
    printf '{"phase":"%s","outcome":"%s","reason":"%s","test_exit_code":%s}\n' \
        "$1" "$2" "$3" "${4:-null}" > "${RESULT_DIR}/phase.json"
}
infrastructure_error() { write_phase "$1" infrastructure_error "$2" null; exit 2; }
unresolved() { write_phase "$1" unresolved "$2" null; exit 1; }

[[ -f "${MODEL_PATCH}" ]] || infrastructure_error preflight model_patch_missing
[[ -f "${TEST_PATCH}" ]] || infrastructure_error preflight test_patch_missing
[[ -f /benchmark/case_adapter.sh ]] || infrastructure_error preflight adapter_missing
source /benchmark/case_adapter.sh || infrastructure_error preflight adapter_load_failed

cd /testbed || infrastructure_error workspace testbed_missing
git reset --hard "${BASE_COMMIT}" >/dev/null 2>&1 || infrastructure_error workspace base_reset_failed
git clean -fdx >/dev/null 2>&1 || infrastructure_error workspace base_clean_failed
sed 's/\r$//' "${MODEL_PATCH}" > /tmp/model.patch
sed 's/\r$//' "${TEST_PATCH}" > /tmp/test.patch
git apply --check --whitespace=nowarn /tmp/test.patch >"${TEST_PATCH_LOG}" 2>&1 \
    || infrastructure_error preflight protected_test_patch_invalid
git apply --check --whitespace=nowarn /tmp/model.patch >"${MODEL_LOG}" 2>&1 \
    || unresolved model_patch model_patch_apply_failed
git apply --whitespace=nowarn /tmp/model.patch >>"${MODEL_LOG}" 2>&1 \
    || unresolved model_patch model_patch_apply_failed
git apply --check --whitespace=nowarn /tmp/test.patch >>"${TEST_PATCH_LOG}" 2>&1 \
    || unresolved test_patch candidate_conflicts_with_test_patch
git apply --whitespace=nowarn /tmp/test.patch >>"${TEST_PATCH_LOG}" 2>&1 \
    || unresolved test_patch candidate_conflicts_with_test_patch

build_project >"${BUILD_LOG}" 2>&1 || unresolved project_build project_build_failed
set +e
run_project_tests >"${TEST_LOG}" 2>&1
status=$?
set -e
write_phase tests_complete completed tests_completed "${status}"
exit "${status}"
