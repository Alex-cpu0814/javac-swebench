# Official SWE-bench-compatible record

- `public_task_150.json` is safe for model-facing use.
- `instance_150.json` and `instance_150.jsonl` are private evaluator records.
- `metadata.json` records provenance, expected outcomes, and verification.
- `SHA256SUMS.txt` pins the delivered artifacts.

Do not expose the gold patch, protected test patch, or expected test lists to a
model during an unbiased evaluation.
