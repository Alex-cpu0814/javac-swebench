# Java-C SWE-bench Case 098

This case is derived from ninia/jep Issue #17 and upstream fix commit `340788b3ae7a3e4ccfc610f73d43afeba508241c`.

The Base tree already contains JEP's official `TestMemoryLeaks` Java stress class. The protected test patch exposes that test through the normal `setup.py build` and `jep.Run` unittest framework, repeating sub-interpreter creation, `import java.util`, and close operations under a bounded JVM heap.

## Identity

- Instance: `ninia__jep-17`
- Base: `7af56bffed4e06a2bcdb8b70bf0aa5d59721d7e6`
- Fix: `340788b3ae7a3e4ccfc610f73d43afeba508241c`
- Issue: [#17](https://github.com/ninia/jep/issues/17)

## Directory contract

- `analysis/`: source-row mapping, provenance, environment, and case analysis.
- `patches/`: upstream gold patch and protected regression-test patch.
- `official_swebench/`: private instance, public task, metadata, JSONL, and checksums.
- `evaluator/`: config-driven isolated evaluator and clean Base-image definition.
- `verification/`: immutable build, run, grading, and control evidence.

## Public/private separation

The model-facing record is `official_swebench/public_task_098.json`. The
complete private instance, gold patch, protected test patch, and expected test
outcomes must not be shown during an unbiased model evaluation. Test provenance
is recorded as `official_existing_memory_stress_test_wrapped_for_unittest_runner` in `official_swebench/metadata.json`.
