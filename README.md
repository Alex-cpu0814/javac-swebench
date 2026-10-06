# Java-C SWE-bench-compatible cases

This repository contains sixteen Java-C cross-language bug cases converted to a
SWE-bench-compatible record format. Cases are separated by test provenance:
`Y_test_data/` contains Fix commits with extractable official regression tests;
`N_test_data/` contains cases whose protected tests were constructed, adapted,
or wrapped during dataset production.

| Set | Case | Instance ID | Issue/PR | FAIL_TO_PASS | PASS_TO_PASS |
|---|---:|---|---:|---:|---:|
| Y | 069 | `LWJGL__lwjgl3-409` | 409 | 1 | 1 |
| Y | 092 | `ninia__jep-77` | 77 | 1 | 121 |
| Y | 100 | `ninia__jep-9-exceptions` | PR 9 | 5 | 69 |
| Y | 112 | `uclouvain__openjpeg-571` | 571 / PR 579 | 1 | 2 |
| Y | 150 | `kohlschutter__junixsocket-116` | 116 | 2 | 1 |
| Y | 152 | `kohlschutter__junixsocket-97` | 97 | 1 | 1 |
| Y | 160 | `kohlschutter__junixsocket-90-write-timeout` | 90 | 1 | 1 |
| Y | 161 | `kohlschutter__junixsocket-90-read-timeout` | 90 | 1 | 1 |
| Y | 175 | `kohlschutter__junixsocket-135` | 135 | 1 | 1 |
| Y | 194 | `MDSplus__mdsplus-1423` | 1423 | 1 | 1 |
| Y | 200 | `MDSplus__mdsplus-2375` | 2375 | 1 | 1 |
| N | 093 | `ninia__jep-79` | 79 | 1 | 130 |
| N | 094 | `ninia__jep-40` | 40 | 1 | 95 |
| N | 096 | `ninia__jep-22` | 22 | 1 | 78 |
| N | 098 | `ninia__jep-17` | 17 | 1 | 78 |
| N | 099 | `ninia__jep-17-cache` | 17 | 1 | 78 |

Case 099 verifies the upstream fix that moves JEP's Java-method cache from
process-global state into each Jep interpreter. Its protected child-JVM test
loads two same-named classes with different methods through separate
ClassLoaders; Base fails and the fix passes all 79 expected tests.

Case 112 reproduces OpenJPEG Issue #571 with a 32-bit x86 GCC build. Its Base
round trip changes 19 pixels, while the upstream fix passes the official
lossless comparison. Published evaluator image:

```text
yutu0814/javac-case-112-openjpeg:benchmark-v1
sha256:33a22445240b5d6abba03d5c41a277d721fc8940f51aa3e7b7138daeb2f87305
```

## Case 092

Case 092 is the current reference implementation. Its evaluator follows the
SWE-bench isolation pattern without requiring the official harness:

```text
clean Base image
  -> inject model patch at container runtime
  -> inject protected test patch at container runtime
  -> build
  -> run tests
  -> grade FAIL_TO_PASS and PASS_TO_PASS
```

The one Base image contains the historical toolchain and a pruned checkout at
the exact Base commit. It does not contain the model patch, protected test
patch, gold patch, Fix source, expected outcomes, or evaluation entrypoint.

Verified Docker Hub image:

```text
yutu0814/javac-case-092-jep:benchmark-v3
sha256:da9c9293093a89f2cfd0e2d584077080c640f0c002cef0589c64e28ac6b550d4
```

### Evaluate a candidate patch

Requirements: Git, Docker with Linux containers, and Python 3.5 or newer.

```powershell
git clone https://github.com/Alex-cpu0814/javac-swebench.git
Set-Location .\javac-swebench\Y_test_data\javac_case_092

docker pull yutu0814/javac-case-092-jep:benchmark-v3

python .\evaluator\evaluate_model_patch.py `
  --patch C:\path\to\my_model_patch.diff
```

The default image is read from `evaluator/case_config.json`. Results are stored
under `verification/runs/<run-id>/`:

- `summary.json`: final `resolved`, `unresolved`, or `error` result.
- `grading.json`: per-test F2P/P2P results.
- `events.jsonl`: structured schema-3.0 event log.
- `*.raw.log`: unmodified patch, build, test, and Docker output.

Exit code `0` means resolved, `1` means the candidate is unresolved, and `2`
means evaluator/infrastructure error.

The included `patches/gold_patch.diff` is an upstream maintainer control, not
a model-generated answer. Do not use it when measuring model repair ability.

### Use a model-generated patch

The normal model-evaluation workflow is:

1. Give the model the public task record. For example, case 093 uses
   `N_test_data/javac_case_093/official_swebench/public_task_093.json`. This record contains
   the repository, Base commit, issue description, and project version. It does
   not contain the gold patch or the protected test patch.
2. Ask the model to return a Git unified diff based on the recorded Base commit.
   The output should be an applyable patch, not a prose explanation or a full
   replacement file. A useful instruction is:

   ```text
   Return only a Git unified diff that can be applied with `git apply`.
   Do not include Markdown code fences or explanatory text.
   ```

3. Save the model output as a file, for example
   `C:\temp\case093-model.patch`. If the model wrapped the diff in
   ```` ```diff ```` fences, remove those fences and keep only the diff. The
   candidate patch should change production code; the evaluator applies the
   protected test patch separately.
