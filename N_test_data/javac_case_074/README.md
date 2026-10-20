# Case 074 — LWJGL pointer-size initialization selects 32-bit jemalloc (#115)

This is an **N_test_data** case: the upstream Fix did not add a regression test. The issue-derived protected test was constructed after the Fix was visible. Base is `1fa5a394949cad836a104d8e5093f734d26ff8e1`; Fix is `4fb6618bfd8990b8a0b805f589a76ff4a1b56684`. `patches/gold_patch.diff` is the complete, byte-exact five-file upstream diff.

On a 64-bit JVM, Base initializes `Pointer.POINTER_SIZE` through `MemoryUtil`. Its allocator initialization reads `Pointer.BITS64` before `Pointer` has finished initializing, so it selects the 32-bit jemalloc name. The local Linux oracle observes `libjemalloc32.so` failing to load while `Pointer.POINTER_SIZE` ultimately reports 8. The Fix initializes pointer size through `MemoryAccess` first, then selects and loads `libjemalloc.so`. The original report concerned `jemalloc32.dll` on Windows.

**Reproduction fidelity:** The original [issue #115](https://github.com/LWJGL/lwjgl3/issues/115) shows `java.lang.ExceptionInInitializerError` and `Failed to load library: jemalloc32.dll (error code = 0)` on Windows. This Linux Docker evaluator does **not** reproduce that exact exception, DLL name, operating system, or full LWJGL startup path. Its Base control instead prints `attempted_library=libjemalloc32.so loaded=false` and fails a protected assertion; the Fix control prints `attempted_library=libjemalloc.so loaded=true`. It tests the same initialization-order and 32-bit-library-selection mechanism, so it should be described as an issue-derived Linux equivalent, not an exact replay of the reporter's log.

The formal evaluator uses a clean, shallow checkout of the exact Base commit in the published image `yutu0814/javac-case-074-lwjgl3@sha256:bf12eb7755f877cb56804e10e4a1336856d076f7fe76c92935124febce443226`. It contains neither the Fix commit object nor protected test files or project binaries. The [Docker Hub image](https://hub.docker.com/r/yutu0814/javac-case-074-lwjgl3) has been pulled by digest and audited offline. The model-facing input is only `official_swebench/public_task_074.json`; keep `instance_074.json`, `patches/`, and expected outcomes out of a blind repair prompt.

Rebuild on a host with Docker, Git, and Python 3.10+:

```powershell
Set-Location 'E:\CLB_Swe-bench\javac-swebench\N_test_data\javac_case_074'
python .\evaluator\build_model_evaluator.py --build-id case-074-build-rebuild
```

Run the Base and reference controls (Base exits `1`, Fix exits `0`):

```powershell
python .\evaluator\evaluate_model_patch.py --patch .\verification\controls\base_control.patch --label base
python .\evaluator\evaluate_model_patch.py --patch .\patches\gold_patch.diff --label gold
```

Evaluate a candidate patch with `python .\evaluator\evaluate_model_patch.py --patch C:\path\candidate.diff`. Results are saved under `verification/runs/<run-id>/`. `summary.json` and `grading.json` give the verdict; per-test logs show the selected library. Evaluation containers run with no network. Exit codes are `0` resolved, `1` unresolved, and `2` infrastructure error.

**Scope:** The evaluator compiles the candidate's original `Pointer.java` against protected small `MemoryUtil`, `MemoryAccess`, and allocator stubs. A protected JNI function returns real `sizeof(void *)`, and a loadable 64-bit jemalloc stub makes the name selection observable. The full 2015 Ant/Kotlin build, other four changed source files, real jemalloc behavior, and original Windows DLL loading are **not** graded. A `Pointer.java`-only candidate could pass this oracle while leaving other upstream changes undone. See `analysis/README.md` for provenance and `verification/README.md` for results.
