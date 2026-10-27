# Case 163 evaluator

Requirements: Docker Desktop/Linux amd64, Git, and Python 3.8+ on the host.
The container has its own historical Java, native toolchain, Python, JUnit and
glibc runtimes. There is no dependency on host Java or a pre-existing Docker
volume, and no privileged container or nested Docker operation is required.

Run from the case directory:

```powershell
$casePython = 'C:\Users\玉兔\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$caseDocker = 'C:\Users\玉兔\AppData\Local\Programs\DockerDesktop\resources\bin\docker.exe'

& $casePython evaluator\build_model_evaluator.py --docker $caseDocker --build-id my-build
& $casePython evaluator\evaluate_model_patch.py --docker $caseDocker --patch patches\gold_patch.diff --run-id my-gold
& $casePython evaluator\evaluate_model_patch.py --docker $caseDocker --patch C:\path\to\candidate.patch --run-id my-candidate
```

Use fresh run/build IDs; records are never overwritten. Docker engine access is
required. Image construction fetches the exact Base and public dependencies when
not cached; candidate evaluation itself always runs with networking disabled.

The image builder prepares and checks a Base-only Git/source archive and public
toolchain assets. It audits the checkout, the absence of Fix and injected test
assets, and the old glibc/JVM. Candidate evaluation applies the candidate patch,
then the protected patch, rebuilds actual Java/JNI code, and runs the real tests.

`build_project.py` resolves native compiler options from candidate POM/AOL files.
It preserves upstream default optimization (none), adapts -target current to the
native compiler, and omits Clang 3.8's unsupported -finline-functions option.
Both native variants are separately compiled, so the nodeps preprocessor branch
can also be repaired by a candidate. This adapter does not run full Maven/NAR
distribution packaging. Main sources are built on a Java 8 classpath, excluding
module-info.java.

`run_case_tests.py` stores raw child logs and runs all 34 protected upstream IDs
with JUnit 5. It rejects missing, duplicate, unexpected and skipped JUnit results.
The old glibc JVM is executed via QEMU's library prefix within this same
container. Failed or timed-out children cannot pass by printing a success line.

The original test sources are hash-protected. A candidate that changes one is
rejected during build. Precreating the newly added protected test is rejected
when applying the protected patch. Exit 0 means resolved, 1 means unresolved,
and 2 means infrastructure error; always inspect summary.json for the reason.

Full control validation:

```powershell
& $casePython analysis\verify_controls.py --docker $caseDocker --suffix my-controls
```

The shipped release control run IDs use suffix `published`. The evaluator records
candidate/test patch hashes, image ID, and runtime evaluator-asset hashes.

Published image: `yutu0814/javac-case-163-junixsocket@sha256:c8b7c236569b9eb461c66197356b0b109088ce31fd0f0057f5441a3afb99e497`. Pull it before evaluation. The default candidate evaluator uses this immutable Docker Hub reference. Local builds use the separate `build_image` tag; evaluate a rebuilt image with explicit `--image <local-tag>` and validate it again. Publication verification uses the `published` suffix (163) or `published-v1` revision (170).
