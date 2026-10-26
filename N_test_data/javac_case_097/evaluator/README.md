# Case 097 isolated evaluator

The active image is configured by immutable Docker Hub digest; build_image supplies the mutable tag for rebuilding with build_model_evaluator.py. It uses exact Base, OpenJDK 8 and Python 3.4.10. The source and original tests are rebuilt with setup.py after applying the candidate and then the protected test patch.

From the repository root:

```powershell
python .\N_test_data\javac_case_097\evaluator\evaluate_model_patch.py --patch C:\path\candidate.diff --run-id my-097-run
```

The container has networking disabled and retains structured phase, grading and raw evidence under verification/runs. Each of the three close scenarios launches a child JVM with bounded runtime and explicit completion markers. The original 78 P2P run alongside the two new lifecycle P2P; all 81 expected tests must pass. The Python runner's per-test outcomes are authoritative even when embedded SystemExit is handled by historical JEP and the outer JVM returns zero.

Protected test sources are under patches/test_source and regenerated into test_patch.diff. The marker observes actual Python object finalization, detecting Java-only no-op/flag-only closes. Cross-thread safety claims are limited to the reported stale-JNIEnv close scenario.
