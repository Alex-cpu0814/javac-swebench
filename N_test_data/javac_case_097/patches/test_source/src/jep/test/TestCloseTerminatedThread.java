package jep.test;

import jep.Jep;
import java.nio.file.Files;
import java.nio.file.Path;

public final class TestCloseTerminatedThread {
    public static void main(String[] args) throws Exception {
        for (int i = 0; i < 3; i++) {
            final Path marker = CloseLifecycleSupport.newMarker();
            final Jep[] holder = new Jep[1];
            final Throwable[] failure = new Throwable[1];
            Thread creator = new Thread(new Runnable() {
                @Override
                public void run() {
                    try {
                        holder[0] = new Jep(false, ".");
                        CloseLifecycleSupport.installSentinel(holder[0], marker);
                    } catch (Throwable error) {
                        failure[0] = error;
                    }
                }
            }, "jep-creator-" + i);
            creator.setDaemon(true);
            try {
                creator.start();
                creator.join(15000);
                if (creator.isAlive())
                    throw new AssertionError("Creator thread did not terminate within 15 seconds");
                if (failure[0] != null)
                    throw new AssertionError("Jep creation failed", failure[0]);
                if (holder[0] == null)
                    throw new AssertionError("Jep instance was not created");
                System.out.println("CLOSING:" + i);
                System.out.flush();
                holder[0].close();
                CloseLifecycleSupport.assertNativeClosed(marker);
                CloseLifecycleSupport.assertUseRejected(holder[0]);
                System.out.println("CLOSE_STEP:" + i);
            } finally {
                Files.deleteIfExists(marker);
            }
        }
        System.out.println("CLOSE_OK");
    }
}
