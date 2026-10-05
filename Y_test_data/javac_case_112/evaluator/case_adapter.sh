#!/usr/bin/env bash

readonly OPJ_BUILD_DIR=/opt/openjpeg-build
readonly OPJ_DATA_DIR=/opt/openjpeg-data
readonly OPJ_INPUT="${OPJ_DATA_DIR}/input/nonregression/issue571.tif"
readonly OPJ_OUTPUT=/tmp/issue571.tif.j2k
readonly OPJ_ROUNDTRIP=/tmp/issue571.lossless.tif

build_project() {
    cmake -S /testbed -B "${OPJ_BUILD_DIR}" \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_C_FLAGS=-m32 \
        -DCMAKE_EXE_LINKER_FLAGS=-m32 \
        -DCMAKE_SHARED_LINKER_FLAGS=-m32 \
        -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
        -DBUILD_SHARED_LIBS=OFF \
        -DBUILD_CODEC=ON \
        -DBUILD_THIRDPARTY=ON \
        -DBUILD_TESTING=ON \
        -DOPJ_DATA_ROOT="${OPJ_DATA_DIR}" || return 1
    cmake --build "${OPJ_BUILD_DIR}" --parallel "$(nproc)"
}

run_project_tests() {
    local encode_status=1
    local decode_status=1
    local compare_status=1

    rm -f "${OPJ_OUTPUT}" "${OPJ_ROUNDTRIP}"

    "${OPJ_BUILD_DIR}/bin/opj_compress" -i "${OPJ_INPUT}" -o "${OPJ_OUTPUT}"
    encode_status=$?
    if [[ "${encode_status}" -eq 0 ]]; then
        echo 'encode_issue571 (openjpeg.issue571) ... ok'
        "${OPJ_BUILD_DIR}/bin/opj_decompress" -i "${OPJ_OUTPUT}" -o "${OPJ_ROUNDTRIP}"
        decode_status=$?
    else
        echo 'encode_issue571 (openjpeg.issue571) ... FAIL'
        echo 'decode_issue571 (openjpeg.issue571) ... skipped encode failed'
    fi

    if [[ "${decode_status}" -eq 0 ]]; then
        echo 'decode_issue571 (openjpeg.issue571) ... ok'
        "${OPJ_BUILD_DIR}/bin/compare_images" \
            -b "${OPJ_INPUT}" -t "${OPJ_ROUNDTRIP}" -n 1 -d
        compare_status=$?
    elif [[ "${encode_status}" -eq 0 ]]; then
        echo 'decode_issue571 (openjpeg.issue571) ... FAIL'
    fi

    if [[ "${compare_status}" -eq 0 ]]; then
        echo 'lossless_roundtrip (openjpeg.issue571) ... ok'
    else
        echo 'lossless_roundtrip (openjpeg.issue571) ... FAIL'
    fi
    return "${compare_status}"
}
