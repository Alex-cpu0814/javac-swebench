#!/usr/bin/env bash

build_project() {
    local flags=(
        -Dbinding.assimp=false -Dbinding.bgfx=false -Dbinding.egl=false
        -Dbinding.glfw=false -Dbinding.jawt=false -Dbinding.jemalloc=false
        -Dbinding.lmdb=false -Dbinding.lz4=false -Dbinding.nanovg=false
        -Dbinding.nfd=false -Dbinding.nuklear=false -Dbinding.odbc=false
        -Dbinding.openal=false -Dbinding.opencl=false -Dbinding.opengl=false
        -Dbinding.opengles=false -Dbinding.openvr=false -Dbinding.par=false
        -Dbinding.remotery=false -Dbinding.rpmalloc=false -Dbinding.sse=false
        -Dbinding.stb=false -Dbinding.tinyexr=false -Dbinding.tinyfd=false
        -Dbinding.tootle=false -Dbinding.vma=false -Dbinding.vulkan=false
        -Dbinding.xxhash=false -Dbinding.yoga=false -Dbinding.zstd=false
    )
    if ! C_INCLUDE_PATH=/testbed/modules/lwjgl/core/src/main/c/dyncall \
        ant -Dbuild.offline=true "${flags[@]}" compile-templates compile; then
        return 1
    fi

    mkdir -p bin/classes/test
    javac -cp "bin/classes/lwjgl/core:bin/libs/java/jsr305.jar:bin/libs/java/testng.jar" \
        -d bin/classes/test \
        modules/lwjgl/core/src/test/java/org/lwjgl/system/MemoryUtilTest.java || return 1
}

run_project_tests() {
    local cp="bin/classes/lwjgl/core:bin/classes/test:bin/libs/java/testng.jar:bin/libs/java/jcommander.jar"
    local native="bin/libs:bin/libs/linux/x64"
    local raw=/tmp/testng.raw.log

    java -ea -Dorg.lwjgl.util.Debug=true -Dorg.lwjgl.util.DebugAllocator=true \
        -Djava.library.path="${native}" -cp "${cp}" \
        org.testng.TestNG -verbose 2 -testclass org.lwjgl.system.MemoryUtilTest >"${raw}" 2>&1
    local status=$?
    cat "${raw}"

    # Keep the complete TestNG log while emitting stable unittest-shaped lines
    # consumed by the generic evaluator.
    if grep -q '^PASSED: testTextDecoding' "${raw}"; then
        echo 'testTextDecoding (org.lwjgl.system.MemoryUtilTest) ... ok'
    else
        echo 'testTextDecoding (org.lwjgl.system.MemoryUtilTest) ... FAIL'
    fi
    if grep -q '^PASSED: testUTF8' "${raw}"; then
        echo 'testUTF8 (org.lwjgl.system.MemoryUtilTest) ... ok'
    else
        echo 'testUTF8 (org.lwjgl.system.MemoryUtilTest) ... FAIL'
    fi
    return "${status}"
}
