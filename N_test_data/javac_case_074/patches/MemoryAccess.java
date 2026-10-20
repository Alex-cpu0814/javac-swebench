package org.lwjgl.system;

/** Focused replacement for the large upstream class. */
final class MemoryAccess {
    static {
        System.load("/results/libpointerprobe.so");
    }

    static native int getPointerSize();
}
