package org.lwjgl.system;

/** Protected issue-derived tests, run in separate JVMs. */
public final class PointerInitializationProbe {
    public static void main(String[] args) {
        if (args.length != 1)
            throw new IllegalArgumentException("Expected one test mode");
        if (!System.getProperty("os.arch").contains("64"))
            throw new AssertionError("A 64-bit JVM is required");

        int size = Pointer.POINTER_SIZE;
        MemoryUtil.initialize();
        System.out.println("pointer_size=" + size + " bits64=" + Pointer.BITS64);
        System.out.println("attempted_library=" + AllocatorProbe.attempted
                + " loaded=" + AllocatorProbe.loaded);

        if (size != 8 || !Pointer.BITS64)
            throw new AssertionError("Native pointer width is incorrect");
        if ("pointerWidth".equals(args[0])) {
            System.out.println("[PASS] pointerWidth");
            return;
        }
        if (!"allocatorSelection".equals(args[0]))
            throw new IllegalArgumentException("Unknown mode: " + args[0]);
        if (!"libjemalloc.so".equals(AllocatorProbe.attempted) || !AllocatorProbe.loaded)
            throw new AssertionError("64-bit JVM selected the wrong jemalloc library");
        System.out.println("[PASS] allocatorSelection");
    }
}
