# SWE-bench-compatible record: case 099

- Canonical JSON: `instance_099.json`
- JSONL: `instance_099.jsonl`
- Instance ID: `ninia__jep-17-cache`
- Repository: `ninia/jep`
- Base commit: `b1ab138dd6d492c7547e24d0b117aeafb112613d`
- Fix commit: `778b516930bdc11ecbb7751d560d373964009639`
- Project version: `3.4.0`

The canonical private record embeds the complete gold patch, protected test
patch, `FAIL_TO_PASS`, and `PASS_TO_PASS`. The JSONL file contains the same
single record on one line.

## Patch provenance

- `gold_patch.diff`: `official_upstream_fix_commit`.
- `test_patch.diff`: `synthetic_regression_test_derived_from_commit_and_issue_17`.
- Test authorship: `dataset_construction`.

## Public/private separation

`public_task_099.json` is the model-facing record. It intentionally omits
the gold patch, protected test patch, and expected test outcomes. Keep the full
instance, metadata, patches, evaluator assets, and verification evidence private
during an unbiased model evaluation.

## Evaluator contract

The clean image contains the historical toolchain and exact Base checkout only.
At runtime the host applies the candidate patch first, then the protected test
patch, builds the project, runs the tests, and grades every expected target.
