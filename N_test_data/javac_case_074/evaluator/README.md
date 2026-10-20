# Local evaluator

`build_model_evaluator.py` packages a depth-one Git checkout of the exact Base commit into a Java 8/Linux x86_64 image, then checks that the worktree is clean and contains no Fix commit object, protected test, or project binaries. It uses `E:/CLB_Swe-bench/_work/lwjgl3-100` when available, or fetches the exact Base commit from upstream; `--source-repo` and `--repo-url` override the source.

`evaluate_model_patch.py` applies a candidate patch before injecting `patches/test_patch.diff`. Pre-creating any protected test path causes a conflict and is rejected. The evaluator compiles the candidate's `Pointer.java` against protected stubs, compiles two protected JNI/shared-library fixtures, and runs the allocator-selection and pointer-width tests in separate JVMs with container networking disabled.

The default image is the published, digest-pinned reference in `case_config.json`; use `--image` to select another image. `build_image` is the local rebuild target. Only `Pointer.java` is compiled from candidate source; this Linux oracle checks the wrong 32-bit library selection, not the original Windows `jemalloc32.dll` exception or the rest of the official five-file Fix or historical full project build.
