#!/usr/bin/env bash

build_project() {
    mvn -B -o -Puse-snapshots,release-native \
        -pl junixsocket-native-custom -am clean install \
        -DskipTests \
        -Djunixsocket.custom.arch=amd64-Linux-clang-jni \
        -Djunixsocket.custom.shaded=default
}

run_project_tests() {
    local status
    mvn -B -o -Puse-snapshots -pl junixsocket-common -am test \
        '-Dtest=AbstractNamespaceTest,AFUNIXSocketAddressTest#testAbstractNamespace' \
        -Dsurefire.failIfNoSpecifiedTests=false
    status=$?
    python3 /benchmark/report_surefire.py \
        /testbed/junixsocket-common/target/surefire-reports
    return "${status}"
}
