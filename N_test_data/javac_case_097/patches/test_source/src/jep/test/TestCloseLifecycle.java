package jep.test;

import jep.Jep;
import java.nio.file.Files;
import java.nio.file.Path;

public final class TestCloseLifecycle {
    public static void main(String[] args) throws Exception {
        if (args.length != 1 || !("same-thread".equals(args[0]) || "double-close".equals(args[0])))
            throw new AssertionError("Expected a close lifecycle mode");
        Path marker = CloseLifecycleSupport.newMarker();
        try {
            Jep jep = new Jep(false, ".");
            CloseLifecycleSupport.installSentinel(jep, marker);
            jep.close();
            CloseLifecycleSupport.assertNativeClosed(marker);
            CloseLifecycleSupport.assertUseRejected(jep);
            if ("double-close".equals(args[0])) {
                jep.close();
                CloseLifecycleSupport.assertNativeClosed(marker);
            }
            // A fresh interpreter must still work on the same owner thread.
            Jep next = new Jep(false, ".");
            try {
                next.eval("value = 42");
                if (((Number)next.getValue("value")).intValue() != 42)
                    throw new AssertionError("New interpreter did not work after close");
            } finally {
                next.close();
            }
        } finally {
            Files.deleteIfExists(marker);
        }
        System.out.println("LIFECYCLE_OK:" + args[0]);
    }
}
