# Case 096 SWE-bench record

- Instance: `ninia__jep-22`
- Issue: #22
- Base: `e4f13ea277ce4809688dde766cc9fd173ec6f63d`
- Fix: `767509de81f3a11b1ca54e23619d3226944a141e`
- FAIL_TO_PASS: 1
- PASS_TO_PASS: 78

The complete instance contains the protected synthetic regression test and the upstream gold patch. `public_task_096.json` is the model-facing record.

The reproducible Docker environment uses OpenJDK 8 and Python 3.4.10. Base + test patch fails the protected test; Base + upstream fix + test patch passes all 79 expected tests.
