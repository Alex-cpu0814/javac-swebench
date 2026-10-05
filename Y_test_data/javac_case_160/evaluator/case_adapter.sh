#!/usr/bin/env bash

build_project() {
    mvn -B -o -Prelease-native \
        -pl junixsocket-native-common,junixsocket-native-custom -am clean install \
        -Dmaven.test.skip=true \
        -Djunixsocket.custom.arch=amd64-Linux-clang-jni \
        -Djunixsocket.custom.shaded=default
}

run_project_tests() {
    local control_status target_status
    local report_dir=/testbed/junixsocket-common/target/surefire-reports

    rm -rf "${report_dir}"
    mvn -B -o -f junixsocket-common/pom.xml test \
        '-Dtest=SoTimeoutTest#testSocketTimeoutExceptionRead'
    control_status=$?
    python3 /benchmark/report_surefire.py "${report_dir}"
    if [[ "${control_status}" -ne 0 ]]; then
        return "${control_status}"
    fi

    rm -rf "${report_dir}"
    timeout --signal=TERM --kill-after=5s 15s \
        mvn -B -o -f junixsocket-common/pom.xml test \
        '-Dtest=SoTimeoutTest#testSocketTimeoutExceptionWrite'
    target_status=$?
    if [[ "${target_status}" -eq 124 || "${target_status}" -eq 137 ]]; then
        printf '%s\n' \
            'testSocketTimeoutExceptionWrite (org.newsclub.net.unix.SoTimeoutTest) ... ERROR'
        return 1
    fi
    python3 /benchmark/report_surefire.py "${report_dir}"
    return "${target_status}"
}
