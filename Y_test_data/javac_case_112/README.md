# Java-C SWE-bench Case 112

This case is derived from OpenJPEG merge commit
`5d953558de8dc4d939b8147fe9547533a8804297`, which fixes Issue #571: a
supposedly lossless JPEG 2000 round trip changes pixels on 32-bit Linux/x86.

## Identity

- Instance: `uclouvain__openjpeg-571`
- Repository: `uclouvain/openjpeg`
- Base: `4f5ec07c315872bdee0885be085ebf57cede2db9`
- Fix: `5d953558de8dc4d939b8147fe9547533a8804297`
- Issue: [#571](https://github.com/uclouvain/openjpeg/issues/571)
- Pull request: [#579](https://github.com/uclouvain/openjpeg/pull/579)
- Source spreadsheet sequence: `112`

## Test and environment

The protected patch is the exact upstream regression-test portion of the fix.
The evaluator builds the Base as 32-bit x86 with GCC, runs the official
`issue571.tif` lossless encode/decode sequence, and compares every component
with the upstream `compare_images` utility. The input file is pinned to the
historical `openjpeg-data` commit and verified by SHA-256.

## Published evaluator image

`yutu0814/javac-case-112-openjpeg:benchmark-v1`

Digest: `sha256:33a22445240b5d6abba03d5c41a277d721fc8940f51aa3e7b7138daeb2f87305`

## Directory contract

- `analysis/`: source-row mapping, provenance, environment, and case analysis.
- `patches/`: upstream gold patch and protected regression-test patch.
- `official_swebench/`: private instance, public task, metadata, JSONL, and checksums.
- `evaluator/`: config-driven isolated evaluator and clean Base-image definition.
- `verification/`: immutable build, run, grading, and control evidence.

## Public/private separation

The model-facing record is `official_swebench/public_task_112.json`. The
complete private instance, gold patch, protected test patch, and expected test
outcomes must not be shown during an unbiased model evaluation. Test provenance
is recorded as `official_upstream_regression_test` in `official_swebench/metadata.json`.
