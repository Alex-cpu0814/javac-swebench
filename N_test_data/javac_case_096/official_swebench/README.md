# SWE-bench-compatible record: case 096

- Canonical JSON: `instance_096.json`
- JSONL: `instance_096.jsonl`
- Instance ID: `ninia__jep-22`
- Repository: `ninia/jep`
- Base commit: `e4f13ea277ce4809688dde766cc9fd173ec6f63d`
- Fix commit: `767509de81f3a11b1ca54e23619d3226944a141e`
- Project version: `3.4.0`

The canonical private record embeds the complete gold patch, protected test
patch, `FAIL_TO_PASS`, and `PASS_TO_PASS`. The JSONL file contains the same
single record on one line.

## Patch provenance

- `gold_patch.diff`: `official_upstream_fix_commit`.
- `test_patch.diff`: `synthetic_regression_test_derived_from_issue_22`.
- Test authorship: `dataset_construction`.

## Public/private separation

`public_task_096.json` is the model-facing record. It intentionally omits
the gold patch, protected test patch, and expected test outcomes. Keep the full
instance, metadata, patches, evaluator assets, and verification evidence private
during an unbiased model evaluation.

## Evaluator contract

The clean image contains the historical toolchain and exact Base checkout only.
At runtime the host applies the candidate patch first, then the protected test
patch, builds the project, runs the tests, and grades every expected target.
