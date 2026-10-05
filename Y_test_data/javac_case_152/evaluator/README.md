# Case 152 evaluator

Build `image/Dockerfile`, then inject a candidate patch, the protected test
patch, `run_evaluation.sh`, and `case_adapter.sh` at runtime. The adapter builds
the candidate JNI artifacts offline, compiles only the isolated regression
harness, and emits stable SWE-bench grading lines.

The image contains only the Base checkout and cached public build dependencies;
it contains neither the fix tree nor either evaluation patch.
