# Java-C SWE-bench Case 100

This case is derived from JEP commit `d2ab3f0343a518948ee44f09279e7ccf6922b856`.
The change maps common Java exceptions to Python built-in exception types and
improves Java import-hook behavior.

## Identity

- Instance: `ninia__jep-9-exceptions`
- Base: `bbf96b5cbb83fe9e4edef71d410d29460084d5fc`
- Fix: `d2ab3f0343a518948ee44f09279e7ccf6922b856`
- Source: https://github.com/ninia/jep/commit/d2ab3f0343a518948ee44f09279e7ccf6922b856

## Verification

The Base tree targets Python 2.6+ and is evaluated with Python 2.7.18,
OpenJDK 8, and NumPy 1.16.6. The Fix run passes all 5 FAIL_TO_PASS and all
69 PASS_TO_PASS tests. The Base run fails the 5 intended tests while all 69
regression tests pass.
