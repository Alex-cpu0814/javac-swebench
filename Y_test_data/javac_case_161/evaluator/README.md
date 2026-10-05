# Case 161 evaluator

Build `image/Dockerfile`, then inject a candidate patch, the protected test
patch, `run_evaluation.sh`, `case_adapter.sh`, and `report_surefire.py` at
runtime. The image contains only the clean Base checkout and cached public
dependencies.

The upstream defect lies in the poll-based read implementation selected on
Solaris and BSD-family systems. Because Docker Desktop runs Linux, the adapter
adds the project's own `junixsocket_use_poll_for_read` compiler define. It does
not alter project source and exercises exactly the native branch changed by
the official fix.

The adapter builds JNI artifacts offline, runs `issue14Pass` as the stable
control, and then runs the official `testSocketTimeoutException` regression.
