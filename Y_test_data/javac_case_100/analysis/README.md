# Case 100 analysis

## Identity

- Instance: `ninia__jep-9-exceptions`
- Repository: `ninia/jep`
- Base: `bbf96b5cbb83fe9e4edef71d410d29460084d5fc`
- Fix: `d2ab3f0343a518948ee44f09279e7ccf6922b856`
- Test source: `official_upstream_regression_test`

## Construction and verification

The production patch is stored in `patches/gold_patch.diff`; the protected
regression test is stored in `patches/test_patch.diff`. The evaluator applies a
candidate model patch first and the protected test patch second to a clean Base
checkout. Recorded verification status: Base fails =
`True`, Fix passes = `True`.
`FAIL_TO_PASS` and `PASS_TO_PASS` are stored in the private instance and metadata.
