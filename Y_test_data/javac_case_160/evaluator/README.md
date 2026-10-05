# Case 160 evaluator

Build `image/Dockerfile`, then inject a candidate patch, the protected test
patch, `run_evaluation.sh`, `case_adapter.sh`, and `report_surefire.py` at
runtime. The adapter builds the JNI artifacts offline and runs the read and
write timeout methods separately.

The Base write method blocks forever, so the adapter applies a 15-second
process limit and emits a stable `ERROR` result when the limit expires. The
image contains only the Base checkout and cached public build dependencies; it
contains neither the fix commit nor either evaluation patch.
