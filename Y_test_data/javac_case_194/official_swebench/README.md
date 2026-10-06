# Official SWE-bench-compatible record

- `public_task_194.json` is safe for model-facing use.
- `instance_194.json` and `instance_194.jsonl` are private evaluator records.
- `metadata.json` records provenance, expected outcomes, and verification.
- `SHA256SUMS` pins the delivered artifacts.

Do not expose the gold patch, protected test patch, or expected test lists to a
model during an unbiased evaluation.
