#!/usr/bin/env bash
set -euo pipefail

source_root=${1:-/source}
support_root=${2:-/support}
output_root=${3:-/results}
adapter_root=${4:-/benchmark}
mkdir -p "$output_root/classes" "$output_root/empty-sourcepath"

baseline_cp="$support_root/lwjgl3-parent/bin/classes/lwjgl/core:$support_root/lwjgl3-parent/bin/classes/lwjgl/vulkan:$support_root/lwjgl3-parent/bin/libs/java/jsr305.jar:$support_root/lwjgl3-parent/bin/libs/java/testng.jar:$support_root/lwjgl3-parent/bin/libs/java/jcommander.jar"
struct_file=modules/lwjgl/vulkan/src/generated/java/org/lwjgl/vulkan/VkFramebufferCreateInfo.java
test_file=modules/lwjgl/vulkan/src/test/java/org/lwjgl/vulkan/VkFramebufferCreateInfoTest.java

{
    javac -encoding UTF-8 -sourcepath "$output_root/empty-sourcepath" \
        -cp "$baseline_cp" -d "$output_root/classes" "$source_root/$struct_file"
    evaluation_cp="$output_root/classes:$baseline_cp"
    javac -encoding UTF-8 -sourcepath "$output_root/empty-sourcepath" \
        -cp "$evaluation_cp" -d "$output_root/classes" "$source_root/$test_file"
    javac -encoding UTF-8 -sourcepath "$output_root/empty-sourcepath" \
        -cp "$evaluation_cp" -d "$output_root/classes" \
        "$adapter_root/RunVkFramebufferCreateInfoTests.java"
} > "$output_root/compilation.raw.log" 2>&1 || {
    cat "$output_root/compilation.raw.log"
    exit 2
}

set +e
java -Dorg.lwjgl.librarypath="$support_root/runtime/lwjgl-native/linux/x64/org/lwjgl" \
    -cp "$evaluation_cp" RunVkFramebufferCreateInfoTests \
    2>&1 | tee "$output_root/tests.raw.log"
test_status=${PIPESTATUS[0]}
exit "$test_status"
