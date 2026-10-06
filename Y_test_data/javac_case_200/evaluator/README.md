# Case 200 evaluator

Build `image/Dockerfile`, then inject a candidate patch, the protected test
patch, `run_evaluation.sh`, and `case_adapter.sh` at runtime. The image contains
only the clean Base checkout and its cached native build.

The container runs as UID/GID 64 because the official oracle distinguishes the
legacy packed value `4194368` from UID `64`. The adapter regenerates the old
Autotools files, rebuilds and installs MDSplus, runs `test-tdishr.tdi` as a
control, and then runs the official `test-treeshr.tdi` owner-ID regression.

