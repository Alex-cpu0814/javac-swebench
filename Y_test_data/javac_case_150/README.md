# Java-C SWE-bench Case 150

This case is derived from `kohlschutter/junixsocket` commit
`f8f280c8b27c47b17d627eb0efd2e33317d4b46d`, which fixes Issue #116.

## Identity

- Instance: `kohlschutter__junixsocket-116`
- Repository: `kohlschutter/junixsocket`
- Base: `7578a2470871e12dd72716925f60d857ad7eb409`
- Fix: `f8f280c8b27c47b17d627eb0efd2e33317d4b46d`
- Issue: [#116](https://github.com/kohlschutter/junixsocket/issues/116)
- Source spreadsheet sequence: `150`

## Test and environment

The protected patch is the exact upstream regression-test portion of the fix.
The evaluator builds the JNI library on Linux and runs the official
`AbstractNamespaceTest` plus the new address-construction control test.

## Published evaluator image

`yutu0814/javac-case-150-junixsocket:benchmark-v1`

Digest: `sha256:1e6da170e3dc03c5245f2c4ce3a47c2b4e200615df73876ed17a2ffa015d5a35`

Docker Hub: [yutu0814/javac-case-150-junixsocket](https://hub.docker.com/r/yutu0814/javac-case-150-junixsocket)

The final isolated controls are `case-150-base-2` and `case-150-gold-1`.

## Directory contract

- `analysis/`: source-row mapping, provenance, environment, and case analysis.
- `patches/`: upstream gold patch and protected regression-test patch.
- `official_swebench/`: private instance, public task, metadata, JSONL, and checksums.
- `evaluator/`: isolated evaluator and clean Base-image definition.
- `verification/`: immutable build, Base-control, and gold-control evidence.

## Public/private separation

The model-facing record is `official_swebench/public_task_150.json`. The
private instance, gold patch, protected test patch, and expected outcomes must
not be shown during an unbiased evaluation.
