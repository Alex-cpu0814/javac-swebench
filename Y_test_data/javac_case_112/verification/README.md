# Case 112 verification evidence

- `builds/`: immutable image-build and clean-image audit records.
- `runs/`: isolated candidate, Base-control, and gold-control evaluations.
- `controls/`: non-fixing control patches used to prove Base failure.

Each run records raw logs, structured events, a phase result, per-test grading,
and a summary. A valid official-test case must show that the Base control fails
the recorded `FAIL_TO_PASS`, while the upstream gold patch passes all expected
`FAIL_TO_PASS` and `PASS_TO_PASS` targets.
