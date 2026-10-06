# Java-C SWE-bench Case 200

This case is derived from `MDSplus/mdsplus` commit
`707f1656dc68c3c863f4d46d4b5a8ce663f0cdad`, which fixes Issue #2375 through
PR #2379.

## Identity

- Instance: `MDSplus__mdsplus-2375`
- Repository: `MDSplus/mdsplus`
- Base: `f6c82e695f5b6964daeec2c4e0bc449a89be892a`
- Fix: `707f1656dc68c3c863f4d46d4b5a8ce663f0cdad`
- Issue: [#2375](https://github.com/MDSplus/mdsplus/issues/2375)
- Pull request: [#2379](https://github.com/MDSplus/mdsplus/pull/2379)
- Source spreadsheet case: `200` (workbook sequence `201`)

## Test and environment

The protected patch is the exact official expected-output change for the
existing `test-treeshr.tdi` integration test. The evaluator builds MDSplus as
UID/GID 64, runs an existing TDI control, and verifies that `owner_id` returns
the UID (`64`) rather than the legacy packed GID/UID value (`4194368`).

## Evaluator image

Published image: `yutu0814/javac-case-200-mdsplus:benchmark-v1`

Published digest: `sha256:77c71ce09d01e830e0b98f3607636f0ffb03abc24ad51498190f6e7e0fb961dd`

Image ID: `sha256:77c71ce09d01e830e0b98f3607636f0ffb03abc24ad51498190f6e7e0fb961dd`

The image contains only the clean Base checkout and cached public build
dependencies. The final isolated controls are `case-200-base-1` and
`case-200-gold-1`. The verified image is published on Docker Hub.

## Directory contract

- `analysis/`: source-row mapping, provenance, environment, and case analysis.
- `patches/`: upstream gold patch and protected regression-oracle patch.
- `official_swebench/`: private instance, public task, metadata, JSONL, and checksums.
- `evaluator/`: isolated evaluator and clean Base-image definition.
- `verification/`: image-build, Base-control, Gold-control, and probe evidence.

## Public/private separation

The model-facing record is `official_swebench/public_task_200.json`. The
private instance, gold patch, protected test patch, and expected outcomes must
not be shown during an unbiased evaluation.

