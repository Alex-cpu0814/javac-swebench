# Java-C to SWE-bench Case 096

This case is derived from ninia/jep Issue #22 and upstream fix commit `767509de81f3a11b1ca54e23619d3226944a141e`.

## Scenario

A worker thread creates a `Jep` instance and terminates. The main thread then calls `Jep.close()`. The Base implementation can use a stale JNI environment from the terminated thread and crash the JVM in `pyembed_thread_close`. The protected test runs this scenario in a child JVM process.

## Identity

- Instance: `ninia__jep-22`
- Base: `e4f13ea277ce4809688dde766cc9fd173ec6f63d`
- Fix: `767509de81f3a11b1ca54e23619d3226944a141e`
- Issue: [#22](https://github.com/ninia/jep/issues/22)

## Verification

The protected test patch and gold patch apply cleanly to the exact Base commit. The clean image `javac-case-096-jep:benchmark-v3` uses OpenJDK 8 and Python 3.4.10, within the Base commit's declared Python support. The Base negative control fails the protected regression test, while the upstream gold control passes all 79 expected tests (1 FAIL_TO_PASS and 78 PASS_TO_PASS).

## Directory contract

- `analysis/`: source-row mapping, provenance, environment, and case analysis.
- `patches/`: upstream gold patch and protected regression-test patch.
- `official_swebench/`: private instance, public task, metadata, JSONL, and checksums.
- `evaluator/`: config-driven isolated evaluator and clean Base-image definition.
- `verification/`: immutable build, run, grading, and control evidence.

## Public/private separation

The model-facing record is `official_swebench/public_task_096.json`. The
complete private instance, gold patch, protected test patch, and expected test
outcomes must not be shown during an unbiased model evaluation. Test provenance
is recorded as `synthetic_issue_regression_test` in `official_swebench/metadata.json`.
