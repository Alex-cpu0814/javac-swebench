# SWE-bench-compatible record: case 069

- Canonical JSON: `instance_069.json`
- JSONL: `instance_069.jsonl`
- Instance ID: `LWJGL__lwjgl3-409`
- Repository: `LWJGL/lwjgl3`
- Base commit: `427e278dc2402aca025cacd58a80eb4eaa8c4832`
- Fix commit: `94f8bd69e176be3e48b4376281fed778e76ab8df`
- Project version: `3.2.1`

The canonical private record embeds the complete gold patch, protected test
patch, `FAIL_TO_PASS`, and `PASS_TO_PASS`. The JSONL file contains the same
single record on one line.

## Patch provenance

- `gold_patch.diff`: `official_upstream_fix_commit`.
- `test_patch.diff`: `official_upstream_regression_test`.
- Test authorship: `LWJGL/lwjgl3_upstream`.

## Public/private separation

`public_task_069.json` is the model-facing record. It intentionally omits
the gold patch, protected test patch, and expected test outcomes. Keep the full
instance, metadata, patches, evaluator assets, and verification evidence private
during an unbiased model evaluation.

## Evaluator contract

The clean image contains the historical toolchain and exact Base checkout only.
At runtime the host applies the candidate patch first, then the protected test
patch, builds the project, runs the tests, and grades every expected target.
