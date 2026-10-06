# Evaluation outputs

Each run writes `model-patch.raw.log`, `test-patch.raw.log`,
`project-build.raw.log`, `tests.raw.log`, and `phase.json`. The Surefire report
adapter emits one stable line per test so the expected FAIL_TO_PASS and
PASS_TO_PASS identifiers can be graded without depending on Maven console
formatting.
