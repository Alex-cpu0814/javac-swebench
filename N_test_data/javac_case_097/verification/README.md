# Case 097 verification

Current controls are listed in local_evidence.json:

- case-097-base-lifecycle-final: only the terminated-creator target fails, with CLOSING:0 and SIGSEGV in captured child output; 80 P2P pass.
- case-097-gold-lifecycle-final: all 81 tests pass with the complete upstream fix.
- case-097-close-noop-lifecycle-final: empty close fails all three new lifecycle/regression tests; 78 original tests pass.
- case-097-close-flag-only-lifecycle-final: Java closed flags without native teardown fail the same three tests.
- case-097-tamper-lifecycle-final: a candidate supplying the protected Java test is rejected.
- case-097-gold-published-digest: the immutable new Docker Hub image passes all 81 tests with the gold patch.

Each current run has grading.json and raw logs; children/ retains child stdout/stderr and hs_err files retain JVM crash details. case-097-retag-audit records the clean image audit and public digest pull. docker_publication.json records anonymous tag access and immutable identity.

Existing case-096 and manual-20260929 records are historical evidence copied without rewriting their identifiers or bytes. The initial lifecycle fixture trial used builtins.open during interpreter shutdown, which is unavailable in that CPython phase; that failed draft remains local and is excluded from the release. The final sentinel captures raw descriptor functions before shutdown and passes both Base normal-close controls and the full Fix run.
