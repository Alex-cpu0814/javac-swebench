#!/usr/bin/env bash

build_project() {
    mvn -B -o -Prelease-native \
        -pl junixsocket-native-common,junixsocket-native-custom -am clean install \
        -Dmaven.test.skip=true \
        '-Djunixsocket.native.clang.c.options=-Wall -Wextra -Wno-reserved-id-macro -Wno-undef -Wno-cast-qual -Wno-disabled-macro-expansion -Wno-language-extension-token -Wno-gnu-auto-type -Wno-c++11-extensions -Wno-c++98-compat -Wno-empty-translation-unit -Wno-gnu-empty-initializer -Werror-implicit-function-declaration -Wint-conversion -Wno-unused-command-line-argument -fno-strict-overflow -finline-functions -fwrapv -fPIC -fvisibility=hidden -fno-common -Os -std=gnu11 -Djunixsocket_use_poll_for_read' \
        -Djunixsocket.custom.arch=amd64-Linux-clang-jni \
        -Djunixsocket.custom.shaded=default
}

run_project_tests() {
    local control_status target_status
    local report_dir=/testbed/junixsocket-common/target/surefire-reports

    rm -rf "${report_dir}"
    mvn -B -o -f junixsocket-common/pom.xml test \
        '-Dtest=SoTimeoutTest#issue14Pass'
    control_status=$?
    python3 /benchmark/report_surefire.py "${report_dir}"
    if [[ "${control_status}" -ne 0 ]]; then
        return "${control_status}"
    fi

    rm -rf "${report_dir}"
    timeout --signal=TERM --kill-after=5s 30s \
        mvn -B -o -f junixsocket-common/pom.xml test \
        '-Dtest=SoTimeoutTest#testSocketTimeoutException'
    target_status=$?
    if [[ "${target_status}" -eq 124 || "${target_status}" -eq 137 ]]; then
        printf '%s\n' \
            'testSocketTimeoutException (org.newsclub.net.unix.SoTimeoutTest) ... ERROR'
        return 1
    fi
    python3 /benchmark/report_surefire.py "${report_dir}"
    return "${target_status}"
}
