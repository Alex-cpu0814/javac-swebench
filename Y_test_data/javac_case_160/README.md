# Java-C SWE-bench Case 160

This case is derived from `kohlschutter/junixsocket` commit
`34af0c1be2539ea4a1390af711ff933463b834f9`, which completes the write-side
timeout behavior discussed in Issue #90.

## Identity

- Instance: `kohlschutter__junixsocket-90-write-timeout`
- Repository: `kohlschutter/junixsocket`
- Base: `ba3d20f60e7fbf1a49ae1f4bac09111299d104ee`
- Fix: `34af0c1be2539ea4a1390af711ff933463b834f9`
- Issue: [#90](https://github.com/kohlschutter/junixsocket/issues/90)
- Source spreadsheet case: `160` (workbook sequence `161`)

## Test and environment

The protected patch is the exact official upstream test change. The evaluator
builds the JNI library on Linux and runs the read-timeout control followed by
the new write-timeout regression test. A process-level timeout converts the
Base revision's permanent blocking write into a stable test error.

## Evaluator image

`yutu0814/javac-case-160-junixsocket:benchmark-v1`

Digest: `sha256:15fcd1b85e32e2b60df81e65888a891648cf05421aece7b8fbaa0e829be75e24`

Docker Hub: [yutu0814/javac-case-160-junixsocket](https://hub.docker.com/r/yutu0814/javac-case-160-junixsocket)

The image contains only the Base checkout plus cached public build
dependencies. The final isolated controls are `case-160-base-1` and
`case-160-gold-1`.

## Directory contract

- `analysis/`: source-row mapping, provenance, environment, and case analysis.
- `patches/`: upstream gold patch and protected regression-test patch.
- `official_swebench/`: private instance, public task, metadata, JSONL, and checksums.
- `evaluator/`: isolated evaluator and clean Base-image definition.
- `verification/`: image-build, Base-control, and Gold-control evidence.

## Public/private separation

The model-facing record is `official_swebench/public_task_160.json`. The
private instance, gold patch, protected test patch, and expected outcomes must
not be shown during an unbiased evaluation.
