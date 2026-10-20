/* Issue-derived protected regression test. */
package org.lwjgl.llvm;

import org.lwjgl.system.MemoryStack;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.lwjgl.llvm.ClangIndex.*;
import static org.lwjgl.system.MemoryStack.stackPush;
import static org.lwjgl.system.MemoryUtil.*;

public final class ClangCStringRegressionTest {
    private static final String SOURCE = "/testbed/config/tests/clang_cstring_fixture.c";

    public static void main(String[] args) {
        if (args.length != 1 || !("direct".equals(args[0]) || "binding".equals(args[0]))) {
            System.err.println("Usage: ClangCStringRegressionTest direct|binding");
            System.exit(2);
        }
        try {
            if (!Files.isRegularFile(Path.of(SOURCE))) {
                throw new IllegalStateException("Missing source fixture: " + SOURCE);
            }
            long index = clang_createIndex(false, false);
            if (index == NULL) {
                throw new IllegalStateException("clang_createIndex returned NULL");
            }
            long tu = NULL;
            try (MemoryStack stack = stackPush()) {
                tu = clang_parseTranslationUnit(index, SOURCE, null, null, 0);
                if (tu == NULL) {
                    throw new IllegalStateException("clang_parseTranslationUnit returned NULL");
                }
                CXString spelling = clang_getTranslationUnitSpelling(tu, CXString.callocStack(stack));
                String direct = memUTF8Safe(memGetAddress(spelling.address()));
                if (!SOURCE.equals(direct)) {
                    throw new IllegalStateException("CXString precondition failed: " + direct);
                }
                String actual = "direct".equals(args[0]) ? direct : clang_getCString(spelling);
                System.out.println("test=" + args[0] + " expected=" + SOURCE + " actual=" + actual);
                if (!SOURCE.equals(actual)) {
                    System.err.println("[FAIL] String mismatch");
                    System.exit(1);
                }
                System.out.println("[PASS] " + args[0]);
                // clang_disposeString is also affected in Base. One string is reclaimed at process exit.
            } finally {
                if (tu != NULL) {
                    clang_disposeTranslationUnit(tu);
                }
                clang_disposeIndex(index);
            }
        } catch (Throwable error) {
            System.err.println("[ERROR] Setup or runtime failure");
            error.printStackTrace();
            System.exit(2);
        }
    }
}
