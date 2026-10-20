# Local evaluator

`build_model_evaluator.py` packages a depth-one Git checkout of Base into an image, downloads LWJGL 3.2.0 dependencies from Maven Central, verifies their SHA-256 values, and audits the image for a clean Base source and absence of protected tests and compiled project classes. The default source checkout is `E:/CLB_Swe-bench/_work/lwjgl3-100` when present; otherwise it fetches the specified commit from upstream. `--source-repo` and `--repo-url` override this choice.

`evaluate_model_patch.py` applies a candidate patch to a fresh container checkout before injecting `patches/test_patch.diff`. It rejects candidates that pre-create a protected test path. The container compiles the current generated OpenVR Java class, compiles the protected C/Java fixture, and runs two modes in separate JVMs. The helper's native function pointer occupies `IVRCompositor` table slot 2, the `WaitGetPoses` entry.

Only the generated Java class is compiled from candidate source. The Kotlin template is included in the full official patch and dataset record but is not regenerated or checked by the automated oracle. Candidate evaluations use the published digest-pinned image in `case_config.json` unless `--image` is supplied. Rebuilds still use the separate local `build_image` tag.
