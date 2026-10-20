package org.lwjgl.openvr;

import org.lwjgl.PointerBuffer;
import org.lwjgl.system.MemoryUtil;

public final class VRCompositorNullGamePoseTest {
    private static native long stubFunction();
    private static native int callCount();
    private static native long renderAddress();
    private static native int renderCount();
    private static native long gameAddress();
    private static native int gameCount();

    private static int run(String mode) {
        if (!("nullGamePose".equals(mode) || "nonNullGamePose".equals(mode))) {
            System.err.println("Usage: VRCompositorNullGamePoseTest nullGamePose|nonNullGamePose");
            return 2;
        }
        PointerBuffer table = null;
        TrackedDevicePose.Buffer render = null;
        TrackedDevicePose.Buffer game = null;
        try {
            System.load("/results/libvrprobe.so");
            table = MemoryUtil.memCallocPointer(128);
            render = TrackedDevicePose.calloc(1);
            if ("nonNullGamePose".equals(mode)) {
                game = TrackedDevicePose.calloc(2);
            }
            table.put(2, stubFunction());
            OpenVR.VRCompositor = new OpenVR.IVRCompositor(MemoryUtil.memAddress(table));
            int result;
            try {
                result = VRCompositor.VRCompositor_WaitGetPoses(render, game);
            } catch (NullPointerException error) {
                System.err.println("[FAIL] " + mode + ": NPE before native call; calls=" + callCount());
                error.printStackTrace(System.err);
                return 1;
            }
            long expectedGameAddress = game == null ? 0 : game.address();
            int expectedGameCount = game == null ? 0 : game.remaining();
            System.out.printf("[NATIVE] mode=%s result=%d calls=%d renderAddress=%d renderCount=%d gameAddress=%d gameCount=%d%n",
                mode, result, callCount(), renderAddress(), renderCount(), gameAddress(), gameCount());
            if (result != 418 || callCount() != 1 || renderAddress() != render.address()
                    || renderCount() != 1 || gameAddress() != expectedGameAddress
                    || gameCount() != expectedGameCount) {
                System.err.println("[FAIL] " + mode + ": native argument mismatch");
                return 1;
            }
            System.out.println("[PASS] " + mode);
            return 0;
        } catch (Throwable error) {
            System.err.println("[ERROR] " + mode + ": setup or runtime failure");
            error.printStackTrace(System.err);
            return 2;
        } finally {
            if (game != null) game.free();
            if (render != null) render.free();
            if (table != null) MemoryUtil.memFree(table);
        }
    }

    public static void main(String[] args) {
        System.exit(run(args.length == 1 ? args[0] : ""));
    }
}
