# SWE-bench-compatible record: case 100

- Canonical JSON: `instance_100.json`
- JSONL: `instance_100.jsonl`
- Instance ID: `ninia__jep-9-exceptions`
- Repository: `ninia/jep`
- Base commit: `bbf96b5cbb83fe9e4edef71d410d29460084d5fc`
- Fix commit: `d2ab3f0343a518948ee44f09279e7ccf6922b856`
- Project version: `3.4.0`

The canonical private record embeds the complete gold patch, protected test
patch, `FAIL_TO_PASS`, and `PASS_TO_PASS`. The JSONL file contains the same
single record on one line.

## Patch provenance

- `gold_patch.diff`: `official_upstream_fix_commit`.
- `test_patch.diff`: `official_upstream_regression_test`.
- Test authorship: `ninia/jep_upstream`.

## Public/private separation

`public_task_100.json` is the model-facing record. It intentionally omits
the gold patch, protected test patch, and expected test outcomes. Keep the full
instance, metadata, patches, evaluator assets, and verification evidence private
during an unbiased model evaluation.

## Evaluator contract

The clean image contains the historical toolchain and exact Base checkout only.
At runtime the host applies the candidate patch first, then the protected test
patch, builds the project, runs the tests, and grades every expected target.
