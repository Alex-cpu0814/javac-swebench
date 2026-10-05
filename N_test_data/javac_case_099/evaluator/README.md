# Case 099 isolated model-patch evaluator

The evaluator follows the case-092 isolation contract. Case-specific behavior
is limited to `case_config.json`, `case_adapter.sh`, and `image/Dockerfile`.
The image contains a clean checkout at Base and no gold patch, protected test
patch, Fix source, expected outcomes, or evaluation entrypoint.

Runtime order:

```text
clean Base -> model patch -> protected test patch -> build -> tests -> grade
```

Build evidence is written to `verification/builds/<build-id>/`; evaluation
evidence is written to `verification/runs/<run-id>/`.
