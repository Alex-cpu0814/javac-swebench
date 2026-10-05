# Case 096 analysis

## Identity

- Instance: `ninia__jep-22`
- Repository: `ninia/jep`
- Base: `e4f13ea277ce4809688dde766cc9fd173ec6f63d`
- Fix: `767509de81f3a11b1ca54e23619d3226944a141e`
- Test source: `synthetic_issue_regression_test`

## Construction and verification

The production patch is stored in `patches/gold_patch.diff`; the protected
regression test is stored in `patches/test_patch.diff`. The evaluator applies a
candidate model patch first and the protected test patch second to a clean Base
checkout. Recorded verification status: Base fails =
`True`, Fix passes = `True`.
`FAIL_TO_PASS` and `PASS_TO_PASS` are stored in the private instance and metadata.
