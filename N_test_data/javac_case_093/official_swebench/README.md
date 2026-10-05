# SWE-bench-compatible record: case 093

- Canonical JSON: `instance_093.json`
- JSONL: `instance_093.jsonl`
- Instance ID: `ninia__jep-79`
- Repository: `ninia/jep`
- Base commit: `9eeb14c4c8b2d0e49feece90a6e330826b49c7dd`
- Fix commit: `d14567567ac1281e978790b9170c981113de282f`
- Project version: `3.6.3`

The canonical private record embeds the complete gold patch, protected test
patch, `FAIL_TO_PASS`, and `PASS_TO_PASS`. The JSONL file contains the same
single record on one line.

## Patch provenance

- `gold_patch.diff`: `official_upstream_fix_commit`.
- `test_patch.diff`: `dataset_construction_synthetic_test`.
- Test authorship: `dataset_construction_team`.

## Public/private separation

`public_task_093.json` is the model-facing record. It intentionally omits
the gold patch, protected test patch, and expected test outcomes. Keep the full
instance, metadata, patches, evaluator assets, and verification evidence private
during an unbiased model evaluation.

## Evaluator contract

The clean image contains the historical toolchain and exact Base checkout only.
At runtime the host applies the candidate patch first, then the protected test
patch, builds the project, runs the tests, and grades every expected target.
