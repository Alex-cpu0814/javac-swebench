# Clean Docker evaluator

Requirements: Python 3.10+ on the host and Docker running Linux amd64 containers.

Build: `python evaluator/build_model_evaluator.py --docker <docker-executable> --run-id <unique-build-id>`.

Evaluate: `python evaluator/evaluate_model_patch.py --docker <docker-executable> --patch <candidate.patch> --run-id <unique-run-id>`.

Run from the case directory. Default image: `local/javac-case-170-junixsocket:benchmark-v1`. The builder stages only the verified Base-only Git archive, eight pinned public JARs and Dockerfile. It audits all 740 Base file hashes, checks Fix is absent, and checks private tests, runtime evaluation assets and compiled project output are absent.

Each fresh container runs offline, with capabilities dropped and no-new-privileges. Actual exec/noexec tmpfs mounts exercise the loader. Read-only mounts supply protected assets. Test applicability is first checked on clean Base; candidate and test patches then apply in that order. Conflicts with protected tests are rejected, and SHA256 guards reject changes to original upstream common tests.

Candidate core Java sources compile with upstream compatibility layers for Java 8. Native code is the same pinned official 2.8.0 JNI runtime fixture across candidates. Full Maven/native-source rebuild and grading candidate C changes are outside this adapter's scope. Positive cases perform real native I/O; all-blocked retains a real loading failure. Child logs record commands, mount flags, class origin and mapped native library paths. JUnit raw output stays separate from normalized grading lines and is parsed from strict XML.

Exit codes: 0 resolved, 1 unresolved, 2 infrastructure error. `verification/runs/<run-id>` contains phase, summary, grading, events and raw logs. Summaries bind patch/test SHA256, evaluator asset hashes and exact image ID. Builds use `verification/builds/<run-id>`. See `LOGGING.md` for event format.

Recheck the six final controls using `python analysis/verify_controls.py --docker <docker-executable>`. To run fresh controls, choose a new `--revision` with `--run-missing`. Existing results are never silently overwritten or reused with changed fingerprints. New audited images also need the verifier's build evidence path updated; current evidence binds `build-170-published`.

Published image: `yutu0814/javac-case-170-junixsocket@sha256:1a70b55b3d05b7f18257b238ba0ab246f055b03023eb9483d1cafc58703fbde3`. Pull it before evaluation. The default candidate evaluator uses this immutable Docker Hub reference. Local builds use the separate `build_image` tag; evaluate a rebuilt image with explicit `--image <local-tag>` and validate it again. Publication verification uses the `published` suffix (163) or `published-v1` revision (170).
