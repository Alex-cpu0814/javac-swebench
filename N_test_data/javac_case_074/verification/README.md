# Verification

`builds/case-074-build-final/summary.json` records the successful clean Base image audit and image ID.

`runs/case-074-base-final/` records FAIL_TO_PASS `allocatorSelection` **FAILED**: on a 64-bit JVM it attempted `libjemalloc32.so` and fell back. PASS_TO_PASS `pointerWidth` **PASSED**: the native pointer width was 8 bytes and `Pointer.BITS64` eventually became true.

`runs/case-074-gold-final/` records both tests **PASSED**: the Fix selected and loaded `libjemalloc.so` and preserved 8-byte pointers.

`runs/case-074-tamper-final/` records rejection of a candidate that pre-created the protected Java test path (`candidate_conflicts_with_test_patch`). All formal controls used the same image ID with container networking disabled.

`focused_reproduction/` preserves the earlier Docker class-initialization comparison and exact `Pointer.java` SHA-256 manifest. This is separate from the formal evaluator. `local_evidence.json` summarizes the final controls. `publication/registry_audit.json` records the anonymous Docker Hub manifest check, digest pull, and offline clean-Base audit. The Linux Base test uses a protected assertion and does not produce the Windows issue's exact `jemalloc32.dll` exception.
