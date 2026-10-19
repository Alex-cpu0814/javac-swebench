public final class RunVkFramebufferCreateInfoTests {

    private static int passed;
    private static int failed;

    public static void main(String[] args) {
        run(
            "testNullAttachmentsPreserveAttachmentCount",
            () -> new org.lwjgl.vulkan.VkFramebufferCreateInfoTest()
                .testNullAttachmentsPreserveAttachmentCount()
        );

        run(
            "testNullAttachmentsPassGeneratedValidation",
            () -> new org.lwjgl.vulkan.VkFramebufferCreateInfoTest()
                .testNullAttachmentsPassGeneratedValidation()
        );

        System.out.println();
        System.out.println(
            "RESULT: passed=" + passed + ", failed=" + failed
        );

        if (failed != 0) {
            System.exit(1);
        }
    }

    private static void run(String name, CheckedRunnable action) {
        System.out.println("===== RUN " + name + " =====");

        try {
            action.run();
            passed++;
            System.out.println("PASS: " + name);
        } catch (Throwable throwable) {
            failed++;
            System.out.println("FAIL: " + name);
            throwable.printStackTrace(System.out);
        }

        System.out.println();
    }

    @FunctionalInterface
    private interface CheckedRunnable {
        void run() throws Throwable;
    }
}
