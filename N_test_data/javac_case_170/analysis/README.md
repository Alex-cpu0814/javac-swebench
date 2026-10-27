# Construction and provenance

The selected upstream Fix is `09548dadf52ba6b4f939d0260c391503f478a6a5`, parent `71a134bce58a22fb17a7a14f00799196c0c71a60`. Its complete six-line deletion is preserved in `patches/gold_patch.diff`. It changes only the Java loader and adds no test. Protected integration tests and their Python/Docker driver were constructed with Fix visible; no blind generation claim is made.

`source_provenance.json` fingerprints all 740 Base files using raw Git blobs. `prepare_image_context.py` independently fetches Base if needed, verifies every file and the absence of Fix, checks dependency hashes, and archives the Base-only Git repository including empty directories. Building does not depend on the exploratory case directory.

The image uses digest-pinned Temurin Java 8 on Ubuntu 22.04. System apt packages come from Ubuntu repositories and are recorded in build logs; they are not snapshot-pinned. Public compiler/test dependencies and the official 2.8.0 JNI fixture are individually SHA256-pinned. No compiled common Java JAR is used: candidate core sources are compiled, applying upstream java15/java8 compatibility replacements for Java 8. BuildProperties uses the candidate's upstream template. The declared core source adapter avoids Maven snapshot parent resolution; it does not rebuild native C or full Maven packaging.

Five selected upstream classes cover address serialization/URI handling and large native ports, socket initialization/capabilities, real byte I/O and factories. All 39 discovered methods execute without exclusions or skips. All original common test source files are fingerprint-protected. This is a scoped suite, not all project tests. `evaluator/upstream_tests.json` freezes exact IDs; JUnit XML must match without duplicates, missing cases or skips.

Discovery v1/v2 exposed missing compatibility overlays; these construction logs are retained. Discovery v3 passed 31 methods. The preliminary large-port mutation was not detected by those four classes, so the unchanged domain SocketAddressTest was added. Discovery v4 passed the final 39 tests. The v2 runs establish the final suite before publication. Release validation uses `*-170-published-v1`; earlier runs are historical, including the ineffective mutation.

`write_records.py` synchronizes records and control patches. `verify_controls.py` checks Docker results against current evaluator/patch/image hashes. `finalize_case.py` writes checksums and validates the case layout. References: [issue #140](https://github.com/kohlschutter/junixsocket/issues/140), [Fix](https://github.com/kohlschutter/junixsocket/commit/09548dadf52ba6b4f939d0260c391503f478a6a5).

The release verification uses six `*-170-published-v1` runs against the immutable Docker Hub image. Earlier v2 runs are retained as prepublication evidence; `final_summary.json` points to the release runs.
