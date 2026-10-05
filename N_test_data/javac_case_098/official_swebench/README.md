# SWE-bench-compatible record: case 098

- Canonical JSON: `instance_098.json`
- JSONL: `instance_098.jsonl`
- Instance ID: `ninia__jep-17`
- Repository: `ninia/jep`
- Base commit: `7af56bffed4e06a2bcdb8b70bf0aa5d59721d7e6`
- Fix commit: `340788b3ae7a3e4ccfc610f73d43afeba508241c`
- Project version: `3.2.0`

The canonical private record embeds the complete gold patch, protected test
patch, `FAIL_TO_PASS`, and `PASS_TO_PASS`. The JSONL file contains the same
single record on one line.

## Patch provenance

- `gold_patch.diff`: `official_upstream_fix_commit`.
- `test_patch.diff`: `official_existing_test_wrapped_by_dataset_harness`.
- Test authorship: `dataset_construction`.

## Public/private separation

`public_task_098.json` is the model-facing record. It intentionally omits
the gold patch, protected test patch, and expected test outcomes. Keep the full
instance, metadata, patches, evaluator assets, and verification evidence private
during an unbiased model evaluation.

## Evaluator contract

The clean image contains the historical toolchain and exact Base checkout only.
At runtime the host applies the candidate patch first, then the protected test
patch, builds the project, runs the tests, and grades every expected target.
