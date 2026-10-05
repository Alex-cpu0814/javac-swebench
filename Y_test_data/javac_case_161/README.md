# Java-C SWE-bench Case 161

This case is derived from `kohlschutter/junixsocket` commit
`ba3d20f60e7fbf1a49ae1f4bac09111299d104ee`, which fixes read-side timeout
behavior discussed in Issue #90.

## Identity

- Instance: `kohlschutter__junixsocket-90-read-timeout`
- Repository: `kohlschutter/junixsocket`
- Base: `1df1513c64079a5100cdc2a372558e1f77849c0f`
- Fix: `ba3d20f60e7fbf1a49ae1f4bac09111299d104ee`
- Issue: [#90](https://github.com/kohlschutter/junixsocket/issues/90)
- Source spreadsheet case: `161` (workbook sequence `162`)
- Duplicate skipped: source case `162` (workbook sequence `163`)

## Test and environment

The protected patch is the exact official upstream regression test. The
evaluator builds the JNI library on Linux with the upstream poll-read feature
path enabled, reproducing the Solaris/BSD code path changed by the fix. It then
runs one pre-existing control and the official timeout regression separately.

## Evaluator image

`yutu0814/javac-case-161-junixsocket:benchmark-v1`

Digest: `sha256:969c2650967701f77c0d620466db2df05b0f5f8b6706167dbf117545f54a2ad3`

Docker Hub: [yutu0814/javac-case-161-junixsocket](https://hub.docker.com/r/yutu0814/javac-case-161-junixsocket)

The image contains only the Base checkout plus cached public build
dependencies. The final isolated controls are `case-161-base-2` and
`case-161-gold-1`.

## Directory contract

- `analysis/`: source-row mapping, provenance, environment, and case analysis.
- `patches/`: upstream gold patch and protected regression-test patch.
- `official_swebench/`: private instance, public task, metadata, JSONL, and checksums.
- `evaluator/`: isolated evaluator and clean Base-image definition.
- `verification/`: image-build, Base-control, Gold-control, and diagnostic evidence.

## Public/private separation

The model-facing record is `official_swebench/public_task_161.json`. The
private instance, gold patch, protected test patch, and expected outcomes must
not be shown during an unbiased evaluation.
