# Case 099 Verification

The gold and protected test patches must apply cleanly to the exact Base commit. Verification requires Base + test patch to fail the child-JVM regression and Fix + test patch to pass it, with the existing regression suite remaining green.

## Helper reuse validation (2026-10-27)

The Python regression now calls `jep_pipe()` instead of duplicating its child
process execution and error reporting. The `CLASSLOADER_CACHE_OK` check remains
in the test. The embedded JSON and JSONL test patches were synchronized.

- Base: `runs/case-099-jep-pipe-base-20261027/summary.json`; the cache regression
  fails with `attr not found: second`, and all 78 existing tests pass.
- Gold: `runs/case-099-jep-pipe-gold-20261027/summary.json`; all 79 tests pass.
- Both runs use image ID
  `sha256:502cb2beb42e3c90413016c2d2ab33dc53fec30912f04ef8eadd47caeae629ee`.

`helper_reuse_validation.json` binds these results to the current test patch
hash. Historical run records retain their original patch hashes.
