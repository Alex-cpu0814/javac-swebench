# Provenance and scope

Upstream issue: https://github.com/LWJGL/lwjgl3/issues/496

Upstream fix: https://github.com/LWJGL/lwjgl3/commit/50869cf9638ef2225a5ca141bf89d617a920a762

The exact first parent and fix are present in the local Git object store. The official patch includes all 14 files changed by the commit, including generator code and generated Java/C bindings. Protected tests are synthetic and issue-derived. The direct pointer read is a control for a valid CXString, while the public `clang_getCString` call is the F2P target. Both run in separate JVMs on one generated source file. The test deliberately does not call the affected `clang_disposeString` on the old binding.

The earlier 3.2.2/3.2.3 Maven release comparison verified the symptom. The exact commit pair was then tested independently with a clean Base-only image: the old binding failed and the complete Fix passed, while the direct CXString control passed on both. Metadata keeps release and exact-commit evidence separate.
