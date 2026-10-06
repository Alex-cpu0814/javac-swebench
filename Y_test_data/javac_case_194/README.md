# Java-C SWE-bench Case 194

This case is derived from `MDSplus/mdsplus` commit
`687b2621aa4dcebc3cc5ee9cd780f38fefd8af87`, which fixes Issue #1423.

## Identity

- Instance: `MDSplus__mdsplus-1423`
- Repository: `MDSplus/mdsplus`
- Base: `a73d6e87149698e49026e3bf8055efc6bbe71d90`
- Fix: `687b2621aa4dcebc3cc5ee9cd780f38fefd8af87`
- Issue: [#1423](https://github.com/MDSplus/mdsplus/issues/1423)
- Source spreadsheet case: `194` (workbook sequence `195`)

## Test and environment

The protected patch is the exact official TreeShr TDI regression script and
expected output. The evaluator performs a native Autotools build, runs an
existing TDI control, and verifies that malformed node names return TreeNNF
without terminating the process.

## Evaluator image

Published image: `yutu0814/javac-case-194-mdsplus:benchmark-v1`

Published digest: `sha256:d12be7067ce51c31c085739c3a3fc4c69d273b8751059234700870a2ce9e5606`

Image ID: `sha256:d12be7067ce51c31c085739c3a3fc4c69d273b8751059234700870a2ce9e5606`

The image contains only the Base checkout and cached public build dependencies.
The final isolated controls are `case-194-base-1` and `case-194-gold-1`. The
verified image is published on Docker Hub.

## Directory contract

- `analysis/`: source-row mapping, provenance, environment, and case analysis.
- `patches/`: upstream gold patch and protected regression-test patch.
- `official_swebench/`: private instance, public task, metadata, JSONL, and checksums.
- `evaluator/`: isolated evaluator and clean Base-image definition.
- `verification/`: image-build, Base-control, Gold-control, and probe evidence.

## Public/private separation

The model-facing record is `official_swebench/public_task_194.json`. The
private instance, gold patch, protected test patch, and expected outcomes must
not be shown during an unbiased evaluation.
