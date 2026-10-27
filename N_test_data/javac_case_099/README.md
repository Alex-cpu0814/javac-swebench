# Java-C SWE-bench Case 099

This case is derived from JEP commit `778b516930bdc11ecbb7751d560d373964009639`, which fixes Issue #17 by moving the Java-method cache from a process-global dictionary to the cache owned by each Jep interpreter.

The protected test builds two versions of the same Java class name with different ClassLoaders. It exercises the first version in one Jep instance, closes it, and then exercises the second version in a new Jep instance. Base reuses the stale global method list; the fix keeps the method cache isolated.

## Identity

- Instance: `ninia__jep-17-cache`
- Base: `b1ab138dd6d492c7547e24d0b117aeafb112613d`
- Fix: `778b516930bdc11ecbb7751d560d373964009639`
- Issue: #17

## Verification

The test runs inside a child JVM so a native failure cannot terminate the Python test runner. The Docker evaluator uses OpenJDK 8 and Python 3.4.10, matching the Base tree's supported environment.

The Python test reuses `jep_pipe()` for child process execution and error
reporting, then checks the success marker. The 2026-10-27 Docker runs confirm
that Base fails only this regression and Gold passes all 79 tests; see
`verification/helper_reuse_validation.json`.

The published image is `yutu0814/javac-case-099-jep:benchmark-v1`, with immutable
reference
`yutu0814/javac-case-099-jep@sha256:502cb2beb42e3c90413016c2d2ab33dc53fec30912f04ef8eadd47caeae629ee`.
This release reuses the validated clean Base image; patches and test assets are
injected at runtime. Publication details are in
`verification/docker_publication.json`.

## Directory contract

- `analysis/`: source-row mapping, provenance, environment, and case analysis.
- `patches/`: upstream gold patch and protected regression-test patch.
- `official_swebench/`: private instance, public task, metadata, JSONL, and checksums.
- `evaluator/`: config-driven isolated evaluator and clean Base-image definition.
- `verification/`: immutable build, run, grading, and control evidence.

## Public/private separation

The model-facing record is `official_swebench/public_task_099.json`. The
complete private instance, gold patch, protected test patch, and expected test
outcomes must not be shown during an unbiased model evaluation. Test provenance
is recorded as `synthetic_classloader_regression_test` in `official_swebench/metadata.json`.
