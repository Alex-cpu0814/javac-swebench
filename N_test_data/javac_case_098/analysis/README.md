# Case 098 analysis

## Identity

- Instance: `ninia__jep-17`
- Repository: `ninia/jep`
- Base: `7af56bffed4e06a2bcdb8b70bf0aa5d59721d7e6`
- Fix: `340788b3ae7a3e4ccfc610f73d43afeba508241c`
- Test source: `official_existing_memory_stress_test_wrapped_for_unittest_runner`

## Construction and verification

The production patch is stored in `patches/gold_patch.diff`; the protected
regression test is stored in `patches/test_patch.diff`. The evaluator applies a
candidate model patch first and the protected test patch second to a clean Base
checkout. Recorded verification status: Base fails =
`None`, Fix passes = `None`.
`FAIL_TO_PASS` and `PASS_TO_PASS` are stored in the private instance and metadata.
