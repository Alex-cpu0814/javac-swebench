package org.lwjgl.system;

/** Mimics the exact architecture choice in the pinned jemalloc Kotlin template. */
final class AllocatorProbe {
    static String attempted;
    static boolean loaded;

    static void initialize() {
        String name = Pointer.BITS64 ? "jemalloc" : "jemalloc32";
        attempted = "lib" + name + ".so";
        try {
            System.loadLibrary(name);
            loaded = true;
        } catch (UnsatisfiedLinkError error) {
            loaded = false;
        }
        System.out.println("attempted_library=" + attempted + " loaded=" + loaded);
    }
}
