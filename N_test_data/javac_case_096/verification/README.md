# Case 096 Verification

`gold_patch.diff` and `test_patch.diff` both pass `git apply --check` against the exact Base commit.

The clean image `javac-case-096-jep:benchmark-v3` is pinned to OpenJDK 8 and Python 3.4.10. Python 3.4 is within the versions declared by the Base commit's `setup.py`; Python 3.5 was not declared and reproduced an unrelated JVM crash in the historical suite.

The negative control (`case-096-py34-negative-final`) applies the test patch without the fix and fails `test_close_terminated_thread` (child JVM exit `-6`). The gold control (`case-096-py34-gold`) applies the upstream fix and passes all 79 expected tests: 1 FAIL_TO_PASS and 78 PASS_TO_PASS.

The reusable no-op negative control is `verification/controls/negative_patch.diff`, matching the control layout used by Cases 092 and 093.
