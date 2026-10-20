package org.lwjgl.system;

/** Keeps the upstream initialization dependency relevant to issue #115. */
final class MemoryUtil {
    static {
        System.load("/results/libpointerprobe.so");
        AllocatorProbe.initialize();
    }

    static native int memGetPointerSize();

    static void initialize() {}
}
