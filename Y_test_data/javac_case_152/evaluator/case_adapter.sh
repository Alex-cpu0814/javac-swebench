#!/usr/bin/env bash

build_project() {
    mvn -B -o -Prelease-native \
        -pl junixsocket-native-common,junixsocket-native-custom -am clean install \
        -Dmaven.test.skip=true \
        -Djunixsocket.custom.arch=amd64-Linux-clang-jni \
        -Djunixsocket.custom.shaded=default \
        && mvn -B -o -f junixsocket-common/pom.xml package -Dmaven.test.skip=true
}

run_project_tests() {
    local common_jar native_common_jar native_custom_jar class_path
    common_jar="$(find junixsocket-common/target -maxdepth 1 -type f \
        -name 'junixsocket-common-*.jar' ! -name '*-sources.jar' \
        ! -name '*-javadoc.jar' ! -name '*-tests.jar' | head -n 1)"
    native_common_jar="$(find junixsocket-native-common/target -maxdepth 1 -type f \
        -name 'junixsocket-native-common-*.jar' ! -name '*-sources.jar' \
        ! -name '*-javadoc.jar' | head -n 1)"
    native_custom_jar="$(find junixsocket-native-custom/target -maxdepth 1 -type f \
        -name '*default.jar' | head -n 1)"
    class_path="${common_jar}:${native_common_jar}:${native_custom_jar}"

    test -n "${common_jar}" && test -n "${native_common_jar}" \
        && test -n "${native_custom_jar}" || return 2
    rm -rf benchmark-tests/target
    mkdir -p benchmark-tests/target/classes
    javac -cp "${class_path}" -d benchmark-tests/target/classes \
        $(find benchmark-tests/src/test/java -name '*.java') || return $?
    java -cp "${class_path}:benchmark-tests/target/classes" \
        org.newsclub.net.unix.FileDescriptorCastRegressionTest
}
