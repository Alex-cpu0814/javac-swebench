# Java-C SWE-bench Case 175

This case is derived from `kohlschutter/junixsocket` commit
`3994501308902ffb5d2eb7bce44971e3438b2a91`, which fixes Issue #135.

## Identity

- Instance: `kohlschutter__junixsocket-135`
- Repository: `kohlschutter/junixsocket`
- Base: `2a159927761424440f7dbd7674992e4b5273a459`
- Fix: `3994501308902ffb5d2eb7bce44971e3438b2a91`
- Issue: [#135](https://github.com/kohlschutter/junixsocket/issues/135)
- Source spreadsheet case: `175` (workbook sequence `176`)
- Duplicate skipped: source case `176` (workbook sequence `177`)

## Test and environment

The protected patch is the exact official upstream Jetty regression test. The
evaluator builds the JNI library and complete Jetty reactor, runs an existing
small HTTP-over-AF_UNIX control, and then verifies a random 512 KiB response
byte-for-byte.

## Evaluator image

Published image: `yutu0814/javac-case-175-junixsocket:benchmark-v1`

Published digest: `sha256:d5eaaed040c90536d22f0ef5548ad00d2ec61b59e698d725014695479df8a20d`

Image ID: `sha256:d5eaaed040c90536d22f0ef5548ad00d2ec61b59e698d725014695479df8a20d`

The image contains only the Base checkout plus cached public build
dependencies. The final isolated controls are `case-175-base-1` and
`case-175-gold-1`. The verified image is published on Docker Hub.

## Directory contract

- `analysis/`: source-row mapping, provenance, environment, and case analysis.
- `patches/`: upstream gold patch and protected regression-test patch.
- `official_swebench/`: private instance, public task, metadata, JSONL, and checksums.
- `evaluator/`: isolated evaluator and clean Base-image definition.
- `verification/`: image-build, Base-control, Gold-control, and diagnostic evidence.

## Public/private separation

The model-facing record is `official_swebench/public_task_175.json`. The
private instance, gold patch, protected test patch, and expected outcomes must
not be shown during an unbiased evaluation.
