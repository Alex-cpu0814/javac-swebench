# SWE-bench-compatible record

`instance_170.json` and the equivalent one-row JSONL contain the private task, exact upstream Gold, constructed test patch and frozen test lists. `public_task_170.json` contains only the issue-derived task and Base identity. It excludes solution/test patches, Fix SHA, test lists and commands. Supply only this public record and clean Base to a model.

This is a custom Java-C SWE-bench-compatible case, not a claim of official SWE-bench inclusion. Gold is upstream-authored; synthetic tests and the evaluation driver are dataset-construction work. `evaluator/model_patch_example.patch` copies Gold for smoke testing and is not model-generated.

Final classification: 2 FAIL_TO_PASS and 41 PASS_TO_PASS, including 39 unchanged upstream JUnit cases. Metadata discloses the source adapter, pinned JNI binary fixture, runtime scope and protection controls. `SHA256SUMS.txt` uses paths relative to this directory and covers release records, patches, evaluator, documentation and raw verification evidence, excluding itself and regenerable caches.
