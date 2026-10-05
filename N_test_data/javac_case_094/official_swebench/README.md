# SWE-bench-compatible record: case 094

- Canonical JSON: `instance_094.json`
- JSONL: `instance_094.jsonl`
- Instance ID: `ninia__jep-40`
- Repository: `ninia/jep`
- Base commit: `bc2edaf0242736c2a2940104eebc6aed5a3ad9e6`
- Fix commit: `8144158fdaf3db44681e5eb4ef9a77907e4746b4`
- Project version: `3.5.0`

The canonical private record embeds the complete gold patch, protected test
patch, `FAIL_TO_PASS`, and `PASS_TO_PASS`. The JSONL file contains the same
single record on one line.

## Patch provenance

- `gold_patch.diff`: `official_upstream_fix_commit`.
- `test_patch.diff`: `dataset_construction_test_derived_from_later_upstream_issue_test`.
- Test authorship: `dataset_construction_team`.

## Public/private separation

`public_task_094.json` is the model-facing record. It intentionally omits
the gold patch, protected test patch, and expected test outcomes. Keep the full
instance, metadata, patches, evaluator assets, and verification evidence private
during an unbiased model evaluation.

## Evaluator contract

The clean image contains the historical toolchain and exact Base checkout only.
At runtime the host applies the candidate patch first, then the protected test
patch, builds the project, runs the tests, and grades every expected target.
