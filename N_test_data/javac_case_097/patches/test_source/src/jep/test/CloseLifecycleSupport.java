package jep.test;

import jep.Jep;
import jep.JepException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Collections;
import java.util.Locale;

final class CloseLifecycleSupport {
    private CloseLifecycleSupport() {}

    static Path newMarker() throws Exception {
        Path marker = Files.createTempFile("jep-close-097-", ".txt");
        Files.delete(marker);
        return marker;
    }

    static void installSentinel(Jep jep, Path marker) throws Exception {
        jep.set("_case097_marker", marker.toAbsolutePath().toString());
        jep.eval("import os");
        jep.eval("_case097_fd = os.open(_case097_marker, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 384)");
        jep.eval("class _CloseSentinel(object):\n"
            + "    def __del__(self, writer=os.write, closer=os.close, descriptor=_case097_fd):\n"
            + "        writer(descriptor, b'CLOSED\\n')\n"
            + "        closer(descriptor)\n");
        jep.eval("_case097_sentinel = _CloseSentinel()");
        jep.eval("_case097_value = 42");
        Object value = jep.getValue("_case097_value");
        if (!(value instanceof Number) || ((Number)value).intValue() != 42)
            throw new AssertionError("Interpreter initialization did not complete");
    }

    static void assertNativeClosed(Path marker) throws Exception {
        if (!Files.exists(marker)
            || !Files.readAllLines(marker, StandardCharsets.UTF_8).equals(Collections.singletonList("CLOSED")))
            throw new AssertionError("Python sub-interpreter was not torn down exactly once");
    }

    static void assertUseRejected(Jep jep) throws Exception {
        try {
            jep.eval("_case097_value = 99");
        } catch (JepException expected) {
            if (expected.getMessage() != null
                && expected.getMessage().toLowerCase(Locale.ROOT).contains("closed"))
                return;
            throw new AssertionError("Use failed for a reason other than closed state", expected);
        }
        throw new AssertionError("Closed interpreter remained usable");
    }
}
