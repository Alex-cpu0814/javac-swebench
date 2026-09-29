# Case 100 Verification

The gold and protected test patches must apply cleanly to the exact Base
commit. Verification requires Fix + test patch to pass all 5 FAIL_TO_PASS and
69 PASS_TO_PASS tests. Base + test patch must fail the 5 intended tests while
the 69 regression tests remain green.

The evaluator uses Python 2.7.18 and NumPy 1.16.6 because this historical JEP
tree uses Python 2 syntax and enables its NumPy bridge unconditionally.
