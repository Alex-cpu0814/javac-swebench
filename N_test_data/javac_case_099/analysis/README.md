# Case 099 analysis

## Identity

- Instance: `ninia__jep-17-cache`
- Repository: `ninia/jep`
- Base: `b1ab138dd6d492c7547e24d0b117aeafb112613d`
- Fix: `778b516930bdc11ecbb7751d560d373964009639`
- Test source: `synthetic_classloader_regression_test`

## Construction and verification

The production patch is stored in `patches/gold_patch.diff`; the protected
regression test is stored in `patches/test_patch.diff`. The evaluator applies a
candidate model patch first and the protected test patch second to a clean Base
checkout. Recorded verification status: Base fails =
`True`, Fix passes = `True`.
`FAIL_TO_PASS` and `PASS_TO_PASS` are stored in the private instance and metadata.
