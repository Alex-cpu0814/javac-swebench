# Java-C SWE-bench Case 163

This case reproduces junixsocket Issue #81: the automatic native-library loader
falls back on glibc 2.12, then the first Unix-domain socket bind terminates Java
with `symbol lookup error: undefined symbol: stat`.

- Instance: `kohlschutter__junixsocket-81`
- Base: `90716d6008c5c9cfa8a061f3d23531acaea29777`
- Fix: `77a4f0c8cd641fc5dfcb62922981c32393c8e079`
- Issue: https://github.com/kohlschutter/junixsocket/issues/81
- Classification: `N_test_data` (synthetic issue-specific regression).

The gold patch is the exact full upstream commit, including the native compiler
configuration change. The protected patch adds one child-JVM probe; production
sources and the selected upstream JUnit tests are not rewritten by the harness.

## Tests

There are **1 FAIL_TO_PASS and 35 PASS_TO_PASS** tests. The target uses the real
automatic loader, bind, connect, accept, and three bidirectional payload exchanges
under glibc 2.12. PASS_TO_PASS comprises the same communication control under
glibc 2.23 plus **34 unchanged upstream JUnit tests**.

All 36 upstream common-module test executions were discovered. AvailableTest's
two cases share a timing-sensitive helper; the untouched Base already failed
testAvailableAtServer (22 expected, 23 observed). Both cases are explicitly
excluded from the frozen P2P selection, remain unmodified, and are not counted
as passing. Discovery reports and the rationale are retained in `analysis/`.

Base fails only the target with child exit 127 and the original `stat` error;
Gold passes all 36 tests. The verified controls also accept an alternative
native fix, detect a port-behavior regression, reject protected-test precreation,
and reject changes to the frozen upstream test sources.

## Evaluation

The published clean-Base image is `yutu0814/javac-case-163-junixsocket:benchmark-v1`.
The evaluator defaults to the immutable reference:
`yutu0814/javac-case-163-junixsocket@sha256:c8b7c236569b9eb461c66197356b0b109088ce31fd0f0057f5441a3afb99e497`.
Its ID and audit are recorded under `verification/builds/case-163-build-final/`.
It contains the historical JDK, Clang, JUnit, QEMU and old glibc, with no Fix
commit, gold patch, injected test, or precompiled project outputs. Runtime
evaluation uses a single nonprivileged, network-disabled container.

See [evaluator/README.md](evaluator/README.md) for build and evaluation commands.
The build adapter compiles the real core Java/JNI sources using the candidate's
native POM/AOL options and upstream default optimization. It does not claim to
run the complete Maven reactor or distribution packaging. Java 8 classpath
compilation omits module-info.java; the unsupported -finline-functions flag is
removed identically for both versions.

The model-facing record is `official_swebench/public_task_163.json`. Keep gold,
protected tests, private records, expected outcomes, and verification evidence
private during an unbiased evaluation. The Fix was visible during test design;
no blind-test-generation claim is made.

## Files

- `analysis/`: provenance, environment, exclusions, and construction utilities.
- `patches/`: exact upstream gold and protected test patches.
- `official_swebench/`: private JSON/JSONL, public task, metadata, checksums.
- `evaluator/`: standalone build and candidate-patch evaluation entrypoints.
- `verification/`: clean-image audit and immutable control runs.

The exploratory working directory and regenerable build caches are removed after
publication. Reproduction provenance and verification logs remain in this case;
evaluation and image rebuilding are independent of exploratory files.

Published-image quick start (Docker executable on PATH):

```powershell
docker pull yutu0814/javac-case-163-junixsocket@sha256:c8b7c236569b9eb461c66197356b0b109088ce31fd0f0057f5441a3afb99e497
python .\evaluator\evaluate_model_patch.py --patch .\patches\gold_patch.diff --run-id consumer-gold-163
```
