#!/usr/bin/env bash

build_project() {
    python setup.py clean >/dev/null 2>&1 || true
    python setup.py build || return 10

    CASE_NATIVE_LIB="$(find build -type f -name 'jep*.so' -print -quit)"
    [[ -n "${CASE_NATIVE_LIB}" ]] || return 11

    CASE_NATIVE_DIR="$(dirname "${CASE_NATIVE_LIB}")"
    ln -sf "$(basename "${CASE_NATIVE_LIB}")" "${CASE_NATIVE_DIR}/libjep.so"

    CASE_CLASSPATH="build/java/jep.jar"
    [[ -f "${CASE_CLASSPATH}" ]] || return 12

    for jar_file in \
        build/java/jep.test.jar \
        tests/lib/sqlitejdbc-v056.jar \
        tests/lib/fakenetty.jar
    do
        if [[ -f "${jar_file}" ]]; then
            CASE_CLASSPATH="${CASE_CLASSPATH}:${jar_file}"
        fi
    done

    export LD_LIBRARY_PATH="/opt/python-2.7.18/lib:${CASE_NATIVE_DIR}:${LD_LIBRARY_PATH:-}"
    export PYTHONPATH="${PWD}/build/lib.linux-x86_64-2.7:${PWD}:${PYTHONPATH:-}"

    local python_lib
    python_lib="$(find /opt/python-2.7.18/lib -maxdepth 1 -type f \
        -name 'libpython2.7.so*' | head -n 1)"

    if [[ -n "${python_lib}" ]]; then
        export LD_PRELOAD="${python_lib}${LD_PRELOAD:+:${LD_PRELOAD}}"
    fi
}

run_project_tests() {
    java -classpath "${CASE_CLASSPATH}" \
        -Djava.library.path="${CASE_NATIVE_DIR}" \
        jep.Run /benchmark/run_tests_verbose.py
}
