# Case 163 analysis

The reported failure is a real dynamic-linker termination at native bind, not
just an UnsatisfiedLinkError during System.load. A glibc 2.14 memcpy dependency
prevents the preferred library from loading on glibc 2.12. The automatic loader
then uses nodeps, whose direct stat reference cannot be resolved at bind.

The commit's default library instead uses older compatible symbols, so automatic
loading succeeds without entering that fallback. A valid candidate may also
repair the nodeps path; the alternative-fix control verifies that the test does
not hard-code the upstream repair strategy.

## Provenance and build

`source_provenance.json` records canonical upstream Git blob bytes. The earlier
exploratory archive applied Windows line-ending conversion; its original hash
record is retained separately as `exploratory_source_provenance.json`.
The one-time exploratory authoring utility is omitted from the published case;
`prepare_image_context.py` rebuilds independently from the pinned upstream Base.

The initial exploratory -O2 build inlined stat to __xstat and masked the reported
failure. The accepted adapter uses upstream NAR 3.6.0's default optimization
setting (none), and consumes candidate native POM/AOL options. Both normal and
nodeps variants are compiled from candidate source. The generated native symbols
and the published 2.3.2 reference JAR agreed in the original-issue reproduction.
No failure shim, mocked JNI implementation, or preload workaround is used.

The target checkout identifies itself as version 2.3.2, while the issue title
mentions 2.2.0. The reported error also affected the published 2.3.2 reference.

## Regression selection

`upstream_test_selection.json` lists all eligible IDs, the two exclusions, and
the exact hashes of all original common-module test sources. All 36 executions
were initially discovered and exercised, including inherited EndOfFileJavaTest
methods. One AvailableTest failed on untouched Base. Both AvailableTest methods
use the same timing-sensitive helper and are omitted from the frozen P2P list;
the remaining 34 are run unchanged and must all pass without skips.

This is a core-source adapter with the original JUnit tests, not a claim that
the complete Maven reactor, native cross-compilation matrix, or release packaging
has been validated. The record belongs in N_test_data because the issue-specific
test was constructed rather than added by the upstream Fix.
