# Case 163 verification

The accepted image build is `builds/case-163-build-final/`. Its clean audit proves
the exact Base checkout, no Fix object, no gold or protected patch, no injected
probe, and no precompiled project output. Public JUnit and toolchain dependencies
are allowed; all task-specific evaluation assets are injected read-only at runtime.

`final_summary.json` binds all six controls to the same image, test patch, and
runtime evaluator-asset hashes:

| Control | Expected and observed |
| --- | --- |
| Base | Only old-glibc regression fails; original stat error, child exit 127; all 35 P2P pass |
| Gold | All 36 tests pass |
| Alternative native fix | All 36 pass through a safe nodeps fallback repair |
| Gold + port regression | Target passes; only original AFUNIXSocketAddressTest.testPort fails |
| Protected-test precreation | Rejected with candidate_conflicts_with_test_patch |
| Original JUnit modification | Rejected by original-test source-hash protection |

Run directories are immutable and named `case-163-<control>-final`. The final
Base child error is in `runs/case-163-base-final/children/old-glibc.stderr.log`;
the Gold output proves three bidirectional payload exchanges. Detailed JUnit XML
and original console output are retained in each run. Preliminary run records
are preserved separately and are not used for the final control assertions.

Docker Hub publication is recorded in `docker_publication.json`, including the immutable reference and anonymous registry status. The release configuration and all six protection controls use the published image. The release run names are listed in `final_summary.json`; earlier local runs are historical.
