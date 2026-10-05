# Java-C SWE-bench Case 152

This case is derived from `kohlschutter/junixsocket` commit
`2f8f096b84fba1ae26058d41cc03df47719379df`, which fixes Issue #97.

## Identity

- Instance: `kohlschutter__junixsocket-97`
- Repository: `kohlschutter/junixsocket`
- Base: `4f7667c4655712fc7371c0dbab0de5bf785e5d3d`
- Fix: `2f8f096b84fba1ae26058d41cc03df47719379df`
- Issue: [#97](https://github.com/kohlschutter/junixsocket/issues/97)
- Source spreadsheet sequence: `152`
- Duplicate source sequences: `153`–`159` (same repository and fix commit; not remade)

## Test and environment

The protected test preserves the official upstream forked-VM regression logic
in an isolated harness that compiles against both sides of the commit's large
API refactor. The evaluator builds the JNI library on Linux, verifies that a
socket file descriptor can become `ProcessBuilder.Redirect`, and runs a stable
file-descriptor control.

## Evaluator image

`yutu0814/javac-case-152-junixsocket:benchmark-v1`

Image ID: `sha256:34489d29f08f54938761edd96b22ef7638687867c33e37101fec92a777fbc973`

Docker Hub: [yutu0814/javac-case-152-junixsocket](https://hub.docker.com/r/yutu0814/javac-case-152-junixsocket)

The published image contains only the Base checkout plus cached public build
dependencies.

The final isolated controls are `case-152-base-1` and `case-152-gold-1`.

## Directory contract

- `analysis/`: source-row mapping, provenance, environment, and case analysis.
- `patches/`: upstream gold patch and protected regression-test patch.
- `official_swebench/`: private instance, public task, metadata, JSONL, and checksums.
- `evaluator/`: isolated evaluator and clean Base-image definition.
- `verification/`: image-build, Base-control, and gold-control evidence.

## Public/private separation

The model-facing record is `official_swebench/public_task_152.json`. The
private instance, gold patch, protected test patch, and expected outcomes must
not be shown during an unbiased evaluation.
