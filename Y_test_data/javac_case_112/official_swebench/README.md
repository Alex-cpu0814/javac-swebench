# SWE-bench-compatible record: case 112

- Canonical JSON: `instance_112.json`
- JSONL: `instance_112.jsonl`
- Instance ID: `uclouvain__openjpeg-571`
- Repository: `uclouvain/openjpeg`
- Base commit: `4f5ec07c315872bdee0885be085ebf57cede2db9`
- Fix commit: `5d953558de8dc4d939b8147fe9547533a8804297`
- Project version: `2.1.0`

The canonical private record embeds the complete gold patch, protected test
patch, `FAIL_TO_PASS`, and `PASS_TO_PASS`. The JSONL file contains the same
single record on one line.

## Patch provenance

- `gold_patch.diff`: `official_upstream_fix_commit`.
- `test_patch.diff`: `official_upstream_regression_test`.
- Test authorship: `uclouvain/openjpeg_upstream`.

## Public/private separation

`public_task_112.json` is the model-facing record. It intentionally omits
the gold patch, protected test patch, and expected test outcomes. Keep the full
instance, metadata, patches, evaluator assets, and verification evidence private
during an unbiased model evaluation.

## Evaluator contract

The clean image contains the historical toolchain and exact Base checkout only.
At runtime the host applies the candidate patch first, then the protected test
patch, builds the project, runs the tests, and grades every expected target.
