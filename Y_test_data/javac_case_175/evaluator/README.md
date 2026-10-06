# Case 175 evaluator

Build `image/Dockerfile`, then inject a candidate patch, the protected test
patch, `run_evaluation.sh`, `case_adapter.sh`, and `report_surefire.py` at
runtime. The image contains only the clean Base checkout and cached public
dependencies.

The adapter builds the JNI library and the complete Jetty reactor offline.
Using `-DskipTests` retains the `junixsocket-common` test-jar required by the
Jetty module. It then runs `testHTTPOverUnixDomain` as a stable small-response
control and the official `testLargeBody` regression separately.
