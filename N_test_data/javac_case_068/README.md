# Case 068 — LWJGL OpenVR optional game pose (#418)

This is an **N_test_data** case: the upstream Fix did not add a regression test. The protected Java/C test was derived from issue #418 after the Fix was visible. Base is `2c007161cff7ba12023ae48dd28a7856c0c6da3d`; Fix is `1ae772163cf3eb432cf6f327db5bf5b7fe9aad5f`. The complete upstream diff is `patches/gold_patch.diff`.

The generated Java wrapper for `VRCompositor_WaitGetPoses(render, null)` dereferences the optional game-pose buffer before the native call. The Fix forwards a null native pointer with count zero. In the isolated local evaluator, Base has FAIL_TO_PASS `FAILED` and PASS_TO_PASS `PASSED`; the official Fix has both `PASSED`. A candidate patch that pre-creates the protected test path is rejected.

The model-facing input is only `official_swebench/public_task_068.json`. Do not put `instance_068.json`, `patches/`, or expected test outcomes into a blind repair prompt.

The published image is [`yutu0814/javac-case-068-lwjgl3:benchmark-v1`](https://hub.docker.com/r/yutu0814/javac-case-068-lwjgl3), pinned to `sha256:30a5258e746b1190c9b5d6c6aacbbaa04bdd0f11f4aff0b5605a3eeb8445dfaa`. It contains a clean, shallow checkout of the exact Base commit and LWJGL 3.2.0 dependencies; it contains no Fix commit object, protected test, reference patch, or project binaries. `verification/publication/registry_audit.json` records the public registry check and digest pull. Rebuild it from this directory on a host with Docker, Git and Python 3.10+:

```powershell
Set-Location 'E:\CLB_Swe-bench\javac-swebench\N_test_data\javac_case_068'
python .\evaluator\build_model_evaluator.py --build-id case-068-build-rebuild
```

Run the expected Base and Fix controls (Base exits `1`; Fix exits `0`):

```powershell
python .\evaluator\evaluate_model_patch.py --patch .\verification\controls\base_control.patch --label base
python .\evaluator\evaluate_model_patch.py --patch .\patches\gold_patch.diff --label gold
```

Evaluate a candidate patch with `python .\evaluator\evaluate_model_patch.py --patch C:\path\candidate.diff`. Each result is saved under `verification/runs/<run-id>/`; `summary.json` and `grading.json` give the verdict, while raw build, test, and per-test logs provide evidence. Exit codes are `0` resolved, `1` unresolved, and `2` infrastructure error. The evaluation container runs with no network.

The validator compiles the candidate's generated `VRCompositor.java` from the exact Base checkout against LWJGL 3.2.0 JAR dependencies. It executes a Java call through a protected native function-pointer stub and checks the actual pointer and count, plus a non-null control. It does not run the Kotlin generator or full Ant build, and it does not require or test a real SteamVR compositor, VR headset, GPU, or display. A generated-Java-only candidate can therefore satisfy this oracle while leaving the template stale; the full reference Fix includes both files. See `analysis/README.md` for the scope and `verification/README.md` for evidence.
