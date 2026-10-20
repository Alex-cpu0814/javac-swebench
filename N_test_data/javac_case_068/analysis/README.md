# Case 068 source and scope

Issue: https://github.com/LWJGL/lwjgl3/issues/418

The sole parent of Fix `1ae772163cf3eb432cf6f327db5bf5b7fe9aad5f` is Base `2c007161cff7ba12023ae48dd28a7856c0c6da3d`. The official Fix changes three files: release notes, the generated Java binding, and its Kotlin template. The exact upstream diff is `../patches/gold_patch.diff`.

The original issue reported a Java NPE when the optional `pGamePoseArray` argument is null. The protected test runs the wrapper through a C function-pointer stub and checks the actual pointer/count arguments. A non-null control checks that the normal path still works. These tests were designed with the Fix visible; they are not official upstream tests and are not blinded.

The evaluator compiles the current generated Java binding from the candidate source against LWJGL 3.2.0 release dependencies. It does not run the Kotlin generator or the full Ant build, and it does not test a real SteamVR compositor, headset, GPU, or display. This limitation is part of the case definition rather than an inferred upstream guarantee. The issue also mentions `GetLastPoses`; this Fix only changes `WaitGetPoses`, which is the tested scope.
