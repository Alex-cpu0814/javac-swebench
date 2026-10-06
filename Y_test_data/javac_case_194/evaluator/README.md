# Case 194 evaluator

Build `image/Dockerfile`, then inject a candidate patch, the protected test
patch, `run_evaluation.sh`, and `case_adapter.sh` at runtime. The image contains
only the clean Base checkout and its cached native out-of-tree build.

The adapter rebuilds and installs MDSplus serially, runs the existing
`test-tdishr.tdi` control, and then runs the official `test-treeshr.tdi`
regression. It emits stable test identifiers for SWE-bench-style grading.
