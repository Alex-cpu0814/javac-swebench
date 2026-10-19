import org.lwjgl.Version;
import org.lwjgl.system.MemoryStack;
import org.lwjgl.vulkan.VkFramebufferCreateInfo;

public final class VulkanFramebufferRepro {
    public static void main(String[] args) {
        System.out.println("LWJGL=" + Version.getVersion());
        System.out.println("JAVA=" + System.getProperty("java.version"));
        System.out.println("OS_ARCH=" + System.getProperty("os.arch"));

        try (MemoryStack stack = MemoryStack.stackPush()) {
            VkFramebufferCreateInfo info =
                VkFramebufferCreateInfo.callocStack(stack);

            // Imageless framebuffer:
            // pAttachments is allowed to be NULL while attachmentCount is nonzero.
            info.pAttachments(null);
            VkFramebufferCreateInfo.nattachmentCount(info.address(), 2);

            System.out.println("ATTACHMENT_COUNT=" + info.attachmentCount());
            System.out.println("P_ATTACHMENTS=NULL");
            System.out.println("CALLING_OLD_GENERATED_VALIDATE");

            // The parent revision incorrectly requires pAttachments to be non-NULL.
            VkFramebufferCreateInfo.validate(info.address());

            System.out.println("UNEXPECTED: validation accepted the structure");
        }
    }
}