4. Optionally validate the patch against a clean local checkout of the case's
   Base commit before using Docker:

   ```powershell
   git apply --check C:\temp\case093-model.patch
   ```

   This check is meaningful only when run from a checkout at the exact Base
   commit. It is not necessary to build the project locally.
5. Run the evaluator from the selected case directory:

   ```powershell
   Set-Location .\N_test_data\javac_case_093
   python .\evaluator\evaluate_model_patch.py `
     --patch C:\temp\case093-model.patch `
     --label model-1
   ```

   Use `N_test_data/javac_case_094` and `case094-model.patch` for case 094. The evaluator
   mounts the candidate patch into a clean Docker container, applies it first,
   applies the protected tests second, builds the project, and grades the test
   results. Do not manually copy the patch into the Docker image.
6. Inspect the newest directory under `verification/runs/<run-id>/`:

   ```powershell
   $run = Get-ChildItem .\verification\runs -Directory |
     Sort-Object LastWriteTime -Descending |
     Select-Object -First 1
   Get-Content (Join-Path $run.FullName 'summary.json')
   Get-Content (Join-Path $run.FullName 'grading.json')
   ```

   `resolved` means the candidate satisfies the case's FAIL_TO_PASS and
   PASS_TO_PASS expectations. `unresolved` means the evaluator ran but the
   repair did not satisfy them. `error` means the evaluator or infrastructure
   failed. For diagnostics, inspect `model-patch.raw.log`,
   `test-patch.raw.log`, `project-build.raw.log`, and `tests.raw.log` in the
   same run directory. A `model_patch_apply_failed` result usually means the model
   output was not a valid diff for the Base commit; a
   `candidate_conflicts_with_test_patch` result means the candidate modified
   files or lines reserved for the protected tests.

### Build the image locally (maintainers)

```powershell
Set-Location .\Y_test_data\javac_case_092
.\evaluator\build_model_evaluator.ps1
```

The Docker build clones the upstream repository and checks out the Base commit,
so local image construction requires network access. Normal users only need the
published image.

## Cases 093 and 094

Cases 093 and 094 use the same v3 isolation contract as case 092. Their clean
images contain only the historical toolchain and a detached Base checkout.
Case 093 uses CentOS 7 for allocator reproduction; case 094 uses the 092
Ubuntu/Python 3.5.3 toolchain to avoid an unrelated allocator failure. Candidate
patches, protected test patches, adapters, and grading assets are mounted at
runtime; gold patches and Fix commits are not present in the images.

Published images:

```text
yutu0814/javac-case-093-jep:benchmark-v3
sha256:acc01f758d28a94ab99d3e35eeaee06bd65f9a119daf4b2522e469c6994e3942

yutu0814/javac-case-094-jep:benchmark-v3
sha256:afb82e4d2a5d2d58231b723073e32e41abfcdb48272923fbe8bb207908efd859
```

Evaluate a candidate patch from either case directory:

```powershell
Set-Location .\N_test_data\javac_case_093
python .\evaluator\evaluate_model_patch.py `
  --patch C:\path\to\my_model_patch.diff

Set-Location ..\javac_case_094
python .\evaluator\evaluate_model_patch.py `
  --patch C:\path\to\my_model_patch.diff
```

Build and run evidence follows the same `verification/builds/` and
`verification/runs/` layout as case 092. The final gold controls resolve with
F2P/P2P `1/130` for 093 and `1/95` for 094.

## Records and provenance

Each case under `Y_test_data/javac_case_NNN/` or
`N_test_data/javac_case_NNN/` includes SWE-bench-compatible records under
`official_swebench/`:

```text
instance_NNN.json
instance_NNN.jsonl
public_task_NNN.json
metadata.json
README.md
SHA256SUMS.txt
```

`public_task_*.json` is the model-facing task. The complete instance and the
private evaluator materials include oracle information and should not be shown
to a model during an unbiased evaluation. Patch provenance and verification
details are recorded in each case's `metadata.json`.

## Links

- GitHub: [Alex-cpu0814/javac-swebench](https://github.com/Alex-cpu0814/javac-swebench)
- Docker Hub: [yutu0814](https://hub.docker.com/u/yutu0814)

The original source and patches remain subject to the licenses of their
respective upstream projects. Each case records its repository and provenance
under `official_swebench/` and `analysis/`.
