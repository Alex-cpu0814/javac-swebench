# Official SWE-bench-compatible record

- `public_task_175.json` is safe for model-facing use.
- `instance_175.json` and `instance_175.jsonl` are private evaluator records.
- `metadata.json` records provenance, expected outcomes, and verification.
- `SHA256SUMS.txt` pins the delivered artifacts.

Do not expose the gold patch, protected test patch, or expected test lists to a
model during an unbiased evaluation.
