# Official SWE-bench-compatible record

- `public_task_152.json` is safe for model-facing use.
- `instance_152.json` and `instance_152.jsonl` are private evaluator records.
- `metadata.json` records provenance, deduplication, outcomes, and verification.
- `SHA256SUMS.txt` pins the delivered artifacts.

Do not expose the gold patch, protected test patch, or expected test lists to a
model during an unbiased evaluation.
