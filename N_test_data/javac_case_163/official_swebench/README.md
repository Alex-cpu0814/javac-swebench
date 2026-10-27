# SWE-bench-compatible record: case 163

- Canonical private record: `instance_163.json`
- Equivalent single-row JSONL: `instance_163.jsonl`
- Model-facing record: `public_task_163.json`
- Instance: `kohlschutter__junixsocket-81`
- Base: `90716d6008c5c9cfa8a061f3d23531acaea29777`
- Fix: `77a4f0c8cd641fc5dfcb62922981c32393c8e079`

The private record embeds the complete upstream patch, constructed regression
test patch, one FAIL_TO_PASS ID and 35 PASS_TO_PASS IDs. The latter include 34
unchanged original JUnit tests and one modern-glibc communication control.

Two timing-sensitive AvailableTest cases are explicitly excluded; they are not
rewritten or counted as passing. Test authorship and build scope are disclosed
in metadata.json. The public task omits patches, Fix, test IDs and grading data.

SHA256SUMS.txt is relative to this directory and covers the releasable case files,
including evaluator code and verification logs. Generated image contexts, scratch
Git checkouts, compiled discovery classes and Python caches are not distributed.
