#!/usr/bin/env bash

build_project() {
    cd /testbed
    ./bootstrap
    cd /build
    NOF77=yes /testbed/configure --prefix=/usr/local/mdsplus --disable-java
    make
    make install
}

run_one_tdi_test() {
    local test_name="$1"
    local display_name="$2"
    local status
    local test_dir=/build/tditest/testing

    rm -f "${test_dir}/${test_name}.log" "${test_dir}/${test_name}.trs" "${test_dir}/test-suite.log"
    make -C "${test_dir}" check TESTS="${test_name}.tdi"
    status=$?
    if [[ "${status}" -eq 0 ]]; then
        printf '%s (MDSplus.tditest) ... ok\n' "${display_name}"
    else
        printf '%s (MDSplus.tditest) ... FAIL\n' "${display_name}"
    fi
    return "${status}"
}

run_project_tests() {
    local control_status=0
    local target_status=0

    run_one_tdi_test test-tdishr test-tdishr || control_status=$?
    run_one_tdi_test test-treeshr test-treeshr-owner-id || target_status=$?
    [[ "${control_status}" -eq 0 && "${target_status}" -eq 0 ]]
}

