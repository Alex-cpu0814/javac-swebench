# Case 097 construction and provenance

This case was previously numbered 096 and keeps instance_id ninia__jep-22. Issue #22 originally reports Linux/amd64. The exact Base and Fix are recorded in source_row_097.json. The complete six-file upstream diff includes Javadoc; no upstream regression source was added in the fix.

`generate_patches.py --git-dir <upstream-bare-repository>` regenerates the exact gold diff, the protected patch from patches/test_source, and the two overbroad close controls. Fetch Fix with its parent in that repository first. The protected child JVM creates on a worker, joins it, and closes from main; it validates completion and a Python destructor side effect. This observes the target JNI path rather than asserting source text. Same-thread and repeated-close P2P detect weakened close behavior.

`verify_controls.py --suffix <fresh-name>` checks Base/Fix, empty close, flag-only close, and test-patch conflict. Original 78 upstream P2P are retained, plus two synthetic P2P. `analysis/tests/test_child_process.py` validates the helper's fail-closed completion checks and timeout handling. `finalize_case.py` binds the current patch, controls, image audit and published-digest smoke run; `verify_case.py` checks identities, outcomes and checksums.

The Windows workspace directory could not be directly renamed while held by another process. It was copied to 097 with all 105 original files SHA-256 compared before changes. Old run/build records retain original 096 IDs and bytes. Active records and newly generated evidence use 097. The published environment is a retag of the audited original Base image, not a claim of a new toolchain build.
