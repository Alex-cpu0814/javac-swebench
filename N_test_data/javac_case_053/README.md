# Java–C SWE-bench Case 053

Instance: `LWJGL__lwjgl3-879`; repository: `LWJGL/lwjgl3`; project version: `3.3.3`.

This N-set case uses a synthetic, issue-derived compilation test. It targets the strict-prototypes diagnostic reported during generated JNI C compilation. The Base-only candidate passed two isolated Base-fails/Fix-passes repetitions, independent review, and explicit human acceptance.

The accepted scope is Linux x86_64 / upstream Clang 14 / OpenJDK 17 with the reported diagnostic explicitly enabled. It does not claim original macOS/Apple Clang reproduction, full Ant builds, generator regeneration, linking, runtime JNI behavior, or module-info generation.

One FAIL_TO_PASS node compiles the actual generated JNI dispatcher. Three PASS_TO_PASS nodes comprise two synthetic compiler/header controls and one existing native-helper compilation; these are not three official project runtime tests.

## Use

Pull the published clean Base evaluator image:

```powershell
docker pull yutu0814/javac-case-053-lwjgl3:benchmark-v1
```

Evaluate a candidate production patch:

```powershell
python evaluator/evaluate_model_patch.py --patch C:\path\candidate.diff
```

Image: `yutu0814/javac-case-053-lwjgl3:benchmark-v1`. Verified Docker Hub digest: `sha256:74b06ab9926769a6f19904b19d8b7f45b3dde7eada5e6c58d478e882044c1c0f`. The image is published at https://hub.docker.com/r/yutu0814/javac-case-053-lwjgl3. Maintainers can rebuild it with `python evaluator/build_model_evaluator.py`; building needs network access. Evaluation disables network and injects the candidate, protected test patch, adapter, and logs at runtime.

Packaged evaluator controls: `case-053-base-1` is unresolved with the target compilation failure and three passing controls; `case-053-gold-1` is resolved with all four nodes passing; `case-053-tamper-1` rejects a candidate that pre-creates the protected test file. See `verification/final_summary.json`. Case-local records, layout and checksums pass validation.

The model-facing record is `official_swebench/public_task_053.json`. Full instances, patches, analysis, evaluator configuration and verification contain private oracle material and must stay out of blind model input.

Directory contract: `analysis/`, `patches/`, `official_swebench/`, `evaluator/`, `verification/`.
