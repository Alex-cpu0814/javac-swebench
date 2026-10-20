# Case 074 provenance and scope

Issue: https://github.com/LWJGL/lwjgl3/issues/115

The sole parent of Fix `4fb6618bfd8990b8a0b805f589a76ff4a1b56684` is Base `1fa5a394949cad836a104d8e5093f734d26ff8e1`. The upstream diff changes five files: two JNI C classes and three Java classes. It includes no regression test. `../patches/gold_patch.diff` is compared byte-for-byte with the local pinned Git diff by `verify_case.py`.

The original issue describes a 64-bit Windows process trying to load `jemalloc32.dll`; the maintainer confirmed the problem and the reporter confirmed a later build worked. The issue-derived protected test evaluates the underlying Java initialization cycle on Linux x86_64 with a real JNI pointer-width function and an intentionally small loadable 64-bit jemalloc stub. The allocator-name conditional matches the historical Kotlin template. The test and reference Fix were not independently blinded.

The formal oracle compiles only candidate `Pointer.java`. The protected fixture stands in for the large historical `MemoryUtil`, `MemoryAccess`, generated `JEmalloc`, and native allocator components. The full Ant/Kotlin build and original Windows DLL failure are outside the validated scope. This case should be described as a limited-scope root-cause benchmark, not a complete upstream build reproduction.
